from __future__ import annotations

import base64
import json
import os
from typing import TYPE_CHECKING, Any, Dict

from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine
    from sqlalchemy.engine.url import URL


_logger = get_logger(__name__)


class SpannerSourceImpl(BaseSQLSource):
    kind = SQLSourceKind.spanner

    def __init__(
        self,
        name: str | None = None,
        project: str | None = None,
        instance: str | None = None,
        database: str | None = None,
        credentials_base64: str | None = None,
        emulator_host: str | None = None,
        engine_args: Dict[str, Any] | None = None,
    ):
        try:
            from google.cloud import sqlalchemy_spanner
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[spanner]")
        del sqlalchemy_spanner  # unused

        self.ingested_tables: Dict[str, Any] = {}
        self.project_id = project or load_integration_variable(integration_name=name, name="SPANNER_PROJECT")
        self.instance_id = instance or load_integration_variable(integration_name=name, name="SPANNER_INSTANCE")
        self.database_id = database or load_integration_variable(integration_name=name, name="SPANNER_DATABASE")
        self.credentials_base64 = credentials_base64 or load_integration_variable(
            integration_name=name, name="SPANNER_CREDENTIALS_BASE64"
        )
        self.emulator_host = emulator_host or load_integration_variable(
            integration_name=name, name="SPANNER_EMULATOR_HOST"
        )

        eargs = {}
        if engine_args is not None:
            eargs = engine_args
        else:
            found = load_integration_variable(
                integration_name=name,
                name="SPANNER_ENGINE_ARGUMENTS",
                parser=json.loads,
            )
            if found is not None:
                eargs = found

        # The SQL sources are read-only, so transactions are not needed.
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool.
        eargs.setdefault(
            "isolation_level",
            os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"),
        )

        # Spanner defaults to ReadWrite, but Chalk only reads data from spanner.
        eargs.setdefault("read_only", True)

        BaseSQLSource.__init__(self, name=name, engine_args=eargs, async_engine_args={})

    # Spanner does not support using URL, so we need to create the engine directly (rather than using URL)
    def get_engine(self) -> "Engine":
        try:
            from google.auth.credentials import AnonymousCredentials
            from google.cloud import spanner
            from google.oauth2 import service_account
            from sqlalchemy.engine import create_engine
        except ImportError:
            raise missing_dependency_exception("chalkpy[spanner]")

        if self._engine is None:  # pyright: ignore[reportUnnecessaryComparison]
            connect_args = {}

            # Uses workload identity if credentials are not provided
            if self.credentials_base64:
                decoded_credentials = base64.b64decode(self.credentials_base64).decode("utf-8")
                json_acct_info: Dict = json.loads(decoded_credentials)
                credentials = (
                    service_account.Credentials.from_service_account_info(json_acct_info)
                    if not self.emulator_host
                    else AnonymousCredentials()
                )
                connect_args = dict(
                    client=spanner.Client(
                        project=self.project_id,
                        client_options={"api_endpoint": self.emulator_host} if self.emulator_host else None,
                        credentials=credentials,
                    ),
                )
            elif self.emulator_host:
                connect_args = dict(
                    client=spanner.Client(
                        project=self.project_id,
                        client_options={"api_endpoint": self.emulator_host},
                        credentials=AnonymousCredentials(),
                    )
                )

            self._engine = create_engine(
                self.local_engine_url().render_as_string(),  # Spanner adapter does not support URL
                connect_args=connect_args,
            ).execution_options(**self.engine_args)

        return self._engine

    def local_engine_url(self) -> "URL":
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="spanner+spanner",
            host=f"/projects/{self.project_id}/instances/{self.instance_id}",
            database=f"databases/{self.database_id}",
        )

    def get_sqlglot_dialect(self) -> str | None:
        # Both BigQuery and Spanner use the same SQL dialect
        # https://cloud.google.com/bigquery/docs/introduction-sql
        return "bigquery"
