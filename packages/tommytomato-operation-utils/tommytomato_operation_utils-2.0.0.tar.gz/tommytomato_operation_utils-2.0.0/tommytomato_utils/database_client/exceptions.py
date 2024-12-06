from typing import List

from sqlalchemy import Table


class NoValidPasswordProvidedError(Exception):

    def __init__(self, password: str):
        super().__init__(
            "Improper configuration! "
            "You have not passed a valid password.\n"
            f"Password: '{password}'"
        )


class DatabaseConnectionError(Exception):

    def __init__(self, message: str):
        super().__init__(f"Failed to connect to the database: {message}")


class ColumnMismatchError(Exception):

    def __init__(self, table: Table, missing_columns: List[str]):
        super().__init__(
            f"Missing columns in DataFrame to upload to database for table '{table.name}':"
            f"{missing_columns}"
        )


class TableNotFoundInReflectedDatabaseSchemaError(Exception):

    def __init__(self, table_name: str):
        super().__init__(f"The table '{table_name}' is not available in the reflected schema")


class SchemaAlreadyExistsError(Exception):

    def __init__(self, table_names: List[str]):
        super(
        ).__init__(f"The schema already contains the following tables: {', '.join(table_names)}")
