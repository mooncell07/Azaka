import asyncio
import ssl

import typing as t

__all__ = ("Context",)


class Context:

    ADDR = "api.vndb.org"
    PORT = 19535
    PROTOCOL_VERSION = 1

    CLIENT_NAME = "Azaka"
    CLIENT_VERSION = "0.1.0a2"

    __slots__ = ("loop", "password", "ssl_context", "username")

    def __init__(
        self,
        *,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        loop: t.Optional[asyncio.BaseEventLoop] = None,
        ssl_context: t.Optional[ssl.SSLContext] = None
    ) -> None:
        self.username = username
        self.password = password

        self.loop = loop or self._get_event_loop()
        self.ssl_context = ssl_context or self._get_ssl_context()

    def _get_ssl_context(self) -> ssl.SSLContext:
        sslctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        sslctx.load_default_certs()

        return sslctx

    def _get_event_loop(self) -> asyncio.AbstractEventLoop:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop
