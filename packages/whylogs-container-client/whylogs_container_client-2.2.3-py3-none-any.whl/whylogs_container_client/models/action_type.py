from enum import Enum


class ActionType(str, Enum):
    BLOCK = "block"
    FLAG = "flag"
    PASS = "pass"

    def __str__(self) -> str:
        return str(self.value)
