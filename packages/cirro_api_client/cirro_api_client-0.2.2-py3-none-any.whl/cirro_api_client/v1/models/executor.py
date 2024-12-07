from enum import Enum


class Executor(str, Enum):
    CROMWELL = "CROMWELL"
    INGEST = "INGEST"
    NEXTFLOW = "NEXTFLOW"
    OMICS_READY2RUN = "OMICS_READY2RUN"
    UNKNOWN = "UNKNOWN"
    """ This is a fallback value for when the value is not known, do not use this value when making requests """

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)
