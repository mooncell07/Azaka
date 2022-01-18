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
    """
    Base class for all Azaka exceptions.

    Attributes:
        message (str): The error message.
    """

    __slots__ = ("message",)

    def __init__(self, msg: str) -> None:
        self.message = msg
        super().__init__(msg)


class InvalidResponseTypeError(AzakaException):
    """
    An exception that is raised when the response type is invalid.

    Attributes:
        type (str): The response type API returned.
    """

    __slots__ = ("type",)

    def __init__(self, type_: t.Optional[ResponseType], msg: str) -> None:
        self.type = type_
        super().__init__(msg)


class OperationNotSupportedError(AzakaException):
    """
    An exception that is raised when an operation is not supported between the field and value.
    """

    __slots__ = ()

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class BrokenConnectorError(AzakaException):
    """
    An exception that is raised when the connector is broken/not available.
    """

    __slots__ = ()

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class CommandError(AzakaException):
    """
    Base class for all command errors.

    Attributes:
        id (ErrorType): The error ID. (An [enum][] of [ErrorType](../public/enums.md#azaka.tools.enums.ErrorType))
    """

    __slots__ = ("id",)

    def __init__(self, **kwargs: t.Any) -> None:
        self.id: ErrorType = ErrorType(kwargs["id"])
        super().__init__(kwargs["msg"])


class CommandFilterError(CommandError):
    """
    An exception that is raised when a command filter is invalid.

    Attributes:
        field (str): The field used in the filter.
        op (str): The operator.
        value (str): The value.
    """

    __slots__ = ("op", "value", "field")

    def __init__(self, **kwargs: t.Any) -> None:

        self.field: str = kwargs["field"]
        self.op: str = kwargs["op"]
        self.value: t.Any = kwargs["value"]

        super().__init__(**kwargs)

    @property
    def expression(self) -> str:
        """
        Returns a string representation of the filter.
        """
        return f"({self.field} {self.op} {self.value})"


class MissingFieldError(CommandError):
    """
    An exception that is raised when a field is missing.

    Attributes:
        field (str): The missing field.
    """

    __slots__ = ("field",)

    def __init__(self, **kwargs: t.Any) -> None:
        self.field: str = kwargs["field"]
        super().__init__(**kwargs)


class BadFieldError(CommandError):
    """
    An exception that is raised when a field is invalid.

    Attributes:
        field (str): The invalid field.
    """

    __slots__ = ("field",)

    def __init__(self, **kwargs: t.Any) -> None:
        self.field: str = kwargs["field"]
        super().__init__(**kwargs)


class AuthorizationError(CommandError):
    """
    An exception that is raised when the credentials to login are invalid.
    """

    __slots__ = ()

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)


class UnknownGetTypeError(CommandError):
    """
    An exception that is raised when the type of a get command is unknown.
    """

    __slots__ = ()

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)


class UnknownGetFlagError(CommandError):

    """
    An exception that is raised when the flag of a get command is unknown.

    Attributes:
        flag (str): The unknown flag.
    """

    __slots__ = ("flag",)

    def __init__(self, **kwargs: t.Any) -> None:
        self.flag: str = kwargs["flag"]
        super().__init__(**kwargs)


class CommandSyntaxError(CommandError):
    """
    An exception that is raised when the syntax of a command is invalid.
    """

    __slots__ = ()

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)


class ThrottledError(CommandError):
    """
    An exception that is raised when the user is getting rate limited.

    Attributes:
        type (str): The type of the rate limit.
        minwait (float): The minimum wait time.
        fullwait (float): The full wait time.
    """

    __slots__ = ("type", "minwait", "fullwait")

    def __init__(self, **kwargs: t.Any) -> None:
        self.type: str = kwargs["type"]
        self.minwait: float = kwargs["minwait"]
        self.fullwait: float = kwargs["fullwait"]

        super().__init__(**kwargs)


class InterfaceError(AzakaException):
    """
    An exception that is raised when the interface is broken.
    """

    __slots__ = ()

    def __init__(self, msg: str) -> None:
        super().__init__(msg)
