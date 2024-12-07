from enum import Enum


class ListEventsEntityType(str, Enum):
    BILLINGACCOUNT = "BillingAccount"
    DATASET = "Dataset"
    NOTEBOOKINSTANCE = "NotebookInstance"
    PROCESS = "Process"
    PROJECT = "Project"
    SAMPLE = "Sample"
    USER = "User"
    USERPROJECTASSIGNMENT = "UserProjectAssignment"
    UNKNOWN = "UNKNOWN"
    """ This is a fallback value for when the value is not known, do not use this value when making requests """

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, number):
        return cls(cls.UNKNOWN)
