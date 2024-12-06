from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, Optional

from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


class CloudSQLSourceImpl(BaseSQLSource):
    kind = SQLSourceKind.cloudsql

    def __init__(
        self,
        *,
        instance_name: Optional[str] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        async_engine_args: Optional[Dict[str, Any]] = None,
    ):
        try:
            import psycopg
            import psycopg2
            from sqlalchemy.dialects import registry  # pyright: ignore
        except ImportError:
            raise missing_dependency_exception("chalkpy[postgresql]")
        del psycopg2  # unused
        del psycopg
        if "postgresql.psycopg" not in registry.impls:
            registry.register(
                "postgresql.psycopg", "chalk.sql._internal.integrations.psycopg3.psycopg_dialect", "dialect"
            )
        if "postgresql.psycopg_async" not in registry.impls:
            registry.register(
                "postgresql.psycopg_async", "chalk.sql._internal.integrations.psycopg3.psycopg_dialect", "dialect_async"
            )
        prefix = name + "_" if name else ""
        self.instance_name = instance_name or os.getenv(prefix + "CLOUDSQL_INSTANCE_NAME")
        self.db = db or os.getenv(prefix + "CLOUDSQL_DATABASE")
        self.user = user or os.getenv(prefix + "CLOUDSQL_USER")
        self.password = password or os.getenv(prefix + "CLOUDSQL_PASSWORD")
        if engine_args is None:
            engine_args = {}
        if async_engine_args is None:
            async_engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        async_engine_args.setdefault("pool_size", 20)
        async_engine_args.setdefault("max_overflow", 60)
        engine_args.setdefault(
            "connect_args",
            {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )
        # We set the default isolation level to autocommit since the SQL sources are read-only, and thus
        # transactions are not needed
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool
        engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        async_engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args=async_engine_args)

    def get_sqlglot_dialect(self) -> str | None:
        return "postgres"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.user,
            password=self.password,
            host="",
            query={"host": "{}/{}/.s.PGSQL.5432".format("/cloudsql", self.instance_name)},
            database=self.db,
        )

    def async_local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="postgresql+psycopg",
            username=self.user,
            password=self.password,
            host="",
            query={"host": "{}/{}/.s.PGSQL.5432".format("/cloudsql", self.instance_name)},
            database=self.db,
        )
