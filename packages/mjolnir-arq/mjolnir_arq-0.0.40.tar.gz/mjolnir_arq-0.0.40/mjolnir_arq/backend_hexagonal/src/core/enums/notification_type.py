

from enum import Enum


class NOTIFICATION_TYPE(str,Enum):
    SUCCESS = "SUCCESS"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
