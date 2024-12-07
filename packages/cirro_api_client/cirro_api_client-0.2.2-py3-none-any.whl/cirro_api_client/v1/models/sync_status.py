from enum import Enum


class SyncStatus(str, Enum):
    FAILED = "FAILED"
    SUCCESSFUL = "SUCCESSFUL"
    UNKNOWN = "UNKNOWN"
    """ This is a fallback value for when the value is not known, do not use this value when making requests """

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)
