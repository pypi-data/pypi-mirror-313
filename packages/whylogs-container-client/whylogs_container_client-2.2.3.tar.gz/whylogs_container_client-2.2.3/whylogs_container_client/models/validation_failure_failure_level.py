from enum import Enum


class ValidationFailureFailureLevel(str, Enum):
    BLOCK = "block"
    FLAG = "flag"

    def __str__(self) -> str:
        return str(self.value)
