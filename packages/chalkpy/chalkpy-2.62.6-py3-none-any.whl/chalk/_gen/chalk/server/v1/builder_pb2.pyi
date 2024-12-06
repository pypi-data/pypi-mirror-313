from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import deployment_pb2 as _deployment_pb2
from chalk._gen.chalk.server.v1 import log_pb2 as _log_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class DeploymentBuildStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEPLOYMENT_BUILD_STATUS_UNSPECIFIED: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_UNKNOWN: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_PENDING: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_QUEUED: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_WORKING: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_SUCCESS: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_FAILURE: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_INTERNAL_ERROR: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_TIMEOUT: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_CANCELLED: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_EXPIRED: _ClassVar[DeploymentBuildStatus]
    DEPLOYMENT_BUILD_STATUS_BOOT_ERRORS: _ClassVar[DeploymentBuildStatus]

DEPLOYMENT_BUILD_STATUS_UNSPECIFIED: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_UNKNOWN: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_PENDING: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_QUEUED: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_WORKING: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_SUCCESS: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_FAILURE: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_INTERNAL_ERROR: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_TIMEOUT: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_CANCELLED: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_EXPIRED: DeploymentBuildStatus
DEPLOYMENT_BUILD_STATUS_BOOT_ERRORS: DeploymentBuildStatus

class ActivateDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id",)
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    def __init__(self, existing_deployment_id: _Optional[str] = ...) -> None: ...

class ActivateDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IndexDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id",)
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    def __init__(self, existing_deployment_id: _Optional[str] = ...) -> None: ...

class IndexDeploymentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeployKubeComponentsRequest(_message.Message):
    __slots__ = ("existing_deployment_id",)
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    def __init__(self, existing_deployment_id: _Optional[str] = ...) -> None: ...

class DeployKubeComponentsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RebuildDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id", "new_image_tag", "base_image_override", "enable_profiling")
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_IMAGE_TAG_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    new_image_tag: str
    base_image_override: str
    enable_profiling: bool
    def __init__(
        self,
        existing_deployment_id: _Optional[str] = ...,
        new_image_tag: _Optional[str] = ...,
        base_image_override: _Optional[str] = ...,
        enable_profiling: bool = ...,
    ) -> None: ...

class RebuildDeploymentResponse(_message.Message):
    __slots__ = ("build_id",)
    BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    build_id: str
    def __init__(self, build_id: _Optional[str] = ...) -> None: ...

class RedeployDeploymentRequest(_message.Message):
    __slots__ = ("existing_deployment_id", "enable_profiling")
    EXISTING_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    existing_deployment_id: str
    enable_profiling: bool
    def __init__(self, existing_deployment_id: _Optional[str] = ..., enable_profiling: bool = ...) -> None: ...

class RedeployDeploymentResponse(_message.Message):
    __slots__ = ("build_id", "deployment_id")
    BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    build_id: str
    deployment_id: str
    def __init__(self, build_id: _Optional[str] = ..., deployment_id: _Optional[str] = ...) -> None: ...

class UploadSourceRequest(_message.Message):
    __slots__ = (
        "deployment_id",
        "archive",
        "no_promote",
        "dependency_hash",
        "base_image_override",
        "use_grpc",
        "enable_profiling",
    )
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    NO_PROMOTE_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCY_HASH_FIELD_NUMBER: _ClassVar[int]
    BASE_IMAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    USE_GRPC_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    archive: bytes
    no_promote: bool
    dependency_hash: str
    base_image_override: str
    use_grpc: bool
    enable_profiling: bool
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        archive: _Optional[bytes] = ...,
        no_promote: bool = ...,
        dependency_hash: _Optional[str] = ...,
        base_image_override: _Optional[str] = ...,
        use_grpc: bool = ...,
        enable_profiling: bool = ...,
    ) -> None: ...

class UploadSourceResponse(_message.Message):
    __slots__ = ("status", "progress_url")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_URL_FIELD_NUMBER: _ClassVar[int]
    status: str
    progress_url: str
    def __init__(self, status: _Optional[str] = ..., progress_url: _Optional[str] = ...) -> None: ...

class GetDeploymentStepsRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class DeploymentBuildStep(_message.Message):
    __slots__ = ("id", "display_name", "status", "start_time", "end_time")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    id: str
    display_name: str
    status: DeploymentBuildStatus
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        display_name: _Optional[str] = ...,
        status: _Optional[_Union[DeploymentBuildStatus, str]] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetDeploymentStepsResponse(_message.Message):
    __slots__ = ("steps", "deployment")
    STEPS_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    steps: _containers.RepeatedCompositeFieldContainer[DeploymentBuildStep]
    deployment: _deployment_pb2.Deployment
    def __init__(
        self,
        steps: _Optional[_Iterable[_Union[DeploymentBuildStep, _Mapping]]] = ...,
        deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...,
    ) -> None: ...

class GetDeploymentLogsRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class GetDeploymentLogsResponse(_message.Message):
    __slots__ = ("logs",)
    LOGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[_log_pb2.LogEntry]
    def __init__(self, logs: _Optional[_Iterable[_Union[_log_pb2.LogEntry, _Mapping]]] = ...) -> None: ...

class GetClusterTimescaleDBRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class GetClusterTimescaleDBResponse(_message.Message):
    __slots__ = ("id", "specs_string", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    specs_string: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        specs_string: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetClusterGatewayRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class GetClusterGatewayResponse(_message.Message):
    __slots__ = ("id", "specs_string", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    specs_string: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        specs_string: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class BackgroundPersistence(_message.Message):
    __slots__ = ("id", "kind", "specs_string", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    kind: str
    specs_string: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        specs_string: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetClusterBackgroundPersistenceRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class GetClusterBackgroundPersistenceResponse(_message.Message):
    __slots__ = ("background_persistence",)
    BACKGROUND_PERSISTENCE_FIELD_NUMBER: _ClassVar[int]
    background_persistence: BackgroundPersistence
    def __init__(self, background_persistence: _Optional[_Union[BackgroundPersistence, _Mapping]] = ...) -> None: ...

class CreateClusterTimescaleDBRequest(_message.Message):
    __slots__ = ("environment_id", "environment_ids", "specs_string")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    environment_id: _containers.RepeatedScalarFieldContainer[str]
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    specs_string: str
    def __init__(
        self,
        environment_id: _Optional[_Iterable[str]] = ...,
        environment_ids: _Optional[_Iterable[str]] = ...,
        specs_string: _Optional[str] = ...,
    ) -> None: ...

class CreateClusterTimescaleDBResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MigrateClusterTimescaleDBRequest(_message.Message):
    __slots__ = ("cluster_timescale_id", "migration_image", "environment_ids")
    CLUSTER_TIMESCALE_ID_FIELD_NUMBER: _ClassVar[int]
    MIGRATION_IMAGE_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    cluster_timescale_id: str
    migration_image: str
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        cluster_timescale_id: _Optional[str] = ...,
        migration_image: _Optional[str] = ...,
        environment_ids: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class MigrateClusterTimescaleDBResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateClusterGatewayRequest(_message.Message):
    __slots__ = ("environment_id", "environment_ids", "specs_string")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    environment_id: _containers.RepeatedScalarFieldContainer[str]
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    specs_string: str
    def __init__(
        self,
        environment_id: _Optional[_Iterable[str]] = ...,
        environment_ids: _Optional[_Iterable[str]] = ...,
        specs_string: _Optional[str] = ...,
    ) -> None: ...

class CreateClusterGatewayResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateClusterBackgroundPersistenceRequest(_message.Message):
    __slots__ = ("environment_ids", "specs_string")
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    SPECS_STRING_FIELD_NUMBER: _ClassVar[int]
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    specs_string: str
    def __init__(
        self, environment_ids: _Optional[_Iterable[str]] = ..., specs_string: _Optional[str] = ...
    ) -> None: ...

class CreateClusterBackgroundPersistenceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSearchConfigRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSearchConfigResponse(_message.Message):
    __slots__ = ("team_id", "team_api_key")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_API_KEY_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    team_api_key: str
    def __init__(self, team_id: _Optional[str] = ..., team_api_key: _Optional[str] = ...) -> None: ...

class UpdateEnvironmentVariablesRequest(_message.Message):
    __slots__ = ("environment_variables",)
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    environment_variables: _containers.ScalarMap[str, str]
    def __init__(self, environment_variables: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UpdateEnvironmentVariablesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
