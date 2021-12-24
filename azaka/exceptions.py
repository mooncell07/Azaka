__all__ = ("AzakaException", "InvalidResponseTypeError", "OperationNotSupportedError")


class AzakaException(Exception):

    __slots__ = ("message",)

    def __init__(self, msg) -> None:
        self.message = msg
        super().__init__(msg)


class InvalidResponseTypeError(AzakaException):

    __slots__ = ("type",)

    def __init__(self, type_, msg) -> None:
        self.type = type_
        super().__init__(msg)


class OperationNotSupportedError(AzakaException):
    def __init__(self, msg) -> None:
        super().__init__(msg)


class BrokenConnectorError(AzakaException):
    def __init__(self, msg) -> None:
        super().__init__(msg)
