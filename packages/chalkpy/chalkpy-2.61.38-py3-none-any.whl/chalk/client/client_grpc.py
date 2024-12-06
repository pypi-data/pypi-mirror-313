from __future__ import annotations

import collections.abc
import dataclasses
import datetime as dt
import random
import warnings
from functools import cached_property
from typing import TYPE_CHECKING, Any, List, Mapping, Optional, Sequence, Tuple, Union, final
from urllib.parse import urlparse

import grpc
import grpc.experimental
from google.protobuf import timestamp_pb2

from chalk import DataFrame, EnvironmentId
from chalk._gen.chalk.auth.v1.agent_pb2 import CustomClaim
from chalk._gen.chalk.auth.v1.permissions_pb2 import Permission
from chalk._gen.chalk.common.v1 import online_query_pb2, upload_features_pb2
from chalk._gen.chalk.common.v1.online_query_pb2 import GenericSingleQuery, UploadFeaturesBulkRequest
from chalk._gen.chalk.engine.v1 import query_server_pb2
from chalk._gen.chalk.engine.v1.query_server_pb2_grpc import QueryServiceStub
from chalk._gen.chalk.graph.v1.graph_pb2 import Graph
from chalk._gen.chalk.server.v1.auth_pb2_grpc import AuthServiceStub
from chalk._gen.chalk.server.v1.graph_pb2 import GetGraphRequest, GetGraphResponse
from chalk._gen.chalk.server.v1.graph_pb2_grpc import GraphServiceStub
from chalk._gen.chalk.server.v1.team_pb2 import (
    CreateServiceTokenRequest,
    CreateServiceTokenResponse,
    ListServiceTokensRequest,
    ListServiceTokensResponse,
)
from chalk._gen.chalk.server.v1.team_pb2_grpc import TeamServiceStub
from chalk.client import ChalkAuthException, FeatureReference
from chalk.client.models import (
    BulkOnlineQueryResponse,
    BulkOnlineQueryResult,
    BulkUploadFeaturesResult,
    OnlineQuery,
    OnlineQueryResponse,
    UploadFeaturesResponse,
)
from chalk.client.serialization.protos import ChalkErrorConverter, OnlineQueryConverter, UploadFeaturesBulkConverter
from chalk.config.auth_config import load_token
from chalk.features._encoding.inputs import GRPC_ENCODE_OPTIONS, recursive_encode_bulk_inputs
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.outputs import encode_outputs
from chalk.features.feature_set import is_feature_set_class
from chalk.features.tag import DeploymentId
from chalk.importer import CHALK_IMPORT_FLAG
from chalk.parsed._proto.utils import datetime_to_proto_timestamp, value_to_proto
from chalk.utils import df_utils
from chalk.utils.df_utils import record_batch_to_arrow_ipc
from chalk.utils.grpc import AuthenticatedChalkClientInterceptor, TokenRefresher, UnauthenticatedChalkClientInterceptor
from chalk.utils.string import removeprefix

if TYPE_CHECKING:
    from pyarrow import RecordBatch, Table

CHALK_GRPC_TRACE_ID_HEADER: str = "x-chalk-trace-id"


@dataclasses.dataclass
class ParsedUri:
    uri_without_scheme: str
    use_tls: bool


def get_trace_id_from_response(call: grpc.Call) -> Optional[str]:
    for k, v in call.trailing_metadata() or []:
        if k == CHALK_GRPC_TRACE_ID_HEADER:
            if isinstance(v, bytes):
                v = v.decode("utf-8")
            assert isinstance(v, str)  # for pyright
            return v
    return None


def _canonicalize_headers(
    headers: None | Sequence[tuple[str, str | bytes]] | Mapping[str, str | bytes]
) -> tuple[tuple[str, str | bytes], ...]:
    if headers is None:
        return ()
    # NOTE: metadata _keys_ must be lowercase
    if isinstance(headers, collections.abc.Mapping):
        return tuple((k.lower(), v) for (k, v) in headers.items())
    return tuple((k.lower(), v) for (k, v) in headers)


@final
class ChalkGRPCClient:
    def __init__(
        self,
        environment: EnvironmentId | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        api_server: str | None = None,
        deployment_tag: str | None = None,
        additional_headers: List[tuple[str, str]] | None = None,
        query_server: str | None = None,
        **kwargs: Any,
    ):
        """Create a `ChalkGRPCClient` with the given credentials.

        Parameters
        ----------
        environment
            ID of the Chalk environment to connect to. If omitted, this is pulled from the current Chalk project config.
        client_id
            Client ID used to authenticate. If omitted, this is pulled from the current Chalk project config.
        client_secret
            Client secret used to authenticate. If omitted, this is pulled from the current Chalk project config.
        api_server
            URI of the Chalk API server used for authentication/metadata.
        additional_headers
            Additional client metadata to send with GRPC requests.
        query_server
            Hardcoded URI for Chalk query server, if available.
        deployment_tag
            Tag of the deployment to query. If omitted, the active deployment is used.
        """
        environment_id = kwargs.get("environment_id", None)
        if environment is not None and environment_id is not None:
            raise ValueError("Both environment and environment_id specified; only pass environment.")

        if environment_id is not None:
            environment = EnvironmentId(environment_id)

        # deprecating this.
        del environment_id

        if CHALK_IMPORT_FLAG.get() is True:
            raise RuntimeError(
                "Attempting to instantiate a Chalk client while importing source modules is forbidden. "
                + "Please exclude this file from import using your `.chalkignore` file "
                + "(see https://docs.chalk.ai/cli/apply), or wrap this query in a function that is not called upon import."
            )
        additional_headers_nonempty: List[tuple[str, str]] = [] if additional_headers is None else additional_headers
        token_config = load_token(
            client_id=client_id,
            client_secret=client_secret,
            active_environment=environment,
            api_server=api_server,
            skip_cache=False,
        )
        if token_config is None:
            raise ChalkAuthException()

        channel_options: List[tuple[str, str | int]] = [
            ("grpc.max_send_message_length", 1024 * 1024 * 100),  # 100MB
            ("grpc.max_receive_message_length", 1024 * 1024 * 100),  # 100MB
            # https://grpc.io/docs/guides/performance/#python
            (grpc.experimental.ChannelOptions.SingleThreadedUnaryStream, 1),
        ]

        token_refresher: TokenRefresher | None = None
        if kwargs.get("_skip_api_server"):
            # Omits the auth handshake with the API server. Primarily for internal use/testing -- if used in production,
            # this client will simply fail to connect. If True then query_server must be provided & point to
            # `localhost/127.0.0.1`.
            if query_server is None:
                raise ValueError("If skipping API server auth, query_server URI must be provided. ]]")
            elif not (query_server.startswith("localhost") or query_server.startswith("127.0.0.1")):
                warnings.warn(
                    "Skipping API server auth should only be enabled if query_server URI is localhost. It will fail to authenticate against a production engine."
                )
            self._environment_id = token_config.activeEnvironment
            if self._environment_id is None or self._environment_id == "":
                raise ValueError("No environment specified")
            self._server_channel: Optional[grpc.Channel] = None
        else:
            server_host: str = token_config.apiServer or "api.chalk.ai"
            for pfx in ("https://", "http://", "www."):
                server_host = removeprefix(server_host, pfx)

            _unauthenticated_server_channel: grpc.Channel = (
                grpc.insecure_channel(
                    target=server_host,
                    options=channel_options,
                )
                if server_host.startswith("localhost") or server_host.startswith("127.0.0.1")
                else grpc.secure_channel(
                    target=server_host,
                    credentials=grpc.ssl_channel_credentials(),
                    options=channel_options,
                )
            )

            self._auth_stub: AuthServiceStub = AuthServiceStub(
                grpc.intercept_channel(
                    _unauthenticated_server_channel,
                    UnauthenticatedChalkClientInterceptor(
                        server="go-api",
                        additional_headers=additional_headers_nonempty,
                    ),
                )
            )

            token_refresher = TokenRefresher(
                auth_stub=self._auth_stub,
                client_id=token_config.clientId,
                client_secret=token_config.clientSecret,
            )

            t = token_refresher.get_token()

            self._environment_id = token_config.activeEnvironment or t.primary_environment
            if not self._environment_id:
                raise ValueError("No environment specified")

            if self._environment_id not in t.environment_id_to_name:
                lower_env_id = self._environment_id.lower()
                valid = [eid for eid, ename in t.environment_id_to_name.items() if ename.lower() == lower_env_id]
                if len(valid) > 1:
                    raise ValueError(f"Multiple environments with name {self._environment_id}: {valid}")
                elif len(valid) == 0:
                    raise ValueError(f"No environment with name {self._environment_id}: {t.environment_id_to_name}")
                else:
                    self._environment_id = valid[0]

            self._server_channel: Optional[grpc.Channel] = grpc.intercept_channel(
                _unauthenticated_server_channel,
                AuthenticatedChalkClientInterceptor(
                    refresher=token_refresher,
                    server="go-api",
                    environment_id=self._environment_id,
                    additional_headers=additional_headers_nonempty,
                ),
            )

            query_server = query_server or t.grpc_engines.get(self._environment_id, None)
        engine_headers = additional_headers_nonempty + [("x-chalk-deployment-type", "engine-grpc")]
        if deployment_tag is not None:
            engine_headers += [("x-chalk-deployment-tag", deployment_tag)]
        interceptors: List[grpc.UnaryUnaryClientInterceptor] = [
            AuthenticatedChalkClientInterceptor(
                refresher=token_refresher,
                environment_id=self._environment_id,
                server="engine",
                additional_headers=engine_headers,
            )
            if token_refresher is not None
            else UnauthenticatedChalkClientInterceptor(
                server="engine",
                additional_headers=engine_headers + [("x-chalk-env-id", self._environment_id)],
            )
        ]

        self._engine_channel: Optional[grpc.Channel] = None
        if query_server is not None:
            parsed_uri = self._parse_uri_for_engine(query_server_uri=query_server)
            self._engine_channel = grpc.intercept_channel(
                grpc.secure_channel(
                    target=parsed_uri.uri_without_scheme,
                    credentials=grpc.ssl_channel_credentials(),
                    options=channel_options,
                )
                if parsed_uri.use_tls
                else grpc.insecure_channel(
                    target=parsed_uri.uri_without_scheme,
                    options=channel_options,
                ),
                *interceptors,
            )

    _INPUT_ENCODE_OPTIONS = GRPC_ENCODE_OPTIONS

    @classmethod
    def _parse_uri_for_engine(cls, query_server_uri: str) -> ParsedUri:
        """
        If the scheme is provided, base TLS off of that (http = no tls, https = tls)
        If there is no scheme, default to TLS EXCEPT for localhost/private-vpc uris.
        """
        url_parsed = urlparse(query_server_uri)
        if url_parsed.scheme == "http":
            use_tls = False
        elif url_parsed.scheme == "https":
            use_tls = True
        elif url_parsed.scheme == "" and any(
            query_server_uri.startswith(pfx) for pfx in ["localhost", "127.0.0.1", "10."]
        ):
            use_tls = False
        else:
            use_tls = True
        uri_without_scheme = removeprefix(query_server_uri, url_parsed.scheme + "://")
        return ParsedUri(uri_without_scheme=uri_without_scheme, use_tls=use_tls)

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        if self._server_channel is not None:
            self._server_channel.close()
        if self._engine_channel is not None:
            self._engine_channel.close()

    @cached_property
    def _graph_stub(self):
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return GraphServiceStub(self._server_channel)

    @cached_property
    def _team_stub(self):
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return TeamServiceStub(self._server_channel)

    @cached_property
    def _query_stub(self) -> QueryServiceStub:
        if self._engine_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return QueryServiceStub(self._engine_channel)

    def ping_engine(self, num: Optional[int] = None) -> int:
        """Ping the engine to check if it is alive.

        Parameters
        ----------
        num
            A random number to send to the engine. If not provided, a random number is generated.
            This number will be returned as the response.

        Returns
        -------
        int
            The number sent to the engine.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> client = ChalkGRPCClient()
        >>> client.ping_engine(3)
        3
        """
        if num is None:
            num = random.randint(0, 999)
        response = self._query_stub.Ping(query_server_pb2.PingRequest(num=num))
        return response.num

    def online_query(
        self,
        input: Union[Mapping[FeatureReference, Any], Any],
        output: Sequence[FeatureReference] = (),
        now: Optional[dt.datetime] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: List[str] | None = None,
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]] = None,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Any]] = None,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
    ) -> OnlineQueryResponse:
        """Compute features values using online resolvers.
        See https://docs.chalk.ai/docs/query-basics for more information.

        Parameters
        ----------
        input
            The features for which there are known values, mapped to those values.
            For example, `{User.id: 1234}`. Features can also be expressed as snakecased strings,
            e.g. `{"user.id": 1234}`
        output
            Outputs are the features that you'd like to compute from the inputs.
            For example, `[User.age, User.name, User.email]`.

            If an empty sequence, the output will be set to all features on the namespace
            of the query. For example, if you pass as input `{"user.id": 1234}`, then the query
            is defined on the `User` namespace, and all features on the `User` namespace
            (excluding has-one and has-many relationships) will be used as outputs.
        staleness
            Maximum staleness overrides for any output features or intermediate features.
            See https://docs.chalk.ai/docs/query-caching for more information.
        tags
            The tags used to scope the resolvers.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        required_resolver_tags
            If specified, *all* required_resolver_tags must be present on a resolver for it to be
            considered eligible to execute.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        query_name
            The semantic name for the query you're making, for example, `"loan_application_model"`.
            Typically, each query that you make from your application should have a name.
            Chalk will present metrics and dashboard functionality grouped by 'query_name'.
        include_meta
            Returns metadata about the query execution under `OnlineQueryResult.meta`.
            This could make the query slightly slower.
            For more information, see https://docs.chalk.ai/docs/query-basics.
        explain
            Log the query execution plan. Requests using `explain=True` will be slower
            than requests using `explain=False`.

            If `True`, 'include_meta' will be set to `True` as well.
        store_plan_stages
            If `True`, the output of each of the query plan stages will be stored.
            This option dramatically impacts the performance of the query,
            so it should only be used for debugging.
        value_metrics_tag_by_features
            If your environment has feature value metrics enabled, this parameter specified a list of featuers to tag these metrics by.
            For example, if value_metrics_tag_by_features=["user.category_id"], then the feature value metrics stored for this query
            will be tagged with the corresponding user's category_id.
        correlation_id
            You can specify a correlation ID to be used in logs and web interfaces.
            This should be globally unique, i.e. a `uuid` or similar. Logs generated
            during the execution of your query will be tagged with this correlation id.
        now
            The time at which to evaluate the query. If not specified, the current time will be used.
            This parameter is complex in the context of online_query since the online store
            only stores the most recent value of an entity's features. If `now` is in the past,
            it is extremely likely that `None` will be returned for cache-only features.

            This parameter is primarily provided to support:
                - controlling the time window for aggregations over cached has-many relationships
                - controlling the time wnidow for aggregations over has-many relationships loaded from an
                  external database

            If you are trying to perform an exploratory analysis of past feature values, prefer `offline_query`.

        Other Parameters
        ----------------
        meta
            Arbitrary `key:value` pairs to associate with a query.

        headers
            Additional headers to send with the request.

        planner_options
            Dictionary of additional options to pass to the Chalk query engine.
            Values may be provided as part of conversations with Chalk support
            to enable or disable specific functionality.

        request_timeout
            Float value indicating number of seconds that the request should wait before timing out
            at the network level. May not cancel resources on the server processing the query.

        Returns
        -------
        OnlineQueryResponse
            Wrapper around the output features and any query metadata
            and errors encountered while running the resolvers.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> result = ChalkGRPCClient().online_query(
        ...     input={
        ...         User.name: "Katherine Johnson"
        ...     },
        ...     output=[User.fico_score],
        ...     staleness={User.fico_score: "10m"},
        ... )
        """
        bulk_response = self._online_query_grpc_request(
            input=input,
            output=output,
            now=now,
            staleness=staleness,
            tags=tags,
            correlation_id=correlation_id,
            query_name=query_name,
            query_name_version=query_name_version,
            include_meta=include_meta,
            meta=meta,
            explain=explain,
            store_plan_stages=store_plan_stages,
            value_metrics_tag_by_features=value_metrics_tag_by_features,
            encoding_options=encoding_options,
            required_resolver_tags=required_resolver_tags,
            planner_options=planner_options,
            request_timeout=request_timeout,
            headers=headers,
        )
        return OnlineQueryConverter.online_query_bulk_response_decode_to_single(bulk_response)

    def _online_query_grpc_request(
        self,
        *,
        input: Union[Mapping[FeatureReference, Any], Any],
        output: Sequence[FeatureReference] = (),
        now: Optional[dt.datetime] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: List[str] | None = None,
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]] = None,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Any]] = None,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
    ) -> online_query_pb2.OnlineQueryBulkResponse:
        stub = self._query_stub
        request = self._make_query_bulk_request(
            input={k: [v] for k, v in input.items()},
            output=output,
            now=[now] if now is not None else [],
            staleness=staleness or {},
            tags=tags or (),
            correlation_id=correlation_id,
            query_name=query_name,
            query_name_version=query_name_version,
            include_meta=include_meta,
            meta=meta or {},
            explain=explain,
            store_plan_stages=store_plan_stages,
            value_metrics_tag_by_features=value_metrics_tag_by_features,
            encoding_options=encoding_options,
            required_resolver_tags=required_resolver_tags or (),
            planner_options=planner_options or {},
        )
        return stub.OnlineQueryBulk(
            request,
            timeout=request_timeout,
            metadata=_canonicalize_headers(headers),
        )

    def online_query_bulk(
        self,
        input: Union[Mapping[FeatureReference, Sequence[Any]], DataFrame],
        output: Sequence[FeatureReference] = (),
        now: Optional[Sequence[dt.datetime]] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: Optional[List[str]] = None,
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str | bytes] | Sequence[tuple[str, str | bytes]] | None = None,
    ) -> BulkOnlineQueryResult:
        response, call = self._online_query_bulk_grpc_request(
            input=input,
            output=output,
            now=now,
            staleness=staleness,
            tags=tags,
            correlation_id=correlation_id,
            query_name=query_name,
            query_name_version=query_name_version,
            include_meta=include_meta,
            meta=meta,
            explain=explain,
            store_plan_stages=store_plan_stages,
            value_metrics_tag_by_features=value_metrics_tag_by_features,
            encoding_options=encoding_options,
            required_resolver_tags=required_resolver_tags,
            planner_options=planner_options,
            request_timeout=request_timeout,
            headers=headers,
        )
        return OnlineQueryConverter.online_query_bulk_response_decode(
            response, trace_id=get_trace_id_from_response(call)
        )

    def _online_query_bulk_grpc_request(
        self,
        *,
        input: Union[Mapping[FeatureReference, Sequence[Any]], DataFrame],
        output: Sequence[FeatureReference] = (),
        now: Optional[Sequence[dt.datetime]] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: Optional[List[str]] = None,
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]] = None,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str | bytes] | Sequence[tuple[str, str | bytes]] | None = None,
    ) -> Tuple[online_query_pb2.OnlineQueryBulkResponse, grpc.Call]:
        """Returns the raw GRPC response and metadata"""
        stub = self._query_stub
        request = self._make_query_bulk_request(
            input=input,
            output=output,
            now=now or (),
            staleness=staleness or {},
            tags=tags or (),
            correlation_id=correlation_id,
            query_name=query_name,
            query_name_version=query_name_version,
            include_meta=include_meta,
            meta=meta or {},
            explain=explain,
            store_plan_stages=store_plan_stages,
            value_metrics_tag_by_features=value_metrics_tag_by_features,
            encoding_options=encoding_options,
            required_resolver_tags=required_resolver_tags or (),
            planner_options=planner_options or {},
        )
        return stub.OnlineQueryBulk.with_call(request, timeout=request_timeout, metadata=_canonicalize_headers(headers))

    def upload_features_bulk(
        self,
        inputs: "Union[Mapping[FeatureReference, Sequence[Any]], DataFrame, Table, RecordBatch]",
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
    ) -> BulkUploadFeaturesResult:
        stub = self._query_stub
        request = UploadFeaturesBulkRequest(
            inputs_feather=self.get_features_feather_bytes(inputs),
        )
        response, call = stub.UploadFeaturesBulk.with_call(
            request, timeout=request_timeout, metadata=_canonicalize_headers(headers)
        )
        return UploadFeaturesBulkConverter.upload_features_bulk_response_decode(
            response, trace_id=get_trace_id_from_response(call)
        )

    def upload_features(
        self,
        inputs: "Union[Mapping[FeatureReference, Sequence[Any]], DataFrame, Table, RecordBatch]",
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
    ) -> UploadFeaturesResponse:
        """
        Upload data to Chalk to be inserted into the online & offline stores.

        Parameters
        ----------
        inputs:
            Input data can be in one of two formats:
            1. A mapping from a feature or feature name to a list of values:
               `{Transaction.id: ["a", "b", "c"], Transaction.amount: [100.0,200.0,300.0]}`
            2. A tabular format such as arrow Table/RecordBatch, polars Dataframe, chalk.DataFrame
               where each column corresponds to a feature.

        headers:
            Additional headers to send with the request.

        request_timeout:
            Float value indicating number of seconds that the request should wait before timing out
            at the network level. May not cancel resources on the server processing the query.

        :return: UploadFeaturesResponse, which contains a list of errors if any occurred.
        """
        stub = self._query_stub
        request = upload_features_pb2.UploadFeaturesRequest(inputs_table=self.get_features_feather_bytes(inputs))
        response, call = stub.UploadFeatures.with_call(
            request, timeout=request_timeout, metadata=_canonicalize_headers(headers)
        )
        trace_id = get_trace_id_from_response(call)

        py_errors = [ChalkErrorConverter.chalk_error_decode(err) for err in response.errors]
        return UploadFeaturesResponse(errors=py_errors, trace_id=trace_id)

    def multi_query(
        self,
        queries: List[OnlineQuery],
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]] = None,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[Sequence[str]] = None,
        planner_options: Optional[Mapping[str, Any]] = None,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
    ) -> BulkOnlineQueryResponse:
        """Execute a series of independent requests in parallel."""
        requests: List[GenericSingleQuery] = []
        for query in queries:
            # NOTE: This assumed every request is a 'bulk' request.
            if value_metrics_tag_by_features is not None:
                query_vmtbf = value_metrics_tag_by_features
            else:
                query_vmtbf = query.value_metrics_tag_by_features
            request = self._make_query_bulk_request(
                input=query.input,
                output=query.output,
                now=(),
                staleness=query.staleness or {},
                tags=query.tags or (),
                correlation_id=correlation_id,
                query_name=query_name,
                query_name_version=query_name_version,
                include_meta=include_meta,
                meta=meta or {},
                explain=explain,
                store_plan_stages=store_plan_stages,
                value_metrics_tag_by_features=query_vmtbf,
                encoding_options=encoding_options,
                required_resolver_tags=required_resolver_tags or (),
                planner_options=planner_options or {},
            )
            requests.append(GenericSingleQuery(bulk_request=request))
        stub = self._query_stub
        response, call = stub.OnlineQueryMulti.with_call(
            online_query_pb2.OnlineQueryMultiRequest(
                queries=requests,
            ),
            timeout=request_timeout,
            metadata=_canonicalize_headers(headers),
        )
        return OnlineQueryConverter.online_query_multi_response_decode(
            response, trace_id=get_trace_id_from_response(call)
        )

    def _make_query_bulk_request(
        self,
        input: Mapping[FeatureReference, Sequence[Any]] | DataFrame,
        output: Sequence[FeatureReference],
        now: Sequence[dt.datetime],
        staleness: Mapping[FeatureReference, str],
        tags: Sequence[str],
        correlation_id: str | None,
        query_name: str | None,
        query_name_version: str | None,
        include_meta: bool,
        meta: Mapping[str, str],
        explain: bool,
        store_plan_stages: bool,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]],
        encoding_options: FeatureEncodingOptions | None,
        required_resolver_tags: Sequence[str],
        planner_options: Mapping[str, str | int | bool],
    ) -> online_query_pb2.OnlineQueryBulkRequest:
        inputs_bytes = self.get_features_feather_bytes(input)
        outputs = encode_outputs(output)
        value_metrics_tags_encoded = encode_outputs(value_metrics_tag_by_features or [])
        # Currently assume every feature tag is just a fqn instead of a more complex expr.
        value_metrics_tags_proto = [online_query_pb2.OutputExpr(feature_fqn=o) for o in value_metrics_tags_encoded]

        now_proto: List[timestamp_pb2.Timestamp] = []
        for ts in now:
            if ts.tzinfo is None:
                ts = ts.astimezone(tz=dt.timezone.utc)
            now_proto.append(datetime_to_proto_timestamp(ts))

        staleness_encoded: dict[str, str] = {}
        for k, v in staleness.items():
            if is_feature_set_class(k):
                for f in k.features:
                    staleness_encoded[f.root_fqn] = v
            else:
                staleness_encoded[str(k)] = v

        context_options_dict: dict[str, Any] = {
            "store_plan_stages": store_plan_stages,
        }
        context_options_dict.update(**(planner_options or {}))
        context_options_proto = {k: value_to_proto(v) for k, v in context_options_dict.items()}
        return online_query_pb2.OnlineQueryBulkRequest(
            inputs_feather=inputs_bytes,
            outputs=[online_query_pb2.OutputExpr(feature_fqn=o) for o in outputs],
            now=now_proto,
            staleness=staleness_encoded,
            context=online_query_pb2.OnlineQueryContext(
                environment=self._environment_id,
                tags=tags,
                required_resolver_tags=required_resolver_tags,
                correlation_id=correlation_id,
                query_name=query_name,
                query_name_version=query_name_version,
                options=context_options_proto,
                value_metrics_tag_by_features=value_metrics_tags_proto,
            ),
            response_options=online_query_pb2.OnlineQueryResponseOptions(
                include_meta=include_meta,
                explain=online_query_pb2.ExplainOptions() if explain else None,
                encoding_options=online_query_pb2.FeatureEncodingOptions(
                    encode_structs_as_objects=encoding_options.encode_structs_as_objects if encoding_options else False
                ),
                metadata=meta,
            ),
            body_type=online_query_pb2.FEATHER_BODY_TYPE_RECORD_BATCHES,
        )

    def get_features_feather_bytes(
        self, inputs: "Mapping[FeatureReference, Sequence[Any]] | DataFrame | Table | RecordBatch"
    ) -> bytes:
        import pyarrow as pa

        if isinstance(inputs, Mapping):
            inputs, _ = recursive_encode_bulk_inputs(inputs, options=self._INPUT_ENCODE_OPTIONS)

        if isinstance(inputs, DataFrame):
            inputs_table: pa.Table = inputs.to_pyarrow()
            input_batch = df_utils.pa_table_to_recordbatch(inputs_table)
        elif isinstance(inputs, pa.Table):
            input_batch = df_utils.pa_table_to_recordbatch(inputs)
        elif isinstance(inputs, pa.RecordBatch):
            input_batch = inputs
        else:
            encoded_inputs = {str(k): v for k, v in inputs.items()}
            input_batch = pa.RecordBatch.from_pydict(encoded_inputs)
        inputs_bytes = record_batch_to_arrow_ipc(input_batch)
        return inputs_bytes

    def get_graph(self, deployment: DeploymentId | None = None) -> Graph:
        """Get the graph for a given deployment.

        Parameters
        ----------
        deployment
            The id of the Chalk deployment, or `None` to use the latest deployment.

        Returns
        -------
        Graph
            The graph for the given deployment.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> ChalkGRPCClient().get_graph()
        """
        resp: GetGraphResponse = self._graph_stub.GetGraph(GetGraphRequest(deployment_id=deployment))
        return resp.graph

    def create_service_token(
        self,
        name: str,
        permissions: List[Permission],
        customer_claims: Mapping[str, List[str]] | None = None,
    ) -> CreateServiceTokenResponse:
        """Create a service token with a given set of permissions and claims.

        Parameters
        ----------
        name
            The name of your service token.
        permissions
            The permissions that you want your token to have.
        customer_claims
            The customer claims that you want your token to have.

        Returns
        -------
        CreateServiceTokenResponse
            A service token response, including a `client_id` and `client_secret` with
            the specified permissions and customer claims.

        Examples
        --------
        >>> from chalk.client import Permission
        >>> client = ChalkGRPCClient(client_id='test', client_secret='test_secret')
        >>> client.create_service_token(permissions=[Permission.PERMISSION_QUERY_ONLINE])
        """
        return self._team_stub.CreateServiceToken(
            CreateServiceTokenRequest(
                name=name,
                permissions=permissions,
                customer_claims=None
                if customer_claims is None
                else [CustomClaim(key=key, values=values) for key, values in customer_claims.items()],
            )
        )

    def list_service_tokens(self) -> ListServiceTokensResponse:
        """Get all service tokens for the current environment.

        Returns
        -------
        ListServiceTokensResponse
            A list of service tokens for the current environment.

        Examples
        --------
        >>> from chalk.client import Permission
        >>> client = ChalkGRPCClient()
        >>> client.list_service_tokens()
        """
        return self._team_stub.ListServiceTokens(ListServiceTokensRequest())
