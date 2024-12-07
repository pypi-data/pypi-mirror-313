from enum import Enum


class MESSAGE_TYPE(str,Enum):
    STATIC = "STATIC"
    TEMPORARY = "TEMPORARY"
    NONE = "NONE"
