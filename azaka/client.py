from __future__ import annotations

import os
import ssl

os.environ["PYTHONASYNCIODEBUG"] = "1"

import asyncio
import inspect
import typing as t

from .commands import Command
from .connection import Connector
from .context import Context
from .exceptions import AzakaException
from .interface import Interface, SETInterface
from .objects import DBStats
from .tools import Cache, ResponseType, Paginator

__all__ = ("Client",)


class Client:

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
            self,
            username=username,
            password=password,
            loop=loop,
            ssl_context=ssl_context,
        )
        self._cache: Cache = Cache(maxsize=cache_size)
        self._connector: Connector = Connector(self.ctx)

    @property
    def is_closing(self) -> bool:
        """
        Returns:
            `True` if the client's [asyncio.Transport][] is closing/closed.
        """
        return (
            self._connector.transport is None
            or self._connector.transport.is_closing()  # noqa
        )

    def register(
        self,
        coro: t.Callable[..., t.Coroutine[t.Any, t.Any, t.Any]],
        *args: t.Any,
        **kwargs: t.Any,
    ) -> None:
        """
        Register a coroutine-function to be called when client is ready to issue commands.

        Args:
            coro: The coroutine to call.

        Info:
            The coroutine-function must take a single argument of type [Context](./context.md#azaka.context.Context).

        Example:
            ```py
            @register
            async def my_coro(ctx):
                ...
            ```
        """

        if inspect.iscoroutinefunction(coro):
            self.ctx.loop.create_task(
                self._connector.handle_user_exceptions(coro(self.ctx, *args, **kwargs))
            )
        else:
            raise TypeError("Callback must be a coroutine.") from None

    def on_error(self, func: t.Callable) -> None:
        """
        Register a function to be called when an error occurs.

        Args:
            func: The function to call.

        Info:
            The function must take a single argument of type
            [AzakaException](../public/exceptions.md#azaka.exceptions.AzakaException).

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
        self._connector.start(command.create())

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
        """
        Fetches the session token.
        Only works when `token` arg of [Client.start](./#azaka.client.Client.start) was set to `True`.

        Returns:
            The session token.
        """
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
            [DBStats](./objects/dbstats.md#azaka.objects.DBStats)
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
    ) -> t.Union[t.Iterable[t.Any], Paginator]:
        """
        Issue a `get` command to the API. This method provides a centralised way to fetch data from the VNDB API.

        Args:
            interface: The [Interface](./interface.md#azaka.interface.Interface) to use.
            paginate: If set to `True`, it returns a [Paginator](./paginator.md#azaka.tools.paginator.Paginator).

        Returns:
            [list][] of subclass of [BaseObject](../public/objects/baseobject.md#azaka.objects.BaseObject)
            if paginate is set to `False` else [Paginator](./paginator.md#azaka.tools.paginator.Paginator)

        Info:
            This is a low level generic method.
            Use the `get_x` methods of [Context](./context.md#azaka.context.Context)
            instead if you want to do basic queries.

        Example:
            ```py
            @register
            async def get_vn_animes(ctx):
                with Interface(type=ctx.vn, flags=(Flags.ANIMES,)) as interface:
                    VN = interface.condition()
                    interface.set_condition(VN.ID == 123)
                await ctx.get(interface)
            ```

        Detailed info about this method can be found in the [tutorial]().
        """
        if paginate:
            return Paginator(self, interface)

        command = Command("get", interface=interface)

        future = self.ctx.loop.create_future()
        await self._connector.inject(command, future)

        result = await future
        obj = [interface._type(data) for data in result["items"]]

        if kwargs.get("metadata"):
            return (obj, result["more"], result["num"])  # type: ignore

        return obj

    async def set_ulist(self, interface: SETInterface) -> ResponseType:
        """
        Issue a `set` command to the API. This method is used to set userlist data.

        Args:
            interface: The [SETInterface](./interface.md#azaka.interface.SETInterface) to use.
        Returns:
            [ResponseType](./enums.md#azaka.tools.enums.ResponseType)
        """
        command = Command(f"set ulist {interface.id}", **interface._kwargs)

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
