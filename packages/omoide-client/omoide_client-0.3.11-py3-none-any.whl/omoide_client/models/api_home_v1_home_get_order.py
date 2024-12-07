from enum import Enum


class ApiHomeV1HomeGetOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"
    RANDOM = "random"

    def __str__(self) -> str:
        return str(self.value)
