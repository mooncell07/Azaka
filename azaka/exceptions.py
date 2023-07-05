__all__ = ("AzakaException", "EXMAP")


STATUS_INVALID_REQUEST_BODY = 400
STATUS_INVALID_AUTH_TOKEN = 401
STATUS_NOT_FOUND = 404
STATUS_THROTTLED = 429
STATUS_SERVER_ERROR = 500
STATUS_SERVER_DOWN = 502


class AzakaException(Exception):
    __slots__ = ("msg", "status_code")

    def __init__(self, msg: str, status_code: int) -> None:
        self.msg = msg
        self.status_code = status_code
        super().__init__(msg)


class InvalidRequestBodyError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg, STATUS_INVALID_REQUEST_BODY)


class InvalidAuthTokenError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg, STATUS_INVALID_AUTH_TOKEN)


class NotFoundError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg, STATUS_NOT_FOUND)


class ThrottledError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg, STATUS_THROTTLED)


class ServerError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg, STATUS_SERVER_ERROR)


class ServerDownError(AzakaException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg, STATUS_SERVER_DOWN)


EXMAP = {
    STATUS_INVALID_REQUEST_BODY: InvalidRequestBodyError,
    STATUS_INVALID_AUTH_TOKEN: InvalidAuthTokenError,
    STATUS_NOT_FOUND: NotFoundError,
    STATUS_THROTTLED: ThrottledError,
    STATUS_SERVER_ERROR: ServerError,
    STATUS_SERVER_DOWN: ServerDownError,
}
