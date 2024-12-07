"""This module features the implementation of the InferenceBuilder
for generating Inference subclass instances from a given AutoInferenceConfig.
"""

from abc import abstractmethod

from mac.config.python_step import PythonStepConfig
from mac.inference.inference import Inference


class InferenceBuilder:
    """This class implements the InferenceBuilder implementation
    for generating Inference subclass instances given an AutoInferenceConfig.

    Attributes:
        - inference_factory: An InferenceFactory object.
    """

    @property
    @abstractmethod
    def inference(self) -> Inference:
        """Returns an Inference subclass instance.
        This specifies the Inference instance to be used
        by create() to build additionally needed components."""

    @abstractmethod
    def create(self, config: PythonStepConfig) -> Inference:
        """Creates an Inference subclass and assigns a model to it.

        :param config: Inference configuration.

        :return: Inference subclass
        """
