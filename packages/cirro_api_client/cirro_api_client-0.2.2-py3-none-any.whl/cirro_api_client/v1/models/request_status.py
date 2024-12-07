from enum import Enum


class RequestStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    DENIED = "DENIED"
    PENDING = "PENDING"
    UNKNOWN = "UNKNOWN"
    """ This is a fallback value for when the value is not known, do not use this value when making requests """

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)
