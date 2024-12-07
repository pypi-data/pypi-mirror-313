from enum import Enum


class AccessType(str, Enum):
    DATASET_UPLOAD = "DATASET_UPLOAD"
    PROJECT_DOWNLOAD = "PROJECT_DOWNLOAD"
    REFERENCE_UPLOAD = "REFERENCE_UPLOAD"
    SAMPLESHEET_UPLOAD = "SAMPLESHEET_UPLOAD"
    UNKNOWN = "UNKNOWN"
    """ This is a fallback value for when the value is not known, do not use this value when making requests """

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)
