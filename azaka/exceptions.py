import typing as t
from .tools import ErrorType


__all__ = (
    "AzakaException",
    "InvalidResponseTypeError",
    "OperationNotSupportedError",
    "BrokenConnectorError",
    "CommandError",
    "CommandFilterError",
)


class AzakaException(Exception):

    __slots__ = ("message",)

    def __init__(self, msg: str) -> None:
        self.message = msg
        super().__init__(msg)


class InvalidResponseTypeError(AzakaException):

    __slots__ = ("type",)

    def __init__(self, type_, msg: str) -> None:
        self.type = type_
        super().__init__(msg)


class OperationNotSupportedError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class BrokenConnectorError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class CommandError(AzakaException):

    __all__ = ("id",)

    def __init__(self, **kwargs: t.Any) -> None:
        self.id = ErrorType(kwargs["id"])

        super().__init__(kwargs["msg"])


class CommandFilterError(CommandError):

    __slots__ = ("op", "value", "field")

    def __init__(self, **kwargs: t.Any) -> None:

        self.op = kwargs.get("op")
        self.value = kwargs.get("value")
        self.field = kwargs.get("field")

        super().__init__(**kwargs)
