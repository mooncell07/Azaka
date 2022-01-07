import asyncio
import ssl
import typing as t

try:
    import uvloop

    UV = True
except ModuleNotFoundError:
    UV = False

__all__ = ("Context",)


class Context:
    """
    A context holding all the necessary info and objects to connect to the VNDB API.
    This same object is given to the 0th arg of every coroutine function decorated
    with [Client.register](../client#azaka.client.Client.register).

    Attributes:
        ADDR (str): The address of the VNDB API.
        PORT (int): The port to which client should connect. Azaka only supports `19535` as it provides TLS support.
        PROTOCOL_VERSION (int): The version of the protocol this client is using. Currently, this is `1`.
        CLIENT_NAME (str): The name of the client. Defaults to `Azaka`.
        CLIENT_VERSION (str): The version of the client.

    """

    ADDR = "api.vndb.org"
    PORT = 19535
    PROTOCOL_VERSION = 1

    CLIENT_NAME = "Azaka"
    CLIENT_VERSION = "0.1.0a4"

    __slots__ = ("loop", "password", "ssl_context", "username")

    def __init__(
        self,
        *,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        loop: t.Optional[asyncio.AbstractEventLoop] = None,
        ssl_context: t.Optional[ssl.SSLContext] = None
    ) -> None:
        """
        Context Constructor. This is where all the necessary info and object are stored.

        Args:
            username: Username to use for logging in.
            password: Password to use for logging in.
            loop: The [asyncio.AbstractEventLoop][] subclass to use.
            ssl_context: The [ssl.SSLContext][] to use. If not provided, a default context will be used.
        """
        self.username = username
        self.password = password

        self.loop = (
            loop if isinstance(loop, asyncio.BaseEventLoop) else self._get_event_loop()
        )
        self.ssl_context = ssl_context or self._get_ssl_context()

    def _get_ssl_context(self) -> ssl.SSLContext:
        sslctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        sslctx.load_default_certs()

        return sslctx

    def _get_event_loop(self) -> asyncio.AbstractEventLoop:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            if UV:
                loop = uvloop.new_event_loop()
            else:
                loop = asyncio.new_event_loop()

            asyncio.set_event_loop(loop)
        return loop
