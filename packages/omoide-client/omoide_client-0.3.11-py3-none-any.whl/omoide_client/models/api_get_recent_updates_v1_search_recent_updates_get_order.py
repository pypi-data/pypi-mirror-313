from enum import Enum


class ApiGetRecentUpdatesV1SearchRecentUpdatesGetOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"
    RANDOM = "random"

    def __str__(self) -> str:
        return str(self.value)
