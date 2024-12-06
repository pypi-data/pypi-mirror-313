from enum import Enum


class UpsertOperationType(Enum):
    RETRIEVED = 0
    CREATED = 1
    UPDATED = 2
    ERROR = -1
