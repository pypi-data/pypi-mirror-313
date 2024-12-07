"""This module features the NATSMessageFactory for creating
concrete NATSMessage subclass instances."""

import logging
from typing import Any

from pydata_util.exceptions import SubclassTypeNotExistError
from pydata_util.nats.nats_message import NATSConversionMessage, NATSPackagingMessage
from pydata_util.types import SupportedNATSMessages

logger = logging.getLogger(__name__)


class NATSMessageFactory:
    """This class implements the AbstractFactory interface
    for creating concrete NATSMessage subclass instances."""

    @property
    def subclass_creators(self) -> dict:
        """Returns a dictionary with keys corresponding to subclass names and values
        corresponding to the subclass creator functions."""
        return {
            SupportedNATSMessages.CONVERSION: NATSConversionMessage,
            SupportedNATSMessages.PACKAGING: NATSPackagingMessage,
        }

    def create(self, subclass_type: str, **kwargs) -> Any:
        """Create an instance of a concrete subclass.

        :param subclass_type: The type of the subclass to be created.
        :param kwargs: The keyword arguments to be passed to the subclass creator
        function.

        :return: An instance of a concrete subclass.
        """
        try:
            subclass_creator = self.subclass_creators[subclass_type]
        except KeyError as exception:
            message = f"The subclass type {subclass_type} is not supported."
            logger.exception(message)
            raise SubclassTypeNotExistError(message) from exception

        supported_frameworks = kwargs.get("supported_frameworks")
        _ = kwargs.pop("supported_frameworks")
        subclass = subclass_creator[supported_frameworks](**kwargs)
        return subclass
