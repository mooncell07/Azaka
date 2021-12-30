from __future__ import annotations

import os
import ssl

os.environ["PYTHONASYNCIODEBUG"] = "1"

import asyncio
import inspect
import typing as t

from .commands import Command, Presets
from .connection import Connector
from .context import Context
from .exceptions import AzakaException
from .interface import Interface
from .objects import DBStats, VisualNovel, Release
from .tools import Cache

__all__ = ("Client",)


class Client(Presets):

    __slots__ = ("_cache", "_connector", "_models", "ctx")

    def __init__(
        self,
        *,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        loop: t.Optional[asyncio.BaseEventLoop] = None,
        ssl_context: t.Optional[ssl.SSLContext] = None,
        cache_size: int = 50,
    ) -> None:
        self.ctx: Context = Context(
            username=username, password=password, loop=loop, ssl_context=ssl_context
        )
        self._cache: Cache = Cache(maxsize=cache_size)
        self._connector: Connector = Connector(self.ctx)
        self._models = {"vn": VisualNovel, "release": Release}

        super().__init__(self)

    @property
    def is_closing(self) -> bool:
        return (
            self._connector.transport is None
            or self._connector.transport.is_closing()  # noqa
        )

    def register(
        self,
        coro: t.Callable[..., t.Any],
    ) -> None:
        if inspect.iscoroutinefunction(coro):
            self.ctx.loop.create_task(
                self._connector.handle_user_exceptions(coro(self.ctx))
            )
        else:
            raise TypeError("Callback must be a coroutine.") from None

    def on_error(self, func: t.Callable[..., t.Any]) -> None:
        self._connector.error_listener(func)

    def start(self, *, token: t.Optional[t.Union[bool, str]] = None) -> None:
        data = {
            "protocol": self.ctx.PROTOCOL_VERSION,
            "client": self.ctx.CLIENT_NAME,
            "clientver": self.ctx.CLIENT_VERSION,
        }

        username = self.ctx.username
        password = self.ctx.password
        if username is not None:
            data["username"] = username

            if isinstance(token, str):
                data["sessiontoken"] = token
                self._cache.put(Command("token"), token)

            elif password is not None:
                data["password"] = password

                if token is True:
                    data["createsession"] = True
            else:
                raise AzakaException(
                    "Either password or session token is required when using username."
                )

        command = Command("login", **data)
        try:
            self._connector.start(command.create())
        except asyncio.CancelledError:
            pass

    async def logout(self) -> None:
        command = Command("logout")
        token = self._cache.get("token")

        if token is not None:
            await self._connector.inject(command, None)
            self.stop()

        else:
            raise AzakaException(
                "logout() is only supported when a session token is available."
            )

    async def fetch_token(self) -> str:
        command = Command("token")

        if command not in self._cache:
            future = self.ctx.loop.create_future()
            await self._connector.inject(command, future)

            result = (await future).result()
            self._cache.put(command, result)

        else:
            result = self._cache[command]
        return result

    async def dbstats(self, update=False) -> DBStats:
        command = Command("dbstats")

        if command not in self._cache or update is True:
            future = self.ctx.loop.create_future()
            await self._connector.inject(command, future)

            result = DBStats(await future)
            self._cache.put(command, result)
        else:
            result = self._cache[command]
        return result

    async def get(self, interface: Interface) -> t.Any:
        command = Command("get", interface=interface)

        future = self.ctx.loop.create_future()
        await self._connector.inject(command, future)

        result = await future
        return [self._models[interface._type.value](data) for data in result["items"]]

    async def get_extra_info(self, *args, default=None) -> t.Optional[t.List[t.Any]]:
        return await self._connector.get_extra_info(args, default=default)

    def stop(self) -> None:
        self.ctx.loop.stop()
