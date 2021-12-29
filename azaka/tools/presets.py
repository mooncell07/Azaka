from __future__ import annotations

import typing as t

from ..commands import BoolOProxy
from ..interface import Interface
from .enums import Flags, Type

__all__ = ("Presets",)


class Presets:
    def __init__(
        self, get: t.Callable[[Interface], t.Coroutine[t.Any, t.Any, t.Any]]
    ) -> None:
        self.get = get

    async def get_basic_vn_info(self, item: BoolOProxy):
        with Interface(type=Type.VN, flags=(Flags.BASIC,)) as interface:
            interface.set_condition(item)

        return await self.get(interface)

    async def get_detailed_vn_info(self, item: BoolOProxy):
        with Interface(type=Type.VN, flags=(Flags.DETAILS,)) as interface:
            interface.set_condition(item)

        return await self.get(interface)

    async def get_vn_stats(self, item: BoolOProxy):
        with Interface(type=Type.VN, flags=(Flags.STATS,)) as interface:
            interface.set_condition(item)

        return await self.get(interface)
