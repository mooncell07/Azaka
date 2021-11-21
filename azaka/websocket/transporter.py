from __future__ import annotations

import asyncio
import logging
import queue
import typing as t
from .protocol import Protocol

if t.TYPE_CHECKING:
    from ..workers.transformer import Transformer


__all__ = ("Transporter",)


class Transporter:

    PROTOCOL_VERSION = 1

    __slots__ = ('_transport', 'conditions', 'logger', 'loop', 'on_connect', 'on_disconnect', 'queue')

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self.on_connect: asyncio.Event = asyncio.Event()
        self.on_disconnect: asyncio.Event = asyncio.Event()
        self.logger: logging.Logger = logging.getLogger(__name__)

        self._transport: t.Optional[asyncio.transports.Transport] = None
        self.queue: queue.Queue = queue.Queue()
        self.conditions: queue.Queue = queue.Queue()

    def notify(self, msg: str) -> None:
        self.queue.put_nowait(msg)
        self.conditions.get_nowait().release()

    async def start(self, credential: Transformer) -> None:
        command = credential.command_formation("login")
        protocol_factory = Protocol(command, self.on_connect, self.on_disconnect)
        protocol_factory.subscriber = self.notify

        addr =  "api.vndb.org"
        port =  19534
        try:
            self._transport, _ = await self.loop.create_connection(  # type: ignore
                    lambda: protocol_factory,
                    addr,
                    port,
                )
        except Exception as e:
            await self.loop.shutdown_asyncgens()
            await self.loop.shutdown_default_executor()
            self.logger.error(e)
        else:
            await self.on_disconnect.wait()
        finally:
            self.shutdown_handler()

    async def inject(self, command: Transformer, condition: asyncio.Condition) -> None:
        await self.on_connect.wait()
        cmd = command.to_bytes() + b"\x04"

        if self._transport:
            self._transport.write(cmd)

            self.logger.info(f"DISPATCHED TRANSPORTER WITH {repr(cmd)}")
            self.conditions.put_nowait(condition)

    def shutdown_handler(self) -> None:
        for task in asyncio.all_tasks(loop=self.loop):
            task.cancel()
        if self._transport:
            self._transport.close()
        self.loop.stop()
