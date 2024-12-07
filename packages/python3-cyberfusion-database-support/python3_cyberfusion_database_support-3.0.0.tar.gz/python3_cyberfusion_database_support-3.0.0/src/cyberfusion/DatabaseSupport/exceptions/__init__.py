"""Generic exceptions."""

from typing import Any


class InvalidInputError(Exception):
    """Invalid input."""

    def __init__(self, input_: Any):
        """Set attributes."""
        self.input_ = input_


class ServerNotSupportedError(Exception):
    """Server not supported."""

    pass


class PasswordMissingError(Exception):
    """Password missing."""

    pass
