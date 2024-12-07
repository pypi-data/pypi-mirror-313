"""This module contains the dataclasses related to
a NATS message."""

from pathlib import Path
from typing import Any, Dict, Generic

import pyarrow as pa
from pydantic import BaseModel, ConfigDict

from pydata_util.nats.event import ModelConversionUpdateEvent, ModelPackagingUpdateEvent
from pydata_util.types import SupportedFrameworks


class NATSMessage(BaseModel):
    """This dataclass stores data related to
    a NATS message."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="allow",
    )

    data: Any

    @property
    def model_input_schema(self) -> pa.Schema:
        """Return the input schema of the model."""
        return self.data.model.config.input_schema

    @property
    def model_file_name(self) -> Path:
        """Return the file name where the model is located."""
        return self.data.model.model_version.file_info.file_name

    @property
    def model_framework(self) -> str:
        """Return the framework of the model."""
        return self.data.model.model_version.conversion.framework

    @property
    def model_name(self) -> str:
        """Return the name of the model."""
        return self.data.model.model_version.name

    @property
    def model_output_schema(self) -> pa.Schema:
        """Return the output schema of the model."""
        return self.data.model.config.output_schema

    @property
    def model_settings(self) -> Dict[str, Any]:
        """Return the settings of the model."""
        return self.data.model.model_version.conversion.settings

    @property
    def model_sha(self) -> str:
        """Return the sha of the model file."""
        return self.data.model.model_version.file_info.sha

    @property
    def workspace_id(self) -> int:
        """Return the workspace ID of the model."""
        return self.data.model.model_version.workspace_id


class NATSPackagingMessage(NATSMessage, Generic[SupportedFrameworks]):
    """This dataclass stores data related to
    a NATS message for model packaging."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="allow",
    )

    data: ModelPackagingUpdateEvent[SupportedFrameworks]


class NATSConversionMessage(NATSMessage, Generic[SupportedFrameworks]):
    """This dataclass stores data related to
    a NATS message for model conversion."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="allow",
    )

    data: ModelConversionUpdateEvent[SupportedFrameworks]
