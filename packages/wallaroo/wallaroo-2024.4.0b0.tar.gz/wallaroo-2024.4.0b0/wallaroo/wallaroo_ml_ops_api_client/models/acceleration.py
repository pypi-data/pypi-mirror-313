from enum import Enum


class Acceleration(str, Enum):
    CUDA = "cuda"
    JETSON = "jetson"
    NONE = "none"
    OPENVINO = "openvino"

    def __str__(self) -> str:
        return str(self.value)
