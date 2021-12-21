import asyncio
import ssl

__all__ = ("Config",)


class Config:

    ADDR = "api.vndb.org"
    PORT = 19535
    PROTOCOL_VERSION = 1

    CLIENT_NAME = "Azaka"
    CLIENT_VERSION = "0.1.0a1"

    __slots__ = ("username", "password", "ssl_context", "loop")

    def __init__(self, *, username, password, ssl_context, loop) -> None:
        self.username = username
        self.password = password
        self.ssl_context = ssl_context or self.get_ssl_context()
        self.loop = loop or self.get_event_loop()

    def get_ssl_context(self) -> ssl.SSLContext:
        sslctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        sslctx.load_default_certs()
        return sslctx

    def get_event_loop(self) -> asyncio.AbstractEventLoop:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop
