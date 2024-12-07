"""This module contains the AutoInferenceConfig class."""

import logging
from typing import Union

from pydantic import ConfigDict, DirectoryPath, FilePath, model_validator

from mac.config.python_step.python_step_config import PythonStepConfig
from mac.types import SupportedFrameworks

logger = logging.getLogger(__name__)

available_frameworks = (
    SupportedFrameworks.KERAS,
    SupportedFrameworks.SKLEARN,
    SupportedFrameworks.PYTORCH,
    SupportedFrameworks.XGBOOST,
    SupportedFrameworks.HUGGING_FACE,
)


class AutoInferenceConfig(PythonStepConfig):
    """This class defines configuration parameters for an automated
    Inference object.

    Attributes:
        - framework: The framework of the model to be loaded, that should match
            `available_frameworks`.
        - model_path: The path to the model.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, extra="forbid", protected_namespaces=()
    )

    model_path: Union[FilePath, DirectoryPath]

    @model_validator(mode="before")
    @classmethod
    def raise_error_if_framework_invalid(cls, data):
        """Checks that the framework is supported."""
        if data["framework"] not in available_frameworks:
            message = f"`framework` should be one of `{available_frameworks}`."
            logger.error(message)
            raise ValueError(message)
        return data
