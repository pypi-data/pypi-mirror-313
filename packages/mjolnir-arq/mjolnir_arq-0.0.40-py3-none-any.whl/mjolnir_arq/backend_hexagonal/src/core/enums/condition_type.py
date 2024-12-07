from enum import Enum


class CONDITION_TYPE(str, Enum):
    EQUALS = "=="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_THAN_OR_EQUAL_TO = ">="
    LESS_THAN_OR_EQUAL_TO = "<="
    DIFFERENT_THAN = "!="
    LIKE = "like"