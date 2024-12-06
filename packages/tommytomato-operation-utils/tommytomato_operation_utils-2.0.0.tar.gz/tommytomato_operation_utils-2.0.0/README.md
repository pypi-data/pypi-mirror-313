# tommytomato_operation_utils

Utility package for hash generation, database operations, and logging. Requires `Pyton 3.11` or higher

## Installation

```sh
pip install tommytomato_operation_utils
```

## Channel log
**Version 2.0.0**
- Changing logs DB from "ecs_log_tasks" to "ops_tools_logs"

**Version 1.5.1**
- Adding feature to make time-dependent hashes in hashing_client.py. Flag: append_current_time. Default = False.

## Modules
### Hashing Client
The Hashing Client is used to generate hashes from lists of strings or specific columns of a DataFrame.

Usage:

```python
from tommytomato_utils.hashing_client.hashing_client import HashingClient
from tommytomato_utils.hashing_client.exceptions import DuplicateHashValuesError
from pandas import DataFrame

# hash a string
input_string = 'hello'
output = HashingClient.get_hash_uuid_from_string(input_string)
print(output)  # printing hash based on input

# Example usage with a DataFrame
df = DataFrame(
    {
        'col1': ['value1', 'value2'],
        'col2': ['value3', 'value4'],
        'col3': ['value5', 'value6'],
    }
)
hash_columns = ['col1', 'col2']  # columns to hash by

hashed_df = HashingClient.add_dataframe_column_hash_given_column_names(
    df, hash_columns, 'box_id'
)
print(hashed_df)  # column "box_id" added!

# Enforcing unique hash values (no duplicates allowed)
try:
    df_with_duplicates = DataFrame(
        {
            'col1': ['value1', 'value1'],  # Intentional duplicate
            'col2': ['value3', 'value3'],  # Intentional duplicate
        }
    )
    hashed_df_no_duplicates = HashingClient.add_dataframe_column_hash_given_column_names(
        df_with_duplicates, hash_columns, 'box_id', allow_duplicates=False
    )
except DuplicateHashValuesError as e:
    print(e)  # This will raise an error and print the DataFrame with duplicate values

# Making time dependent hashes, while keeping column hash
hashed_df_no_duplicates = HashingClient.add_dataframe_column_hash_given_column_names(
    df_with_duplicates, hash_columns, 'box_id', allow_duplicates=False, append_current_time=True,
)
```
#### Methods:

- `get_hash_uuid_from_string(string_value: str) -> str`: Generates a UUID5 hash from a string.
- `add_dataframe_column_hash_given_column_names(dataframe: DataFrame, hash_column_names: List[str], column_name: str, allow_duplicates: bool = True) -> DataFrame`:
Generates a hash column in a DataFrame based on the specified columns.

Parameters:
- dataframe: The DataFrame to which the hash column will be added.
- hash_column_names: List of column names to concatenate and hash.
- column_name: Name of the new column to store the hash values.
- allow_duplicates: If set to False, the method checks for duplicate hash values. If duplicates are found, a DuplicateHashValuesError is raised, along with the DataFrame showing the duplicate values.

### Database Client
The Database Client provides a set of methods for interacting with a PostgreSQL database, including creating tables, inserting data, and querying data.

Usage:

```python
from tommytomato_utils.database_client.database_client import DatabaseClient, DatabaseClientConfig
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Configuration for the database client
config = DatabaseClientConfig(
    host='localhost',
    port=5432,
    user='user',
    password='password',
    database='test_db'
)

# Creating the DatabaseClient instance with Base
db_client = DatabaseClient(config, base=Base)

# Test connection
db_client.test_connection()

# Create tables
db_client.create_tables()

# Insert data
data = [
    {'column1': 'value1', 'column2': 'value2'},
    {'column1': 'value3', 'column2': 'value4'}
]
db_client.insert_data('table_name', data)

# Query data
query = "SELECT * FROM table_name"
df = db_client.query_data(query)
print(df)
```

#### Classes and Methods:

- `DatabaseClientConfig`: Configuration dataclass for the DatabaseClient.
- `DatabaseClient`: Main class for interacting with the database.
  - `test_connection()`: Test the database connection.
  - `reflect_schema()`: Reflect the database schema.
  - `refresh_schema()`: Refresh the database schema.
  - `session_scope()`: Context manager for database sessions.
  - `create_tables()`: Create tables based on a provided base class. Raises an error if base is not provided.
  - `insert_data(table_name: str, data: List[Dict[str, Any]])`: Insert data into a specified table.
  - `query_data(query)`: Execute a query and return the results as a DataFrame.
  - `execute_sql(sql, params=None)`: Execute a raw SQL statement.

### Logger
The Logger provides logging capabilities to both STDOUT and optionally to a database. It uses a custom logging handler to log messages to a database table if desired.
Usage:

```python
import datetime
import logging

from tommytomato_utils.database_client.database_client import DatabaseClient, DatabaseClientConfig
from tommytomato_utils.logger.configure_logging import configure_logging
from tommytomato_utils.logger.log_status import LogStatus

# Initialize the DatabaseClient
db_client = DatabaseClient(config=DatabaseClientConfig(
  host='localhost',
  port=5432,
  user='user',
  password='password',
  database='database'
))

# Example 1: Logger without database logging
logger1 = configure_logging(log_level=logging.INFO)
logger1.log(LogStatus.STARTED, "Task has started without DB logging.")
logger1.log(LogStatus.COMPLETED, "Task has completed without DB logging.")

# Example 2: Logger with database logging
logger2 = configure_logging(
  db_client=db_client,
  hub_id="hub123",
  run_id="run456",
  user_id="user789",
  tool_name="my_tool",
  production_date=datetime.date(year=2024, month=10, day=10),
  log_to_db = True,
  log_level = logging.INFO
)
logger2.log(LogStatus.STARTED, "Task has started with DB logging.")
logger2.log(LogStatus.COMPLETED, "Task has completed with DB logging.")
logger2.log(LogStatus.FAILED, "Task has failed with DB logging.")
logger2.log(LogStatus.IN_PROGRESS, "Task is in progress with DB logging.")


```
#### Classes and Methods:

- `Logger`: Main class for logging messages.
  - `__init__(name: str = "tommytomato_operation_utils", level: int = logging.INFO)`: Initialize the Logger.
  - `get_logger()`: Returns the logger instance.
  - `log(status: LogStatus, message: str)`: Logs a message with the given status.
- `DatabaseLoggingHandler`: Custom logging handler for logging messages to a database.
  - `__init__(db_client: DatabaseClient, hub_id: str, run_id: str, user_id: str, tool_name: str, production_date: datetime.date)`: Initialize the DatabaseLoggingHandler.
  - `emit(record: logging.LogRecord)`: Emit a log record to the database.
- `configure_logging`: Function to configure logging based on user preferences.
  - `configure_logging(db_client: DatabaseClient = None, hub_id: str = None, run_id: str = None, user_id: str = None, tool_name: str = None, production_date: datetime.date = None, log_to_db: bool = False, log_level: int = logging.INFO)`: Configures the logging setup.
- `LogStatus`: Enum for logging statuses.
  - `LogStatus.STARTED`: Status for started tasks.
  - `LogStatus.COMPLETED`: Status for completed tasks.
  - `LogStatus.FAILED`: Status for failed tasks.
  - `LogStatus.IN_PROGRESS`: Status for tasks in progress.

### Secrets Manager
The Secrets Manager provides functionality to load secrets from environment variables and AWS Secrets Manager.

Usage:

```python
from tommytomato_utils.load_secrets.environment import Environment
from tommytomato_utils.load_secrets.secrets_loader import SecretsLoader

# Determine the environment
env_str = 'TESTING'
current_env = Environment.from_str(env_str)

# List of required secrets
required_secrets = [
    'GDRIVE_CLIENT_SECRET',
    'TOMMY_ADMIN_DJANGO_DB_USER',
    'TOMMY_ADMIN_DJANGO_DB_PASSWORD',
    'OPERATION_DB_USER',
    'OPERATION_DB_PASSWORD'
]

# Load the secrets based on the environment
secrets_loader = SecretsLoader(current_env)
secrets = secrets_loader.load_secrets(required_secrets)

# Use the loaded secrets in your application
GDRIVE_CLIENT_SECRET = secrets.get('GDRIVE_CLIENT_SECRET')
TOMMY_ADMIN_DJANGO_DB_USER = secrets.get('TOMMY_ADMIN_DJANGO_DB_USER')
TOMMY_ADMIN_DJANGO_DB_PASSWORD = secrets.get('TOMMY_ADMIN_DJANGO_DB_PASSWORD')
OPERATION_DB_USER = secrets.get('OPERATION_DB_USER')
OPERATION_DB_PASSWORD = secrets.get('OPERATION_DB_PASSWORD')
```

#### Classes and Methods:

- `Environment`: Enum class for defining valid environments.
  - `possible_environment_values()`: Returns a list of possible environment values.
  - `from_str(env_str: str)`: Converts a string to an Environment enum.
  - `ErrorWhenReadingInSecretsFromAWSSecretsManagerError`: Custom exception for AWS Secrets Manager errors.
- `SecretsLoader`: Class for loading secrets from environment variables and AWS Secrets Manager.
  - `__init__(environment: Environment)`: Initialize the SecretsLoader.
  - `load_env_files()`: Load the base .env file.
  - `validate_secrets(secrets: Dict[str, str], required_secrets: List[str])`: Validate that all required secrets are present.
  - `load_from_env(required_secrets: List[str])`: Load secrets from environment variables.
  - `load_from_aws(required_secrets: List[str])`: Load secrets from AWS Secrets Manager.
  - `load_secrets(required_secrets: List[str])`: Load secrets from environment variables and AWS Secrets Manager, validating that all required secrets are present.

## Deploying a new version (Only Admin)
Clone repository locally
```sh
git clone git@github.com:TommyTomato-BV/ops-python-tommytomato-utils.git
```
Make necessary changes locally and update the version number:
```py
setup(
    name='tommytomato_operation_utils',
    version='1.3.0',  # change this line in the setup.py
    description='Utility package for hash generation and database operations.',
    long_description=open('README.md').read(),
```
Installed required libraries to push to PyPi.
```sh
pip install twine setuptools wheel build
python setup.py sdist bdist_wheel
```
Create distribution files
```sh
python -m build
```
Check distribution files before uploading:
```sh
twine check dist/*
```
Upload
```sh
twine upload dist/*
```
You will be required to fill in your API token, from your PyPi account.
After pushing, wait a couple of minutes and you should be able to query!
