from __future__ import annotations

import asyncio
import logging
import typing as t
import ssl
from .protocol import Protocol
from ..tools.queuecontrolmixin import QueueControlMixin

__all__ = ("Transporter",)
logger = logging.getLogger(__name__)


class Transporter(QueueControlMixin):

    PROTOCOL_VERSION = 1

    __slots__ = (
        "_transport",
        "loop",
    )

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:

        self._transport: t.Optional[asyncio.transports.Transport] = None
        self.loop = loop

        super().__init__()

    async def start(self, credential: bytes) -> None:
        protocol_factory = Protocol(credential, self.on_connect, self.on_disconnect)
        protocol_factory.listener = self.listener
        addr = "api.vndb.org"
        port = 19535
        cert = self.ssl_handler()

        try:
            self._transport, _ = await self.loop.create_connection(  # type: ignore
                protocol_factory=lambda: protocol_factory,
                host=addr,
                port=port,
                ssl=cert,
            )
            await self.on_disconnect.wait()
            self.shutdown_handler()

        except Exception as e:
            self.shutdown_handler()
            raise e

    async def inject(self, command: bytes, condition: asyncio.Condition) -> None:
        await self.on_connect.wait()

        transport = self._transport
        if transport is not None:
            transport.write(command)

            logger.info(f"DISPATCHED TRANSPORTER WITH {repr(command)}")
            self.condition_queue.put_nowait(condition)

    def is_closing(self) -> bool:
        return self._transport is None or self._transport.is_closing()

    async def get_extra_info(
        self, args: t.Tuple[str, ...], *, default: t.Optional[t.Any] = None
    ) -> t.Optional[t.List[t.Any]]:
        await self.on_connect.wait()
        transport = self._transport

        if transport is not None:
            return [transport.get_extra_info(arg, default=default) for arg in args]

        return None

    def ssl_handler(self) -> ssl.SSLContext:
        sslctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        sslctx.load_default_certs()

        return sslctx

    def shutdown_handler(self) -> None:
        for task in asyncio.all_tasks(loop=self.loop):
            task.cancel()

        self.on_disconnect.set()

        if self._transport is not None:
            self._transport.close()

        if self.loop.is_running:
            self.loop.stop()
