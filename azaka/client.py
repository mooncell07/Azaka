import asyncio
import typing as t
from .websocket.transporter import Transporter
from .workers.transformer import make_command

__all__ = ("Client",)

CLIENT_NAME = "Azaka"
CLIENT_VERSION = "0.1.0"


class Client:

    __slots__ = ("loop", "password", "transporter", "username")

    def __init__(
        self,
        *,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        loop: t.Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        self.loop = (
            loop
            if isinstance(loop, asyncio.AbstractEventLoop) and not loop.is_closed()
            else self._acquire_loop()
        )
        self.transporter: Transporter = Transporter(self.loop)
        self.username = username
        self.password = password

    def _acquire_loop(self) -> asyncio.AbstractEventLoop:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop

    async def dbstats(self) -> str:
        command = make_command("dbstats")
        condition = asyncio.Condition()

        async with condition:
            await self.transporter.inject(command, condition)
            await condition.acquire()

        return self.transporter.queue.get_nowait()

    def start(self) -> None:
        data = dict(
            protocol=self.transporter.PROTOCOL_VERSION,
            client=CLIENT_NAME,
            clientver=CLIENT_VERSION,
        )
        if None not in (self.username, self.password):
            data.update({"username": self.username, "password": self.password})

        command = make_command("login", args=data)
        self.loop.create_task(self.transporter.start(command))
        try:
            self.loop.run_forever()
        finally:
            self.loop.stop()

    def close(self) -> None:
        self.transporter.shutdown_handler()
