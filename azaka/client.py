import os

os.environ["PYTHONASYNCIODEBUG"] = "1"

import asyncio
import typing as t

from .connection import Transporter
from .objects import DBStats
from .workers import Cache, make_command, make_repr

__all__ = ("Client",)
CLIENT_NAME = "Azaka"
CLIENT_VERSION = "0.1.0"


class Client:

    __slots__ = ("_transporter", "cache", "loop", "password", "username")

    def __init__(
        self,
        *,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        cache_size: int = 50,
        loop: t.Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        self.loop = (
            loop
            if isinstance(loop, asyncio.AbstractEventLoop) and not loop.is_closed()
            else self._acquire_loop()
        )
        self._transporter: Transporter = Transporter(self.loop)
        self.cache = Cache(maxsize=cache_size)
        self.password = password
        self.username = username

    def _acquire_loop(self) -> asyncio.AbstractEventLoop:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop

    async def fetch_dbstats(self) -> DBStats:
        command = make_command("dbstats")

        if command not in self.cache:
            condition = asyncio.Condition()

            async with condition:
                await self._transporter.inject(command, condition)
                await condition.acquire()

            result = DBStats(self._transporter.queue.get_nowait())
            self.cache.put(command, result)
        else:
            result = self.cache[command]
        return result

    def start(self) -> None:
        data = {
            "protocol": self._transporter.PROTOCOL_VERSION,
            "client": CLIENT_NAME,
            "clientver": CLIENT_VERSION,
        }

        username = self.username
        password = self.password
        if (username is not None) and (password is not None):
            data["username"] = username
            data["password"] = password

        command = make_command("login", args=data)
        self.loop.create_task(self._transporter.start(command))

        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(
                asyncio.gather(
                    self.loop.shutdown_asyncgens(),
                    self.loop.shutdown_default_executor(),
                )
            )
            self._transporter.shutdown_handler()
            self.loop.close()

    async def get_extra_info(self, *args, default=None) -> t.List[t.Any]:
        return await self._transporter.get_extra_info(args, default=default)

    def close(self) -> None:
        self._transporter.shutdown_handler()

    @property
    def is_closing(self) -> bool:
        return self._transporter.is_closing()

    def __repr__(self) -> str:
        return make_repr(self)
