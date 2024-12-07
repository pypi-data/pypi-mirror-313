import json
from enum import Enum
from typing import Any, Dict, Optional

import wallaroo.config as wallaroo_config


class Architecture(str, Enum):
    """
    An Enum to represent the supported processor architecture.
    """

    X86 = "x86"
    ARM = "arm"
    Power10 = "power10"

    @classmethod
    def default(cls) -> "Architecture":
        _config = wallaroo_config._config
        if _config is None or _config.get("default_arch") is None:
            raise Exception(
                "Your Client hasn't been properly set up. Try creating it again or contact Wallaroo support."
            )
        return Architecture(_config["default_arch"])

    def __str__(self) -> str:
        return str(self.value)


class Acceleration(str, Enum):
    """
    An Enum to represent the supported acceleration options.
    """

    _None = "none"
    CUDA = "cuda"
    Jetson = "jetson"
    OpenVINO = "openvino"

    @classmethod
    def default(cls) -> "Acceleration":
        return cls._None

    def __str__(self) -> str:
        return str(self.value)

    def is_applicable(self, arch: Architecture) -> bool:
        if self == Acceleration._None:
            return True
        if self == Acceleration.CUDA:
            return True
        if self == Acceleration.Jetson:
            return arch == Architecture.ARM
        if self == Acceleration.OpenVINO:
            return arch == Architecture.X86
        return False


class EngineConfig:
    """Wraps an engine config."""

    # NOTE: refer to /conductor/helm/payloads/deployment-manager/helm/default-values and
    # /conductor/helm/payloads/deployment-manager/helm/orchestra-deployment.yaml
    # for reasonable defaults
    def __init__(
        self,
        cpus: int,
        gpus: Optional[int] = 0,
        inference_channel_size: Optional[int] = None,
        model_concurrency: Optional[int] = None,
        pipeline_config_directory: Optional[str] = None,
        model_config_directory: Optional[str] = None,
        model_directory: Optional[str] = None,
        audit_logging: bool = False,
        arch: Architecture = Architecture.X86,
        accel: Acceleration = Acceleration._None,
    ) -> None:
        self._cpus = cpus
        self._gpus = gpus
        self._inference_channel_size = (
            inference_channel_size if inference_channel_size else 10000
        )
        self._model_concurrency = model_concurrency if model_concurrency else 1
        self._audit_logging = audit_logging
        self._pipeline_config_directory = pipeline_config_directory
        self._model_config_directory = model_config_directory
        self._model_directory = model_directory
        self._arch = arch
        self._accel = accel

    # TODO: Is there a better way to keep this in sync with our helm chart?
    def _to_dict(self) -> Dict[str, Any]:
        """Generate a dictionary representation for use to coversion to json or yaml"""
        config: Dict[str, Any] = {
            "cpus": self._cpus,
            "gpus": self._gpus,
            "arch": str(self._arch),
            "accel": str(self._accel),
        }
        if self._inference_channel_size:
            config["inference_channel_size"] = self._inference_channel_size
        if self._model_concurrency:
            config["model_server"] = {"model_concurrency": self._model_concurrency}
        config["audit_logging"] = {"enabled": self._audit_logging}
        return config

    def to_json(self) -> str:
        """Returns a json representation of this object"""
        return json.dumps(self._to_dict())


class InvalidAccelerationError(Exception):
    """Raised when the specified acceleration is incompatible with the given platform architecture.

    :param str accel: acceleration
    :param str arch: architecture
    """

    def __init__(self, accel: Acceleration, arch: Architecture):
        super().__init__(
            "The specified model architecture configuration is not available. "
            "Please try this operation again using a different configuration "
            "or contact support@wallaroo.ai for questions or help."
        )
