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

    __slots__ = ("transport", "cfg", "protocol_factory")

    def __init__(self, cfg) -> None:

        self.transport: t.Optional[asyncio.transports.Transport] = None
        self.cfg = cfg

        super().__init__()
        self.protocol_factory = Protocol(
            self.listener, self.on_connect, self.on_disconnect
        )

    async def connect(self, command: bytes) -> None:

        self.protocol_factory.command = command
        try:
            self.transport, _ = await self.cfg.loop.create_connection(  # type: ignore
                protocol_factory=lambda: self.protocol_factory,
                host=self.cfg.ADDR,
                port=self.cfg.PORT,
                ssl=self.cfg.ssl_context,
            )
            await self.on_disconnect.wait()
        except Exception:
            raise
        finally:
            self.cfg.loop.stop()

    def start(self, command):
        task = self.cfg.loop.create_task(self.connect(command))
        task._log_destroy_pending = False  # type: ignore

        try:
            self.cfg.loop.run_forever()
        finally:
            self.shutdown()
            self.cfg.loop.close()

        if task.done() or task.cancelled():
            if isinstance(task.exception(), BaseException):
                raise task.exception() from None  # type: ignore

    async def inject(self, command: bytes, future: asyncio.Future) -> None:
        await self.on_connect.wait()

        transport = self.transport
        if transport is not None:
            transport.write(command)

            logger.info(f"DISPATCHED TRANSPORTER WITH {repr(command)}")
            self.future_queue.put_nowait(future)

    async def get_extra_info(
        self, args: t.Tuple[str, ...], *, default: t.Optional[t.Any] = None
    ) -> t.Optional[t.List[t.Any]]:
        await self.on_connect.wait()
        transport = self.transport

        if transport is not None:
            return [transport.get_extra_info(arg, default=default) for arg in args]

        return None

    def shutdown(self) -> None:
        self.on_disconnect.set()
        for task in asyncio.all_tasks(loop=self.cfg.loop):
            task.cancel()

        if self.transport is not None:
            self.transport.close()
