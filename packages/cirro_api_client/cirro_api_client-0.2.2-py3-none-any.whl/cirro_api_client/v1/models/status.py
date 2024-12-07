from enum import Enum


class Status(str, Enum):
    ARCHIVED = "ARCHIVED"
    COMPLETED = "COMPLETED"
    DELETE = "DELETE"
    DELETED = "DELETED"
    DELETING = "DELETING"
    FAILED = "FAILED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUSPENDED = "SUSPENDED"
    UNKNOWN = "UNKNOWN"
    """ This is a fallback value for when the value is not known, do not use this value when making requests """

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)
