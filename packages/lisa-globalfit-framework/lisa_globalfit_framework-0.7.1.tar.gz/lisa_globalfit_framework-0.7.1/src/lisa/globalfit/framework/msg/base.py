from dataclasses import dataclass
from pickle import PicklingError, UnpicklingError, dumps, loads
from typing import Self

from lisa.globalfit.framework.exceptions import DeserializationError, SerializationError


@dataclass
class MessageBase:
    """Base class for event messages exchanged within the framework."""

    def encode(self) -> bytes:
        """Encode the message for communication on the message bus.

        Implementations should return a binary representation of the message, using
        Python pickle serialization protocol.

        :return: Encoded message.
        """
        try:
            return dumps(self)
        except PicklingError as err:
            msg = f"could not encode message: {err}"
            raise SerializationError(msg) from err

    @classmethod
    def decode(cls, data: bytes) -> Self:
        """Decode a message from its binary representation.

        :param data: Binary content of the encoded message.

        :return: Decoded message.
        """
        # TODO: We would like to use a proper serialization format eventually.
        # However, protobuf does not support Numpy arrays natively, so it might
        # need a bit of work.
        try:
            return loads(data)  # noqa: S301
        except UnpicklingError as err:
            msg = f"could not decode message: {err}"
            raise DeserializationError(msg) from err
