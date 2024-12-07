from enum import Enum


class AppVersion(str, Enum):
    VALUE_0 = "2024.1.0"
    VALUE_1 = "2024.1.5"
    VALUE_2 = "2024.2.0"
    VALUE_3 = "2024.2.1"
    VALUE_4 = "2024.2.2"
    VALUE_5 = "2024.3.0"
    VALUE_6 = "2024.4.0"

    def __str__(self) -> str:
        return str(self.value)
