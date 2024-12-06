import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from tommytomato_utils.database_client.database_client import DatabaseClient, DatabaseClientConfig
from tommytomato_utils.database_client.exceptions import ColumnMismatchError


class TestDatabaseClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = DatabaseClientConfig(
            host='localhost',
            port=5432,
            user='test_user',
            password='test_password',
            database='test_db'
        )
        cls.Base = declarative_base()
        cls.Base.metadata.clear()  # Clear metadata to prevent conflicts

        # Define a test table within the Base
        class TestTable(cls.Base):
            __tablename__ = 'test_table'
            id = Column(Integer, primary_key=True)
            name = Column(String)
            age = Column(Integer)

    @patch('tommytomato_utils.database_client.database_client.create_engine')
    def setUp(self, mock_create_engine):
        # Mocking the create_engine method to use an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        mock_create_engine.return_value = self.engine
        self.db_client = DatabaseClient(self.config, base=self.Base)
        self.metadata = MetaData()
        # Create a test table
        self.test_table = Table(
            'test_table', self.metadata, Column('id', Integer, primary_key=True),
            Column('name', String), Column('age', Integer)
        )
        self.metadata.create_all(self.engine)
        # Manually add the test table to the db_client's tables dictionary
        self.db_client.tables['test_table'] = self.test_table
        # Creating a sessionmaker for the test class
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        self.metadata.drop_all(self.engine)

    def test_connection(self):
        try:
            self.db_client.test_connection()
        except Exception as e:
            self.fail(f"test_connection raised Exception unexpectedly: {e}")

    def test_reflect_schema(self):
        self.db_client.reflect_schema()
        self.assertIn('test_table', self.db_client.tables)
        self.assertEqual(self.db_client.tables['test_table'].columns.keys(), ['id', 'name', 'age'])

    def test_validate_columns(self):
        df = pd.DataFrame({
            'id': [1],
            'name': ['John'],
            'age': [30]
        })
        try:
            self.db_client._validate_columns(df, self.test_table)
        except Exception as e:
            self.fail(f"_validate_columns raised Exception unexpectedly: {e}")

        df_invalid = pd.DataFrame({
            'id': [1],
            'name': ['John']
        })
        with self.assertRaises(ColumnMismatchError):
            self.db_client._validate_columns(df_invalid, self.test_table)

    def test_order_columns(self):
        df = pd.DataFrame({
            'name': ['John'],
            'age': [30],
            'id': [1]
        })
        ordered_df = self.db_client._order_columns(df, self.test_table)
        self.assertEqual(list(ordered_df.columns), ['id', 'name', 'age'])

    def test_insert_data(self):
        data = [{
            'id': 1,
            'name': 'John',
            'age': 30
        }]
        try:
            self.db_client.insert_data('test_table', data)
        except Exception as e:
            self.fail(f"insert_data raised Exception unexpectedly: {e}")

        with self.engine.connect() as connection:
            result = connection.execute(self.test_table.select()).fetchall()
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0], (1, 'John', 30))

    def test_query_data(self):
        data = [{
            'id': 1,
            'name': 'John',
            'age': 30
        }]
        self.db_client.insert_data('test_table', data)

        query = 'SELECT * FROM test_table'
        df = self.db_client.query_data(query)
        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df.iloc[0]['name'], 'John')

    def test_execute_sql(self):
        data = [{
            'id': 1,
            'name': 'John',
            'age': 30
        }]
        self.db_client.insert_data('test_table', data)

        sql = 'SELECT * FROM test_table WHERE id = :id'
        params = {
            'id': 1
        }
        df = self.db_client.execute_sql(sql, params)
        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df.iloc[0]['name'], 'John')

    def test_query_with_params(self):
        # Insert test data
        data = [{
            'id': 1,
            'name': 'John',
            'age': 30
        }, {
            'id': 2,
            'name': 'Jane',
            'age': 25
        }]
        self.db_client.insert_data('test_table', data)

        # Define the query with parameters
        query = 'SELECT * FROM test_table WHERE age = :age'
        params = {
            'age': 30
        }

        # Execute the query with parameters
        df = self.db_client.execute_sql(query, params)
        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df.iloc[0]['name'], 'John')
        self.assertEqual(df.iloc[0]['age'], 30)

    @patch('tommytomato_utils.database_client.database_client.create_engine')
    @patch(
        'tommytomato_utils.database_client.database_client.DatabaseClient.reflect_schema',
        MagicMock()
    )
    @patch(
        'tommytomato_utils.database_client.database_client.DatabaseClient.test_connection',
        MagicMock()
    )
    def test_create_tables_without_base(self, mock_create_engine):
        mock_create_engine.return_value = create_engine('sqlite:///:memory:')
        db_client_no_base = DatabaseClient(self.config)
        with self.assertRaises(ValueError):
            db_client_no_base.create_tables()

    def test_create_tables_with_base(self):
        # Drop the test table to simulate table creation
        self.metadata.drop_all(self.engine)
        self.db_client.tables.pop('test_table', None)

        try:
            self.db_client.create_tables()
        except Exception as e:
            self.fail(f"create_tables raised Exception unexpectedly: {e}")
