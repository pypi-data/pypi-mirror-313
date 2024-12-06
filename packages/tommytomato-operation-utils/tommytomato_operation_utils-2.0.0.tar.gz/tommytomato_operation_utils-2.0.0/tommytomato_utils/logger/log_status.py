from enum import Enum


class LogStatus(Enum):
    """
    Enum class for the status of a log message.
    """
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
