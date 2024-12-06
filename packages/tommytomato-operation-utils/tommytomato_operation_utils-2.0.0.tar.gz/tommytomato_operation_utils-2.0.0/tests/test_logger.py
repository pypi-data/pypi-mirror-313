import datetime
import logging
import unittest
from unittest.mock import MagicMock

from tommytomato_utils.database_client.database_client import DatabaseClient
from tommytomato_utils.logger.configure_logging import configure_logging
from tommytomato_utils.logger.log_status import LogStatus


class TestLogger(unittest.TestCase):

    def setUp(self):
        self.db_client = MagicMock(DatabaseClient)
        self.hub_id = "hub123"
        self.run_id = "run456"
        self.user_id = "user789"
        self.tool_name = "my_tool"

    def test_logger_without_db_logging(self):
        custom_logger = configure_logging(log_level=logging.DEBUG)

        with self.assertLogs("tommytomato_operation_utils", level='DEBUG') as cm:
            custom_logger.log(LogStatus.STARTED, "Task has started without DB logging.")
            custom_logger.log(LogStatus.COMPLETED, "Task has completed without DB logging.")

        self.assertIn(
            "INFO:tommytomato_operation_utils:started: Task has started without DB logging.",
            cm.output
        )
        self.assertIn(
            "INFO:tommytomato_operation_utils:completed: Task has completed without DB logging.",
            cm.output
        )

    def test_logger_with_db_logging(self):
        custom_logger = configure_logging(
            db_client=self.db_client,
            hub_id=self.hub_id,
            run_id=self.run_id,
            user_id=self.user_id,
            tool_name=self.tool_name,
            production_date=datetime.date(year=2024, month=10, day=10),
            log_to_db=True,
            log_level=logging.DEBUG
        )

        with self.assertLogs("tommytomato_operation_utils", level='DEBUG') as cm:
            custom_logger.log(LogStatus.STARTED, "Task has started with DB logging.")
            custom_logger.log(LogStatus.COMPLETED, "Task has completed with DB logging.")

        self.assertIn(
            "INFO:tommytomato_operation_utils:started: Task has started with DB logging.",
            cm.output
        )
        self.assertIn(
            "INFO:tommytomato_operation_utils:completed: Task has completed with DB logging.",
            cm.output
        )

        custom_logger.log(LogStatus.STARTED, "Task has started with DB logging.")
        custom_logger.log(LogStatus.COMPLETED, "Task has completed with DB logging.")
        self.assertEqual(len(self.db_client.insert_data.call_args_list), 2)

        # Verify the first log entry
        args, kwargs = self.db_client.insert_data.call_args_list[0]
        log_entry = args[1][0]
        self.assertEqual(log_entry['hub_id'], self.hub_id)
        self.assertEqual(log_entry['run_id'], self.run_id)
        self.assertEqual(log_entry['user_id'], self.user_id)
        self.assertEqual(log_entry['tool_name'], self.tool_name)
        self.assertEqual(log_entry['status'], LogStatus.STARTED.value)
        self.assertEqual(log_entry['message'], "started: Task has started with DB logging.")

        # Verify the second log entry
        args, kwargs = self.db_client.insert_data.call_args_list[1]
        log_entry = args[1][0]
        self.assertEqual(log_entry['status'], LogStatus.COMPLETED.value)
        self.assertEqual(log_entry['message'], "completed: Task has completed with DB logging.")

    def test_missing_db_params(self):
        with self.assertRaises(ValueError):
            configure_logging(db_client=self.db_client, log_to_db=True, log_level=logging.DEBUG)
