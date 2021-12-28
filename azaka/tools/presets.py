from __future__ import annotations

import typing as t

from ..commands import BoolOProxy
from .enums import Flags, Type

__all__ = ("Presets",)

if t.TYPE_CHECKING:
    from ..interface import Interface


class Presets:
    def __init__(
        self,
        get: t.Callable[[Interface], t.Coroutine[t.Any, t.Any, t.Any]],
        clean_interface: t.Callable,
    ) -> None:
        self.get = get
        self.interface = clean_interface

    async def get_basic_vn_info(self, item: BoolOProxy):
        with self.interface(type=Type.VN, flags=(Flags.BASIC,)) as interface:
            interface.set_condition(item)

        return await self.get(interface)

    async def get_detailed_vn_info(self, item: BoolOProxy):
        with self.interface(type=Type.VN, flags=(Flags.DETAILS,)) as interface:
            interface.set_condition(item)

        return await self.get(interface)

    async def get_vn_stats(self, item: BoolOProxy):
        with self.interface(type=Type.VN, flags=(Flags.STATS,)) as interface:
            interface.set_condition(item)

        return await self.get(interface)
