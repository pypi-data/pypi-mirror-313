from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


class DatabricksSourceImpl(BaseSQLSource):
    kind = SQLSourceKind.databricks

    def __init__(
        self,
        host: Optional[str] = None,
        http_path: Optional[str] = None,
        access_token: Optional[str] = None,
        db: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        name: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
    ):
        try:
            from databricks import sql
        except ImportError:
            raise missing_dependency_exception("chalkpy[databricks]")
        del sql
        self.host = host or load_integration_variable(name="DATABRICKS_HOST", integration_name=name)
        self.http_path = http_path or load_integration_variable(name="DATABRICKS_HTTP_PATH", integration_name=name)
        self.access_token = access_token or load_integration_variable(name="DATABRICKS_TOKEN", integration_name=name)
        self.db = db or load_integration_variable(name="DATABRICKS_DATABASE", integration_name=name)
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(name="DATABRICKS_PORT", integration_name=name, parser=int)
        )
        if engine_args is None:
            engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        engine_args.setdefault(
            "connect_args",
            {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args={})

    def get_sqlglot_dialect(self) -> str | None:
        return "databricks"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="databricks",
            username="token",
            password=self.access_token,
            host=self.host,
            port=self.port,
            database=self.db,
            query={"http_path": self.http_path or ""},
        )
