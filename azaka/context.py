from __future__ import annotations

import asyncio
import ssl
import typing as t

from .interface import Interface
from .commands import (
    UserCondition,
    VNCondition,
    BoolOProxy,
    ReleaseCondition,
    QuoteCondition,
    CharacterCondition,
    StaffCondition,
    UlistCondition,
    UlistLabelsCondition,
    ProducerCondition,
)
from .tools import Flags
from .objects import (
    VN,
    Character,
    Producer,
    Quote,
    Release,
    Staff,
    User,
    UlistLabels,
    Ulist,
)

try:
    import uvloop  # type: ignore

    UV = True
except ModuleNotFoundError:
    UV = False

__all__ = ("Context",)

if t.TYPE_CHECKING:
    from .client import Client


class Context:
    """
    A context holding all the necessary info and objects to connect and interact with the VNDB API.
    This same object is given to the 0th arg of every coroutine function decorated
    with [Client.register](../client#azaka.client.Client.register).

    Attributes:
        ADDR (str): The address of the VNDB API.
        PORT (int): The port to which client should connect. Azaka only supports `19535` as it provides TLS support.
        PROTOCOL_VERSION (int): The version of the protocol this client is using. Currently, this is `1`.
        CLIENT_NAME (str): The name of the client. Defaults to `Azaka`.
        CLIENT_VERSION (str): The version of the client.
    """

    ADDR: t.Final[str] = "api.vndb.org"
    PORT: t.Final[int] = 19535
    PROTOCOL_VERSION: t.Final[int] = 1

    CLIENT_NAME: t.Final[str] = "Azaka"
    CLIENT_VERSION: t.Final[str] = "0.1.0"

    __slots__ = (
        "client",
        "loop",
        "password",
        "ssl_context",
        "username",
        "vn",
        "character",
        "quote",
        "user",
        "ulist",
        "ulist_labels",
        "release",
        "staff",
        "producer",
    )

    def __init__(
        self,
        client: Client,
        *,
        username: t.Optional[str] = None,
        password: t.Optional[str] = None,
        loop: t.Optional[asyncio.AbstractEventLoop] = None,
        ssl_context: t.Optional[ssl.SSLContext] = None
    ) -> None:
        """
        Context Constructor. This is where all the necessary info and objects are stored.

        Attributes:
            client: The client object that is using this context.
            username: Username to use for logging in.
            password: Password to use for logging in.
            loop: The [asyncio.AbstractEventLoop][] subclass to use.
            ssl_context: The [ssl.SSLContext][] to use. If not provided, a default context will be used.

        ## COMMAND TYPE ATTRIBUTES
        Below are the attributes which are meant to be used as
        argument for the `type` parameter of [Interface.__init__](./interface.md#azaka.interface.Interface.__init__).

        Attributes:
            vn: The `vn` command type.
            character: The `character` command type.
            producer: The `producer` command type.
            release: The `release` command type.
            staff: The `staff` command type.
            quote: The `quote` command type.
            user: The `user` command type.
            ulist_labels: The `ulist-labels` command type.
            ulist: The `ulist` command type.

        Warning:
            This object is not meant to be constructed by users.

        """
        self.client = client
        self.username = username
        self.password = password

        self.loop = (
            loop if isinstance(loop, asyncio.BaseEventLoop) else self._get_event_loop()
        )
        self.ssl_context = ssl_context or self._get_ssl_context()

        self.vn: t.Type[VN] = VN
        self.character: t.Type[Character] = Character
        self.producer: t.Type[Producer] = Producer
        self.release: t.Type[Release] = Release
        self.staff: t.Type[Staff] = Staff
        self.quote: t.Type[Quote] = Quote
        self.user: t.Type[User] = User
        self.ulist_labels: t.Type[UlistLabels] = UlistLabels
        self.ulist: t.Type[Ulist] = Ulist

    def _get_ssl_context(self) -> ssl.SSLContext:
        sslctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        sslctx.load_default_certs()

        return sslctx

    def _get_event_loop(self) -> asyncio.AbstractEventLoop:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            if UV:
                loop = uvloop.new_event_loop()
            else:
                loop = asyncio.new_event_loop()

            asyncio.set_event_loop(loop)
        return loop

    async def get_vn(
        self,
        predicate: t.Callable[[t.Type[VNCondition]], BoolOProxy],
        *,
        details: bool = False
    ) -> t.Optional[t.List[VN]]:
        """
        Get VNs matching the predicate. By default this will use [BASIC](./enums.md#azaka.tools.enums.Flags) flag.
        If you want to append [DETAILS](./enums.md#azaka.tools.enums.Flags) flag,
        you need to pass `details=True` as an argument.

        Args:
            predicate: A callable that takes a
                       [VNCondition](../public/condition.md#azaka.commands.condition.VNCondition)
                       and returns a [BoolOProxy](../internals/commands/proxy.md#azaka.commands.proxy.BoolOProxy).
            details: Whether to get the basic and detailed info of the vn.

        Returns:
            A [list][] of [VN](./objects/vn.md#azaka.objects.vn.VN) matching the predicate.

        Example:
            ```python
            @register
            async def main(ctx):
                await ctx.get_vn(lambda VN: VN.ID == 11)
            ```

        All the `get_x` methods in this class can be used in same way as `get_vn`.

        Info:
            This and all `get_x` methods in this class are an abstraction over
            [Client.get](../client#azaka.client.Client.get)
            and provide lesser flexibility.
        """
        flags = (
            (
                Flags.BASIC,
                Flags.DETAILS,
            )
            if details
            else (Flags.BASIC,)
        )

        with Interface(type=self.vn, flags=flags) as interface:
            interface.set_condition(predicate(VNCondition))

        result = await self.client.get(interface)
        if isinstance(result, list):
            return result

        return None

    async def get_staff(
        self,
        predicate: t.Callable[[t.Type[StaffCondition]], BoolOProxy],
        *,
        details: bool = False
    ) -> t.Optional[t.List[Staff]]:
        """
        Get Staff matching the predicate. [info and usage](./context.md#azaka.context.Context.get_vn)

        Args:
            predicate: A callable that takes a
                       [StaffCondition](../public/condition.md#azaka.commands.condition.StaffCondition)
                       and returns a [BoolOProxy](../internals/commands/proxy.md#azaka.commands.proxy.BoolOProxy).

        Returns:
            A [list][] of [Staff](./objects/staff.md#azaka.objects.staff.Staff)s matching the predicate.
        """
        flags = (
            (
                Flags.BASIC,
                Flags.DETAILS,
            )
            if details
            else (Flags.BASIC,)
        )

        with Interface(type=self.staff, flags=flags) as interface:
            interface.set_condition(predicate(StaffCondition))

        result = await self.client.get(interface)
        if isinstance(result, list):
            return result

        return None

    async def get_release(
        self,
        predicate: t.Callable[[t.Type[ReleaseCondition]], BoolOProxy],
        *,
        details: bool = False
    ) -> t.Optional[t.List[Release]]:
        """
        Get Releases matching the predicate. [info and usage](./context.md#azaka.context.Context.get_vn)

        Args:
            predicate: A callable that takes a
                       [ReleaseCondition](../public/condition.md#azaka.commands.condition.ReleaseCondition) and returns
                       a [BoolOProxy](../internals/commands/proxy.md#azaka.commands.proxy.BoolOProxy).
            details: Whether to get the basic and detailed info of the release.

        Returns:
            A [list][] of [Release](./objects/release.md#azaka.objects.release.Release)s matching the predicate.
        """

        flags = (
            (
                Flags.BASIC,
                Flags.DETAILS,
            )
            if details
            else (Flags.BASIC,)
        )

        with Interface(type=self.release, flags=flags) as interface:
            interface.set_condition(predicate(ReleaseCondition))

        result = await self.client.get(interface)
        if isinstance(result, list):
            return result

        return None

    async def get_character(
        self,
        predicate: t.Callable[[t.Type[CharacterCondition]], BoolOProxy],
        *,
        details: bool = False
    ) -> t.Optional[t.List[Character]]:
        """
        Get Characters matching the predicate. [info and usage](./context.md#azaka.context.Context.get_vn)

        Args:
            predicate: A callable that takes a
                       [CharacterCondition](../public/condition.md#azaka.commands.condition.CharacterCondition) and
                       returns a [BoolOProxy](../internals/commands/proxy.md#azaka.commands.proxy.BoolOProxy).
            details: Whether to get the basic and detailed info of the character.

        Returns:
            A [list][] of [Character](./objects/character.md#azaka.objects.character.Character)s matching the predicate.
        """
        flags = (
            (
                Flags.BASIC,
                Flags.DETAILS,
            )
            if details
            else (Flags.BASIC,)
        )

        with Interface(type=self.character, flags=flags) as interface:
            interface.set_condition(predicate(CharacterCondition))

        result = await self.client.get(interface)
        if isinstance(result, list):
            return result

        return None

    async def get_producer(
        self,
        predicate: t.Callable[[t.Type[ProducerCondition]], BoolOProxy],
        *,
        details: bool = False
    ) -> t.Optional[t.List[Producer]]:
        """
        Get Producers matching the predicate. [info and usage](./context.md#azaka.context.Context.get_vn)

        Args:
            predicate: A callable that takes a
                       [ProducerCondition](../public/condition.md#azaka.commands.condition.ProducerCondition)
                       and returns a [BoolOProxy](../internals/commands/proxy.md#azaka.commands.proxy.BoolOProxy).
            details: Whether to get the basic and detailed info of the producer.

        Returns:
            A [list][] of [Producer](./objects/producer.md#azaka.objects.producer.Producer)s matching the predicate.
        """
        flags = (
            (
                Flags.BASIC,
                Flags.DETAILS,
            )
            if details
            else (Flags.BASIC,)
        )

        with Interface(type=self.producer, flags=flags) as interface:
            interface.set_condition(predicate(ProducerCondition))

        result = await self.client.get(interface)
        if isinstance(result, list):
            return result

        return None

    async def get_quote(
        self, predicate: t.Callable[[t.Type[QuoteCondition]], BoolOProxy]
    ) -> t.Optional[t.List[Quote]]:
        """
        Get Quotes matching the predicate. [info and usage](./context.md#azaka.context.Context.get_vn)

        Args:
            predicate: A callable that takes a
                       [QuoteCondition](../public/condition.md#azaka.commands.condition.QuoteCondition) and returns a
                       [BoolOProxy](../internals/commands/proxy.md#azaka.commands.proxy.BoolOProxy).

        Returns:
            A [list][] of [Quote](./objects/quote.md#azaka.objects.quote.Quote)s matching the predicate.
        """
        with Interface(type=self.quote, flags=(Flags.BASIC,)) as interface:
            interface.set_condition(predicate(QuoteCondition))

        result = await self.client.get(interface)
        if isinstance(result, list):
            return result

        return None

    async def get_user(
        self, predicate: t.Callable[[t.Type[UserCondition]], BoolOProxy]
    ) -> t.Optional[t.List[User]]:
        """
        Get Users matching the predicate. [info and usage](./context.md#azaka.context.Context.get_vn)

        Args:
            predicate: A callable that takes a
                       [UserCondition](../public/condition.md#azaka.commands.condition.UserCondition) and returns a
                       [BoolOProxy](../internals/commands/proxy.md#azaka.commands.proxy.BoolOProxy).

        Returns:
            A [list][] of [User](./objects/user.md#azaka.objects.user.User)s matching the predicate.
        """
        with Interface(type=self.user, flags=(Flags.BASIC,)) as interface:
            interface.set_condition(predicate(UserCondition))

        result = await self.client.get(interface)
        if isinstance(result, list):
            return result

        return None

    async def get_ulist(
        self, predicate: t.Callable[[t.Type[UlistCondition]], BoolOProxy]
    ) -> t.Optional[t.List[Ulist]]:
        """
        Get Ulists matching the predicate. [info and usage](./context.md#azaka.context.Context.get_vn)

        Args:
            predicate: A callable that takes a
                       [UlistCondition](../public/condition.md#azaka.commands.condition.UlistCondition) and returns a
                       [BoolOProxy](../internals/commands/proxy.md#azaka.commands.proxy.BoolOProxy).

        Returns:
            A [list][] of [Ulist](./objects/ulist.md#azaka.objects.ulist.Ulist)s matching the predicate.
        """
        with Interface(type=self.ulist, flags=(Flags.BASIC,)) as interface:
            interface.set_condition(predicate(UlistCondition))

        result = await self.client.get(interface)
        if isinstance(result, list):
            return result

        return None

    async def get_ulist_labels(
        self, predicate: t.Callable[[t.Type[UlistLabelsCondition]], BoolOProxy]
    ) -> t.Optional[t.List[UlistLabels]]:
        """
        Get Ulist Labels matching the predicate. [info and usage](./context.md#azaka.context.Context.get_vn)

        Args:
            predicate: A callable that takes a
                       [UlistLabelsCondition](../public/condition.md#azaka.commands.condition.UlistLabelsCondition) and
                       returns a [BoolOProxy](../internals/commands/proxy.md#azaka.commands.proxy.BoolOProxy).

        Returns:
            A [list][] of
            [UlistLabels](./objects/ulistlabels.md#azaka.objects.ulistlabels.UlistLabels)
            matching the predicate.
        """
        with Interface(type=self.ulist_labels, flags=(Flags.BASIC,)) as interface:
            interface.set_condition(predicate(UlistLabelsCondition))

        result = await self.client.get(interface)
        if isinstance(result, list):
            return result

        return None
