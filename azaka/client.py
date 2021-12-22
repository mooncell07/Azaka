from __future__ import annotations

import os
import ssl

os.environ["PYTHONASYNCIODEBUG"] = "1"

import asyncio
import inspect
import typing as t

from .connection import Transporter
from .context import Context
from .objects import DBStats
from .tools import Cache, make_command, make_repr

__all__ = ("Client",)


class Client:

    __slots__ = ("_cache", "_transporter", "ctx")

    def __init__(
        self,
        *,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        loop: t.Optional[asyncio.BaseEventLoop] = None,
        ssl_context: t.Optional[ssl.SSLContext] = None,
        cache_size: int = 50
    ) -> None:
        self.ctx = Context(
            username=username, password=password, loop=loop, ssl_context=ssl_context
        )
        self._cache = Cache(maxsize=cache_size)
        self._transporter: Transporter = Transporter(self.ctx)

    @property
    def is_closing(self) -> bool:
        return (
            self._transporter.transport is None
            or self._transporter.transport.is_closing()  # noqa
        )

    def register(
        self,
        coro: t.Callable[..., t.Any],
    ) -> None:
        create_task = self.ctx.loop.create_task

        if inspect.iscoroutinefunction(coro):
            create_task(coro(self.ctx))
        else:
            raise TypeError("Callback must be a coroutine.") from None

    def start(self) -> None:
        data = {
            "protocol": self.ctx.PROTOCOL_VERSION,
            "client": self.ctx.CLIENT_NAME,
            "clientver": self.ctx.CLIENT_VERSION,
        }

        username = self.ctx.username
        password = self.ctx.password
        if (username is not None) and (password is not None):
            data["username"] = username
            data["password"] = password

        command = make_command("login", args=data)
        self._transporter.start(command)

    async def fetch_dbstats(self, update=False) -> DBStats:
        command = make_command("dbstats")

        if command not in self._cache or update is True:
            future = self.ctx.loop.create_future()
            await self._transporter.inject(command, future)

            result = DBStats(await future)
            self._cache.put(command, result)
        else:
            result = self._cache[command]
        return result

    async def get_extra_info(self, *args, default=None) -> t.Optional[t.List[t.Any]]:
        return await self._transporter.get_extra_info(args, default=default)

    def close(self) -> None:
        self.ctx.loop.stop()

    def __repr__(self) -> str:
        return make_repr(self)

    def __str__(self) -> str:
        return make_repr(self)
