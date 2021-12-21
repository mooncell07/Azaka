import os
import ssl

os.environ["PYTHONASYNCIODEBUG"] = "1"

import asyncio
import inspect
import typing as t

from .config import Config
from .connection import Transporter
from .objects import DBStats
from .tools import Cache, make_command, make_repr

__all__ = ("Client",)


class Client:

    __slots__ = ("_transporter", "_cache", "cfg")

    def __init__(
        self,
        *,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        _cache_size: int = 50,
        loop: t.Optional[asyncio.AbstractEventLoop] = None,
        ssl_context: t.Optional[ssl.SSLContext] = None
    ) -> None:
        self.cfg = Config(
            username=username, password=password, loop=loop, ssl_context=ssl_context
        )
        self._cache = Cache(maxsize=_cache_size)
        self._transporter: Transporter = Transporter(self.cfg)

    @property
    def is_closing(self) -> bool:
        return (
            self._transporter.transport is None
            or self._transporter.transport.is_closing()
        )

    def register(
        self,
        coro: t.Callable[..., t.Any],
    ):
        create_task = self.cfg.loop.create_task

        if inspect.iscoroutinefunction(coro):
            create_task(coro(self))
        else:
            raise TypeError("Callback must be a coroutine.") from None

    def start(self) -> None:
        data = {
            "protocol": self.cfg.PROTOCOL_VERSION,
            "client": self.cfg.CLIENT_NAME,
            "clientver": self.cfg.CLIENT_VERSION,
        }

        username = self.cfg.username
        password = self.cfg.password
        if (username is not None) and (password is not None):
            data["username"] = username
            data["password"] = password

        command = make_command("login", args=data)
        self._transporter.start(command)

    async def fetch_dbstats(self, update=False) -> DBStats:
        command = make_command("dbstats")

        if command not in self._cache or update is True:
            future = self.cfg.loop.create_future()
            await self._transporter.inject(command, future)

            result = DBStats(await future)
            self._cache.put(command, result)
        else:
            result = self._cache[command]
        return result

    async def get_extra_info(self, *args, default=None) -> t.Optional[t.List[t.Any]]:
        return await self._transporter.get_extra_info(args, default=default)

    def close(self) -> None:
        self.cfg.loop.stop()

    def __repr__(self) -> str:
        return make_repr(self)

    def __str__(self) -> str:
        return make_repr(self)
