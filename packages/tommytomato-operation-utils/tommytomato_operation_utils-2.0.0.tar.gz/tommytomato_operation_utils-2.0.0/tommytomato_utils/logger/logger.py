import logging

from tommytomato_utils.logger.log_status import LogStatus


class Logger:

    def __init__(self, name: str = "tommytomato_operation_utils", level: int = logging.INFO):
        """
        Initializes the Logger.

        Args:
            name (str): Name of the logger.
            level (int): Logging level.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self._setup_console_handler(level)

    def _setup_console_handler(self, level: int):
        """
        Sets up the console handler with the specified logging level.

        Args:
            level (int): Logging level.
        """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def add_handler(self, handler: logging.Handler):
        """
        Adds a logging handler to the logger.

        Args:
            handler (logging.Handler): Logging handler to add.
        """
        self.logger.addHandler(handler)

    def get_logger(self):
        """
        Returns the logger instance.
        """
        return self.logger

    def log(self, status: LogStatus, message: str):
        """
        Logs a message with the given status.

        Args:
            status (LogStatus): Logging status.
            message (str): Log message.
        """
        formatted_message = f"{status.value}: {message}"
        extra = {
            'log_status': status.value
        }
        self.logger.log(logging.INFO, formatted_message, extra=extra)
