"""This module defines custom data types."""

from enum import Enum
from typing import Callable, Tuple, TypeVar, Union

import numpy.typing as npt
import pyarrow as pa
from typing_extensions import TypeAlias

SupportedFrameworks = TypeVar("SupportedFrameworks")

# Arrow converters
ArrowToNDArrayConverter: TypeAlias = Callable[[pa.Array], npt.NDArray]
NDArrayToArrowConverter: TypeAlias = Callable[
    [npt.NDArray],
    Tuple[pa.DataType, Union[pa.Array, pa.ListArray, pa.ExtensionArray]],
]


class ArrowListDType(str, Enum):
    """This class defines the possible PyArrow list data types."""

    FIXED_SIZE_LIST = "fixed_size_list"
    FIXED_SHAPE_TENSOR = "fixed_shape_tensor"
    LIST = "list"


class IOArrowDType(str, Enum):
    """This class defines the possible Arrow pa.ChunkedArray
    data types for the input and output to/from
    an ArrowFlightServer."""

    FIXED_SIZE_LIST = ArrowListDType.FIXED_SIZE_LIST.value
    FIXED_SHAPE_TENSOR = ArrowListDType.FIXED_SHAPE_TENSOR.value
    LIST = ArrowListDType.LIST.value
    SCALAR = "scalar"


class SupportedNATSMessages(str, Enum):
    """This class defines the supported NATS message types."""

    CONVERSION = "conversion"
    PACKAGING = "packaging"
