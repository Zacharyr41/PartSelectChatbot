from enum import Enum


class QueryType(Enum):
    MAIN = 1
    IS_SEARCHABLE = 2
    SEARCHABLE_TEXT = 3
    IN_SCOPE = 4
    NONE = 5
