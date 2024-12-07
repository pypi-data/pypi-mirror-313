from enum import Enum


class ApplyAs(str, Enum):
    COPY = "copy"
    DELTA = "delta"

    def __str__(self) -> str:
        return str(self.value)
