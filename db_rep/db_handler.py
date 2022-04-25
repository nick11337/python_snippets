import logging
from urllib import parse
from abc import ABC, abstractmethod
from contextlib import suppress
from dataclasses import dataclass
from typing import Optional, Any, Protocol, NamedTuple

from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine, Connection, URL


class SQLTables(Protocol):
    """Basic Protocol Class for SQLAlchemy Table collection

    Using the Protocol avoids tight dependencies with other packages but enforces a structure at the same time.
    """

    meta: MetaData


class DBCredentials(NamedTuple):
    """Typed credentials object with obfuscated string display

    Using NamedTuple explicitly, should be immutable.
    """

    username: str
    password: str

    def __repr__(self):
        """Password is masked except first and last character"""
        return (
            f"{self.__class__.__name__}(username='{self.username}', "
            f"password='{self.password[0]}{20 * 'X'}{self.password[-1]}')"
        )


class DBConfig(ABC):
    @property
    @abstractmethod
    def connection_string(self) -> str:
        NotImplementedError()


@dataclass
class DBConfigSQLite(DBConfig):
    """For testing purposes that write into a file or per default just in memory"""

    filename: str = ":memory:"

    @property
    def connection_string(self) -> str:
        return f"sqlite:///{self.filename}"


@dataclass
class DBConfigMYSQL(DBConfig):
    """Typed config template for MYSQLServer"""

    credentials: DBCredentials
    server: str
    database: str
    port: int

    @classmethod
    def from_settings(cls, settings: Any):
        """Stub, for alternative constructor from settings"""
        raise NotImplementedError()

    @property
    def connection_string(self) -> str:
        url = URL.create(
            drivername="mysql+mysqlconnector",
            username=self.credentials.username,
            password=self.credentials.password,
            host=self.server,
            port=self.port,
            database=self.database,
        )
        return url


@dataclass
class DBConfigSQLServer(DBConfig):
    """Typed config template for MSSQLServer"""

    credentials: DBCredentials
    server: str
    database: str
    port: int
    driver: str = "{ODBC Driver 17 for SQL Server}"

    @property
    def connection_string(self) -> str:
        """On demand built connection string based on config attributes."""
        conn_core_str = parse.quote_plus(
            f"DRIVER={self.driver};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.credentials.username};"
            f"PWD={self.credentials.password};"
        )
        return (
            f"mssql+pyodbc:///?odbc_connect={conn_core_str}"
        )  # &autocommit=true todo set this?


@dataclass
class DBConfigPostgreSQL(DBConfig):
    """Typed config template for PostgreSQL"""

    credentials: DBCredentials
    server: str
    database: str
    port: int = 5432
    driver: str = "postgresql+psycopg2"

    @property
    def connection_string(self):
        """On demand built connection string based on config attributes."""
        return (
            f"{self.driver}://{self.credentials.username}:{self.credentials.password}"
            f"@{self.server}/{self.database}"
        )


class RDBMHandle:
    """Wrapper for Database Connectivity

    The class expects the usage of a contextmanager. Connections are only started through it:

    >>> with RDBMHandle(DBConfigSQLite()) as db:
    >>>     result = db.conn.execute('select 1').fetchall()

    :param config: dbconfig object specific to the backend
    :param tables: a tables object for sqlalchemy
    :param logger: if needed, a provided logger can be injected
    """

    logger: logging.Logger
    tables: Optional[SQLTables]
    conn: Optional[Connection] = None

    # use for masking schemata in sqlite unittests
    schema_map: dict[str, dict[str, Any]] = {"sqlite": {"metadata": None}}

    def __init__(
        self,
        config: DBConfig,
        tables: Optional[SQLTables] = None,
        logger: Optional[logging.Logger] = None,
        schema_map: Optional[dict[str, dict[str, Any]]] = None,
    ):
        self.logger = logger if logger else logging.getLogger(__name__)
        self.engine = self._get_engine(config)
        self.tables = tables
        if schema_map:
            self.schema_map = schema_map

    def _get_engine(self, configs: DBConfig) -> Engine:
        """Create the engine WITHOUT connecting yet

        An active connection should not be part of the __init__ but should happen later
        in the context manager.
        :param configs: config dataclass customized to the database target
        :return: prepared engine ready for connection
        """
        self.logger.info(f"Creating Engine for {configs=}")
        engine = create_engine(configs.connection_string)
        return engine

    def connect(self) -> Connection:
        """Start the connection for prepared engine"""
        if self.engine.dialect.name in self.schema_map:
            self.conn = self.engine.connect().execution_options(
                schema_translate_map=self.schema_map[self.engine.dialect.name]
            )
        else:
            self.conn = self.engine.connect()
        return self.conn

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with suppress(AttributeError):
            self.conn.close()
            self.engine.dispose()
