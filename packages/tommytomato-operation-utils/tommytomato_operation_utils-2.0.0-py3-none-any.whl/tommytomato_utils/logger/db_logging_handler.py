from datetime import date, datetime
from logging import Handler, error
from uuid import uuid4

from pytz import timezone

from tommytomato_utils.database_client.database_client import DatabaseClient


class DatabaseLoggingHandler(Handler):

    LOGS_DATABASE_TABLE_NAME = 'ops_tools_logs'

    def __init__(
        self, db_client: DatabaseClient, hub_id: str, run_id: str, user_id: str, tool_name: str,
        production_date: date
    ):
        super().__init__()
        self.db_client = db_client
        self.hub_id = hub_id
        self.run_id = run_id
        self.user_id = user_id
        self.tool_name = tool_name
        self.production_date = production_date

    def emit(self, record):
        try:
            log_status = record.__dict__.get('log_status', 'status_undefined')
        except AttributeError:
            log_status = 'status_undefined'

        log_entry = {
            'id': str(uuid4()),
            'tool_name': self.tool_name,
            'status': log_status,
            'message': record.getMessage(),
            'run_id': self.run_id,
            'user_id': self.user_id,
            'hub_id': self.hub_id,
            'production_date': self.production_date,
            'inserted_at': datetime.now(timezone('Europe/Amsterdam')),
        }
        try:
            self.db_client.insert_data(self.LOGS_DATABASE_TABLE_NAME, [log_entry])
        except Exception as e:
            error(f"Failed to log to database: {e}")
