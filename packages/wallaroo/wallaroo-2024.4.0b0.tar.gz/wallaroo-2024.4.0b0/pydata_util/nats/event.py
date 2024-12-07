"""This module features the modelling dataclasses for
received events through NATS.

In particular, it features a one-to-one mapping of the ModelConversionUpdate
config found in `wallsvc`
(more info here: https://github.com/WallarooLabs/platform/blob/main/conductor/wallsvc/src/models/event.rs).
"""

import base64
import logging
from typing import Any, Dict, Generic, Optional, Union

import pyarrow as pa
from pydantic import (
    BaseModel,
    ConfigDict,
    DirectoryPath,
    EncodedBytes,
    EncoderProtocol,
    FilePath,
    model_validator,
)
from typing_extensions import Annotated

from pydata_util.types import SupportedFrameworks

logger = logging.getLogger(__name__)


class Conversion(BaseModel, Generic[SupportedFrameworks]):
    """This dataclass stores data related to
    the conversion of a model."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="allow",
    )

    framework: SupportedFrameworks
    settings: Optional[Dict[str, Any]] = None

    @model_validator(mode="before")
    @classmethod
    def split_task_from_framework_if_necessary(cls, data: Any) -> Any:
        """Split the task from the framework if necessary and assign it to
        the settings attribute."""
        # Until we separate tasks from framework in the HuggingFace case
        framework = data.get("framework")
        if framework.startswith("hugging-face"):
            data["framework"] = "hugging-face"
            data["settings"] = {"task": framework.split("hugging-face-")[1]}

        return data


class FileInfo(BaseModel):
    """This dataclass stores data related to
    a model file."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra="allow",
    )

    sha: str
    file_name: Union[FilePath, DirectoryPath]


class ModelVersion(BaseModel, Generic[SupportedFrameworks]):
    """This dataclass stores data related to
    a model version."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="allow",
    )

    name: str
    conversion: Conversion[SupportedFrameworks]
    workspace_id: int
    file_info: FileInfo


class SchemaEncoder(EncoderProtocol):
    """This class implements a custom encoder/decoder
    for PyArrow schemas."""

    @classmethod
    def decode(cls, data: bytes) -> pa.Schema:
        """Decode the incoming bytes to a PyArrow schema.

        :param data: The encoded schema.
        """
        if data == b"**undecodable**":
            raise ValueError("Cannot decode data")

        decoded = base64.b64decode(data)

        try:
            with pa.ipc.open_stream(decoded) as reader:
                return reader.schema
        except OSError as exc:
            message = f"Cannot decode schema: {decoded!r}"
            logger.exception(message)
            raise ValueError(message) from exc

    @classmethod
    def encode(cls, value: pa.Schema) -> str:  # type: ignore[override]
        """Encode the PyArrow schema to byte string."""
        return base64.b64encode(value.serialize()).decode("utf-8")


EncodedSchema = Annotated[bytes, EncodedBytes(encoder=SchemaEncoder)]


class ModelConfig(BaseModel):
    """This dataclass stores the configuration
    related to a model."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra="allow",
    )

    input_schema: EncodedSchema
    output_schema: EncodedSchema


class ConfiguredModelVersion(BaseModel, Generic[SupportedFrameworks]):
    """This dataclass stores data related to
    a configured model."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="allow",
        protected_namespaces=(),
    )

    model_version: ModelVersion[SupportedFrameworks]
    config: ModelConfig


class ModelPackagingUpdateEvent(BaseModel, Generic[SupportedFrameworks]):
    """This dataclass stores data related to a model packaging update.
    For more info see: https://github.com/WallarooLabs/platform/blob/main/conductor/wallsvc/src/models/event.rs#L30.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="allow",
    )

    model: ConfiguredModelVersion[SupportedFrameworks]


class ModelConversionUpdateEvent(
    ModelPackagingUpdateEvent[SupportedFrameworks], Generic[SupportedFrameworks]
):
    """This dataclass stores data related to a ModelUpdate event.
    It can be used either for model conversion or model packaging messages.
    For more info see: https://github.com/WallarooLabs/platform/blob/main/conductor/wallsvc/src/models/event.rs#L79
    respectively."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="allow",
    )

    orig_path: Optional[str] = None
