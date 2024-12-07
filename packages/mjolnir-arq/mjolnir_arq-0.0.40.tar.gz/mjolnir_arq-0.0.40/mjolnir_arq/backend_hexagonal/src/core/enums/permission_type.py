from enum import Enum


class PERMISSION_TYPE(str, Enum):
    UPDATE = "UPDATE"
    READ = "READ"
    DELETE = "DELETE"
    SAVE = "SAVE"
    LIST = "LIST"
