import typing as t
from .tools import ErrorType, ResponseType


__all__ = (
    "AzakaException",
    "InvalidResponseTypeError",
    "OperationNotSupportedError",
    "BrokenConnectorError",
    "CommandError",
    "CommandFilterError",
    "MissingFieldError",
    "BadFieldError",
    "AuthorizationError",
    "UnknownGetTypeError",
    "UnknownGetFlagError",
    "CommandSyntaxError",
    "ThrottledError",
    "InterfaceError",
)


class AzakaException(Exception):

    __slots__ = ("message",)

    def __init__(self, msg: str) -> None:
        self.message = msg
        super().__init__(msg)


class InvalidResponseTypeError(AzakaException):

    __slots__ = ("type",)

    def __init__(self, type_: t.Optional[ResponseType], msg: str) -> None:
        self.type = type_
        super().__init__(msg)


class OperationNotSupportedError(AzakaException):
    __slots__ = ()

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class BrokenConnectorError(AzakaException):
    __slots__ = ()

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class CommandError(AzakaException):

    __slots__ = ("id",)

    def __init__(self, **kwargs: t.Any) -> None:
        self.id: ErrorType = ErrorType(kwargs["id"])
        super().__init__(kwargs["msg"])


class CommandFilterError(CommandError):

    __slots__ = ("op", "value", "field")

    def __init__(self, **kwargs: t.Any) -> None:

        self.field: str = kwargs["field"]
        self.op: str = kwargs["op"]
        self.value: t.Any = kwargs["value"]

        super().__init__(**kwargs)

    @property
    def expression(self) -> str:
        return f"({self.field} {self.op} {self.value})"


class MissingFieldError(CommandError):

    __slots__ = ("field",)

    def __init__(self, **kwargs: t.Any) -> None:
        self.field: str = kwargs["field"]
        super().__init__(**kwargs)


class BadFieldError(CommandError):

    __slots__ = ("field",)

    def __init__(self, **kwargs: t.Any) -> None:
        self.field: str = kwargs["field"]
        super().__init__(**kwargs)


class AuthorizationError(CommandError):

    __slots__ = ()

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)


class UnknownGetTypeError(CommandError):

    __slots__ = ()

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)


class UnknownGetFlagError(CommandError):

    __slots__ = ("flag",)

    def __init__(self, **kwargs: t.Any) -> None:
        self.flag: str = kwargs["flag"]
        super().__init__(**kwargs)


class CommandSyntaxError(CommandError):

    __slots__ = ()

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)


class ThrottledError(CommandError):

    __slots__ = ("type", "minwait", "fullwait")

    def __init__(self, **kwargs: t.Any) -> None:
        self.type: str = kwargs["type"]
        self.minwait: float = kwargs["minwait"]
        self.fullwait: float = kwargs["fullwait"]

        super().__init__(**kwargs)


class InterfaceError(AzakaException):

    __slots__ = ()

    def __init__(self, msg: str) -> None:
        super().__init__(msg)
