from __future__ import annotations

import asyncio
import logging
import typing as t

from ..tools.queuecontrolmixin import QueueControlMixin
from ..exceptions import BrokenConnectorError
from .protocol import Protocol

if t.TYPE_CHECKING:
    from ..context import Context

__all__ = ("Connector",)
logger = logging.getLogger(__name__)


class Connector(QueueControlMixin):

    __slots__ = ("ctx", "protocol_factory", "sessiontoken", "transport")

    def __init__(self, ctx: Context) -> None:

        self.ctx = ctx
        self.transport: t.Optional[asyncio.transports.Transport] = None
        self.sessiontoken = ctx.loop.create_future()

        super().__init__()
        self.protocol_factory = Protocol(
            self.sessiontoken, self.listener, self.on_connect, self.on_disconnect
        )

    async def connect(self, command: bytes) -> None:
        self.protocol_factory.command = command

        try:
            self.transport, _ = await asyncio.wait_for(
                self.ctx.loop.create_connection(  # type: ignore
                    protocol_factory=lambda: self.protocol_factory,
                    host=self.ctx.ADDR,
                    port=self.ctx.PORT,
                    ssl=self.ctx.ssl_context,
                ),
                timeout=5,
            )
            await self.on_disconnect.wait()

        except Exception as e:
            raise e from None

        finally:
            self.ctx.loop.stop()

    def start(self, command: bytes) -> None:
        task = self.ctx.loop.create_task(self.connect(command))
        task._log_destroy_pending = False  # type: ignore

        try:
            self.ctx.loop.run_forever()
        finally:
            self.shutdown()
            self.ctx.loop.close()

        if task.done() or task.cancelled():
            if isinstance(task.exception(), BaseException):
                raise task.exception() from None  # type: ignore

    async def inject(
        self, command: t.Union[bytes, str], future: t.Optional[asyncio.Future]
    ) -> None:
        await self.on_connect.wait()
        transport = self.transport

        if transport is None:
            raise BrokenConnectorError("Transport not available.")

        else:
            if command == "token" and future is not None:
                future.set_result(self.sessiontoken)

            else:
                transport.write(command)
                logger.info(f"DISPATCHED TRANSPORTER WITH {repr(command)}")

                if future is not None:
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
        for task in asyncio.all_tasks(loop=self.ctx.loop):
            task.cancel()

        if self.transport is not None:
            self.transport.close()
