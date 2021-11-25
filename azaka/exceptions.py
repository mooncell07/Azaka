__all__ = ("AzakaException", "InvalidResponseTypeError")


class AzakaException(Exception):

    __slots__ = ("message",)

    def __init__(self, msg) -> None:
        self.message = msg
        super().__init__(msg)


class InvalidResponseTypeError(AzakaException):

    __slots__ = ("type",)

    def __init__(self, type, msg) -> None:
        self.type = type
        super().__init__(msg)
