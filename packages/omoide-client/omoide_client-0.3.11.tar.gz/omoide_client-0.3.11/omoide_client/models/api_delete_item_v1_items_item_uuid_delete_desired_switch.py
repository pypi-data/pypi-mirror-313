from enum import Enum


class ApiDeleteItemV1ItemsItemUuidDeleteDesiredSwitch(str, Enum):
    PARENT = "parent"
    SIBLING = "sibling"

    def __str__(self) -> str:
        return str(self.value)
