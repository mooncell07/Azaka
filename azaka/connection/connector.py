from __future__ import annotations

import asyncio
import contextlib
import logging
import traceback
import typing as t

from ..commands import Command
from ..exceptions import BrokenConnectorError
from ..tools import QueueControlMixin
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
        self.sessiontoken: asyncio.Future = ctx.loop.create_future()

        super().__init__()
        self.protocol_factory = Protocol(self)

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
        finally:
            self.ctx.loop.stop()

    def start(self, command: bytes) -> None:
        task = self.ctx.loop.create_task(self.connect(command))
        task._log_destroy_pending = False  # type: ignore

        try:
            self.ctx.loop.run_forever()
        except KeyboardInterrupt:
            pass

        finally:
            self.shutdown()
            self.ctx.loop.close()

            logger.debug("SHUTDOWN COMPLETED.")

        if task.done() or task.cancelled():
            with contextlib.suppress(asyncio.CancelledError):
                if task.exception() is not None:
                    raise task.exception() from None  # type: ignore

    async def inject(
        self, command: Command, future: t.Optional[asyncio.Future]
    ) -> None:
        await self.on_connect.wait()

        transport = self.transport
        processed_command = command.create()

        if transport is None:
            raise BrokenConnectorError("Transport not available.")

        elif command.name == "token" and future is not None:
            future.set_result(self.sessiontoken)

        else:
            transport.write(processed_command)
            await self.drain()

            logger.info(f"DISPATCHED TRANSPORTER WITH {repr(processed_command)}")

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

        logger.debug("SHUTDOWN STARTED.")

        self.ctx.loop.run_until_complete(self.ctx.loop.shutdown_default_executor())
        self.ctx.loop.run_until_complete(self.ctx.loop.shutdown_asyncgens())

        for task in asyncio.all_tasks(loop=self.ctx.loop):
            task.cancel()

            try:
                self.ctx.loop.run_until_complete(task)
            except asyncio.CancelledError:
                pass

        if self.transport is not None:
            self.transport.close()

        self.ctx.loop.call_soon_threadsafe(self.ctx.loop.stop)

    async def handle_user_exceptions(self, coro: t.Coroutine) -> None:
        try:
            await coro
        except Exception as e:
            tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            logger.error(f"IGNORING EXCEPTION IN {coro.__qualname__}:\n{tb}")
