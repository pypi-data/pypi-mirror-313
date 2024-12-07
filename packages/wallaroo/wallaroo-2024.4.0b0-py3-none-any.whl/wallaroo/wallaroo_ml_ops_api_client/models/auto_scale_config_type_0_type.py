from enum import Enum


class AutoScaleConfigType0Type(str, Enum):
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
