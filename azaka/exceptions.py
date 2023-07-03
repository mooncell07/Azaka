import enum

__all__ = ("AzakaException", "EXMAP")


class AzakaException(Exception):
    def __init__(self, msg: str, status_code: int) -> None:
        self.msg = msg
        self.status_code = status_code
        super().__init__(msg)


class InvalidRequestBodyError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg, 400)


class InvalidAuthTokenError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg, 401)


class NotFoundError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg, 404)


class ThrottledError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg, 429)


class ServerError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg, 500)


class ServerDownError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg, 502)


EXMAP = {
    400: InvalidRequestBodyError,
    401: InvalidAuthTokenError,
    404: NotFoundError,
    429: ThrottledError,
    500: ServerError,
    502: ServerDownError,
}
