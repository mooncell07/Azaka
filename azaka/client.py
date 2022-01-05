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
from .objects import (
    VN,
    BaseObject,
    Character,
    DBStats,
    Producer,
    Quote,
    Release,
    Staff,
    User,
    UlistLabels,
    Ulist,
)
from .tools import Cache, Type, ResponseType, Paginator

__all__ = ("Client",)


def _model_selector(type: Type) -> t.Type[BaseObject]:
    models = {
        "vn": VN,
        "release": Release,
        "producer": Producer,
        "character": Character,
        "staff": Staff,
        "quote": Quote,
        "user": User,
        "ulist-labels": UlistLabels,
        "ulist": Ulist,
    }
    return models[type.value]


class Client(Presets):

    __slots__ = ("_cache", "_connector", "ctx")

    def __init__(
        self,
        *,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        loop: t.Optional[asyncio.AbstractEventLoop] = None,
        ssl_context: t.Optional[ssl.SSLContext] = None,
        cache_size: int = 50,
    ) -> None:
        """
        Client Constructor. This is the main entry point for the library.

        Args:
            username: Username to use for logging in.
            password: Password to use for logging in.
            loop: The [asyncio.AbstractEventLoop][] subclass to use.
            ssl_context: The [ssl.SSLContext][] to use. If not provided, a default context will be used.
            cache_size: Size of the internal cache of data. Defaults to 50.

        Info:
            If you have uvloop installed, then the lib will by default use uvloop's event loop.

        Note:
            A password or session token should be provided if passing an username.
        """
        self.ctx: Context = Context(
            username=username, password=password, loop=loop, ssl_context=ssl_context
        )
        self._cache: Cache = Cache(maxsize=cache_size)
        self._connector: Connector = Connector(self.ctx)

        super().__init__(self)

    @property
    def is_closing(self) -> bool:
        """
        Returns:
            True if the client's [asyncio.Transport][] is closing/closed.
        """
        return (
            self._connector.transport is None
            or self._connector.transport.is_closing()  # noqa
        )

    def register(
        self,
        coro: t.Callable[..., t.Any],
    ) -> None:
        """
        Register a coroutine to be called when client is ready to issue commands.

        Args:
            coro: The coroutine to call.

        Info:
            The coroutine must be a function that takes a single argument of type [Context][].

        Example:
            ```py
            @register
            async def my_coro(ctx):
                ...
            ```
        """

        if inspect.iscoroutinefunction(coro):
            self.ctx.loop.create_task(
                self._connector.handle_user_exceptions(coro(self.ctx))
            )
        else:
            raise TypeError("Callback must be a coroutine.") from None

    def on_error(self, func: t.Callable[..., t.Any]) -> None:
        """
        Register a function to be called when an error occurs.

        Args:
            func: The function to call.

        Info:
            The function must take a single argument of type [AzakaException][].

        Example:
            ```py
            @on_error
            def my_error_handler(error):
                ...
            ```
        """
        self._connector.error_listener(func)

    def start(self, *, token: t.Optional[t.Union[bool, str]] = None) -> None:
        """
        Start the client and attempt to login.

        Args:
            token: The token to use. If not provided, password will be used if username is provided.

        Raises:
            AzakaException: Raises when a username was passed but not a password or session token.

        Note:
            For fetching a token, the argument should be set to `True` and username and password must be provided.
        """
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
        """
        logout and close the client's connection. Only works when client was connected using a session token.

        Raises:
            AzakaException: Raises when there is no session token available.
        """
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

    async def dbstats(self, update: bool = False) -> DBStats:
        """
        Get the VNDB database statistics.

        Args:
            update: If set to `True`, the client makes an api call to get data else it returns cached data.

        Returns:
            [DBStats][]
        """
        command = Command("dbstats")

        if command not in self._cache or update is True:
            future = self.ctx.loop.create_future()
            await self._connector.inject(command, future)

            result = DBStats(await future)
            self._cache.put(command, result)
        else:
            result = self._cache[command]
        return result

    async def get(
        self, interface: Interface, paginate=False, **kwargs: bool
    ) -> t.Union[t.Iterable[BaseObject], Paginator]:
        """
        Issue a `get` command to the API.

        Args:
            interface: The [Interface][] to use.
            paginate: If set to `True`, the client will return a [Paginator][] instance.

        Returns:
            [list][] of [BaseObject][] if paginate is set to `False` else [Paginator][] if paginate is set to `True`.
        """
        if paginate:
            return Paginator(self, interface)

        command = Command("get", interface=interface)

        future = self.ctx.loop.create_future()
        await self._connector.inject(command, future)

        result = await future
        obj = [_model_selector(interface._type)(data) for data in result["items"]]

        if kwargs.get("metadata"):
            return (obj, result["more"], result["num"])  # type: ignore

        return obj

    async def set_ulist(self, id: int, **kwargs: str) -> ResponseType:
        """
        Issue a `set` command to the API. This method is used to set userlist data.

        Args:
            id: The item id.
            **kwargs: The data to set.

        Info:
            The following keys are supported for kwargs:

                - notes

                - started

                - finished

                - vote

                - labels

        Returns:
            [ResponseType][]
        """
        command = Command(f"set ulist {id}", **kwargs)

        future = self.ctx.loop.create_future()
        await self._connector.inject(command, future)
        result = await future

        return result

    async def get_extra_info(
        self, *args: str, default: t.Optional[bool] = None
    ) -> t.Optional[t.List[t.Any]]:
        """
        Get extra information about the client's internal [asyncio.Transport][].

        Args:
            args: The extra information to get.
            default: The default value to return if the information is not available.

        Returns:
            [list][] of extra information.
        """
        return await self._connector.get_extra_info(args, default=default)

    def stop(self) -> None:
        """
        Stops the event loop and closes the connection.
        """
        self.ctx.loop.stop()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} connected={not self.is_closing}>"
