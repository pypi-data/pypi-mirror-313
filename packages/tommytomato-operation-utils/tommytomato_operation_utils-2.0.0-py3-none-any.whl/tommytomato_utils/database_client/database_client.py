import atexit
import logging
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type

import pandas as pd
import sqlalchemy
from sqlalchemy import MetaData, Table, create_engine, exc, text
from sqlalchemy.orm import DeclarativeMeta, sessionmaker
from tenacity import retry, stop_after_attempt, wait_fixed

from tommytomato_utils.database_client.exceptions import (
    ColumnMismatchError, DatabaseConnectionError, NoValidPasswordProvidedError,
    SchemaAlreadyExistsError, TableNotFoundInReflectedDatabaseSchemaError
)

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DatabaseClientConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    def __post_init__(self):
        if not self.password or self.password == 'None':
            raise NoValidPasswordProvidedError(self.password)

    def get_connection_string(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class DatabaseClient:

    def __init__(self, config: DatabaseClientConfig, base: Optional[Type[DeclarativeMeta]] = None):
        self.engine = create_engine(
            config.get_connection_string(),
            pool_pre_ping=True,
            pool_size=1,
            max_overflow=1,
            pool_recycle=1800
        )
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.tables = {}
        self.base = base
        atexit.register(self.close_engine)

        try:
            self.test_connection()
        except exc.SQLAlchemyError as e:
            raise DatabaseConnectionError(str(e))

        self.reflect_schema()

    def test_connection(self):
        with self.engine.connect() as connection:
            connection.execute(text("SELECT 1"))

    def reflect_schema(self):
        self.metadata.reflect(bind=self.engine)
        for table_name, table in self.metadata.tables.items():
            self.tables[table_name] = table
        logger.info("\n\nSchema reflected:\n %s", self.tables.keys())

    def refresh_schema(self):
        self.metadata.clear()
        self.reflect_schema()

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_tables(self):
        if self.base is None:
            raise ValueError("The 'base' parameter must be provided when creating tables.")
        try:
            self._check_if_tables_exist(self.base)
            self.base.metadata.create_all(self.engine)
            logger.info("\nTables created successfully")
            self.refresh_schema()
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while creating tables: {e}")
            raise

    def _check_if_tables_exist(self, base: Type[DeclarativeMeta]):
        existing_tables = set(self.tables.keys())
        new_tables = set(base.metadata.tables.keys())
        intersecting_tables = existing_tables.intersection(new_tables)
        if intersecting_tables:
            raise SchemaAlreadyExistsError(list(intersecting_tables))

    def _validate_and_format_data_before_insert(self, table: Table, data: List[Dict[str, Any]]):
        df = pd.DataFrame(data)
        self._validate_columns(df, table)
        df = self._order_columns(df, table)
        data = df.to_dict(orient='records')
        return data

    def _validate_columns(self, df: pd.DataFrame, table: Table):
        expected_columns = self.tables[table.name].columns.keys()
        df_columns = df.columns.tolist()
        if not all(col in df_columns for col in expected_columns):
            missing_columns = [col for col in expected_columns if col not in df_columns]
            raise ColumnMismatchError(table=table, missing_columns=missing_columns)

    def _order_columns(self, df: pd.DataFrame, table: Table) -> pd.DataFrame:
        table_columns = self.tables[table.name].columns.keys()
        return df[table_columns]

    def insert_data(self, table_name: str, data: List[Dict[str, Any]]):
        if table_name not in self.tables:
            raise TableNotFoundInReflectedDatabaseSchemaError(table_name=table_name)
        table = self.tables[table_name]
        data = self._validate_and_format_data_before_insert(table, data)
        with self.session_scope() as session:
            session.execute(table.insert(), data)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def query_data(self, query):
        if not isinstance(query, str):
            raise ValueError("The query parameter must be a string")
        with self.session_scope() as session:
            try:
                result = session.execute(text(query))
                df = pd.DataFrame(result.fetchall(), columns=list(result.keys()))
                return df
            except sqlalchemy.exc.ProgrammingError as exception:
                logger.error(f"An error occurred while querying data: {exception}")

    def execute_sql(self, sql, params=None):
        with self.session_scope() as session:
            try:
                if params:
                    result = session.execute(text(sql), params)
                else:
                    result = session.execute(text(sql))
                if result.returns_rows:
                    df = pd.DataFrame(result.fetchall(), columns=list(result.keys()))
                    return df
            except exc.SQLAlchemyError as e:
                logger.error(f"An error occurred while executing SQL: {e}")
                raise

    def close_engine(self):
        logger.debug("Closing engine...")
        self.engine.dispose()
