# MAKINAROCKS CONFIDENTIAL
# ________________________
#
# [2017] - [2024] MakinaRocks Co., Ltd.
# All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of MakinaRocks Co., Ltd. and its suppliers, if any.
# The intellectual and technical concepts contained herein are
# proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
# covered by U.S. and Foreign Patents, patents in process, and
# are protected by trade secret or copyright law. Dissemination
# of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained
# from MakinaRocks Co., Ltd.
from contextlib import contextmanager
from importlib import import_module
from typing import Generator, Dict, Any, Mapping, Union, Sequence
from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import Session, sessionmaker

from runway.common.schemas import DatabaseConfig
from runway.common.values import DatabaseType


class DatabaseClient:
    """
    A class to handle database connections and sessions in a non-pooled way.
    Automatically closes connections after use.
    """

    def __init__(self, config: DatabaseConfig):
        """
        Initialize DatabaseClient with configuration

        Parameters
        ----------
        config : DatabaseConfig
            Database configuration including connection details
        """
        self.config = config
        self._validate_and_import_package()

    def _get_connection_url(self) -> URL:
        """Create SQLAlchemy URL for database connection based on database type"""
        url_configs : Dict[DatabaseType, Dict[str, Any]] = {
            DatabaseType.postgresql: {
                "drivername": "postgresql",
                "required_package": "psycopg2",
            },
            DatabaseType.mysql: {
                "drivername": "mysql+pymysql",
                "required_package": "pymysql",
            },
            DatabaseType.oracle: {
                "drivername": "oracle+cx_oracle",
                "required_package": "cx_Oracle",
            },
            DatabaseType.mssql: {
                "drivername": "mssql+pyodbc",
                "required_package": "pyodbc",
                "query": {
                    "driver": "ODBC Driver 18 for SQL Server",
                    "TrustServerCertificate": "yes",
                },
            },
            DatabaseType.tibero: {
                "drivername": "tibero+pyodbc",
                "required_package": "pyodbc",
                "query": {"driver": "Tibero 6 ODBC Driver", "charset": "UTF8"},
            },
        }

        if self.config.type not in url_configs:
            raise ValueError(f"Unsupported database type: {self.config.type}")

        url_config = url_configs[self.config.type]
        query: Mapping[str, Union[Sequence[str], str]] = url_config.get("query", {})
        return URL.create(
            username=self.config.username,
            password=self.config.password,
            host=self.config.host,
            port=self.config.port,
            database=self.config.database,
            drivername=url_config["drivername"],
            query=query,
        )

    def _get_engine_kwargs(self) -> dict:
        """Get database specific engine configuration"""
        kwargs: Dict[str, Any] = {
            "poolclass": None,
            "pool_pre_ping": True,
            "isolation_level": "READ COMMITTED",
        }
        # Oracle specific settings
        if self.config.type == DatabaseType.oracle:
            kwargs.update(
                {"connect_args": {"encoding": "UTF-8", "nencoding": "UTF-8"}},
            )

        return kwargs

    def _validate_and_import_package(self) -> None:
        """Validate and import required database package"""
        package_map = {
            DatabaseType.postgresql: "psycopg2",
            DatabaseType.mysql: "pymysql",
            DatabaseType.oracle: "cx_Oracle",
            DatabaseType.mssql: "pyodbc",
            DatabaseType.tibero: "pyodbc",
        }
        if self.config.type is not DatabaseType.postgresql:
            raise NotImplementedError(f"Database type {self.config.type} is not supported yet")

        required_package = package_map.get(self.config.type)
        if not required_package:
            raise ValueError(f"Unsupported database type: {self.config.type}")

        try:
            import_module(required_package)
        except ImportError:
            raise ImportError(
                f"Required package '{required_package}' is not installed. "
                f"Please install it to use {self.config.type} database.",
            )

    def _create_engine(self) -> Engine:
        """Create SQLAlchemy engine with no connection pooling"""
        return create_engine(self._get_connection_url(), **self._get_engine_kwargs())

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Create a context managed database session

        Yields
        ------
        Session
            SQLAlchemy session object

        Raises
        ------
        SQLAlchemyError
            If database connection fails
        """
        engine = None
        session = None

        try:
            engine = self._create_engine()
            SessionLocal = sessionmaker(bind=engine)
            session = SessionLocal()

            yield session

            session.commit()

        except Exception as e:
            if session:
                session.rollback()
            raise e

        finally:
            if session:
                session.close()
            if engine:
                engine.dispose()
