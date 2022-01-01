from __future__ import annotations

import typing as t

from ..interface import Interface
from ..tools.enums import Flags, Type
from .proxy import BoolOProxy

if t.TYPE_CHECKING:
    from ..client import Client
    from ..objects import BaseObject

__all__ = ("Presets",)


class Presets:

    __slots__ = ("client",)

    def __init__(self, client: Client) -> None:
        self.client = client

    async def get_basic_vn_info(self, item: BoolOProxy) -> t.Iterable[BaseObject]:
        with Interface(type=Type.VN, flags=(Flags.BASIC,)) as interface:
            interface.set_condition(item)

        return await self.client.get(interface)

    async def get_detailed_vn_info(self, item: BoolOProxy) -> t.Iterable[BaseObject]:
        with Interface(type=Type.VN, flags=(Flags.DETAILS,)) as interface:
            interface.set_condition(item)

        return await self.client.get(interface)

    async def get_vn_stats(self, item: BoolOProxy) -> t.Iterable[BaseObject]:
        with Interface(type=Type.VN, flags=(Flags.STATS,)) as interface:
            interface.set_condition(item)

        return await self.client.get(interface)

    async def get_user(self, item: BoolOProxy) -> t.Iterable[BaseObject]:
        with Interface(type=Type.USER, flags=(Flags.BASIC,)) as interface:
            interface.set_condition(item)

        return await self.client.get(interface)
