from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from ..client import Client
    from ..interface import Interface
    from ..objects import BaseObject

__all__ = ("Paginator",)


class Paginator:
    def __init__(self, client: Client, interface: Interface) -> None:
        self._client = client
        self._interface = interface
        self.current_page: t.Optional[t.Iterable[BaseObject]] = None
        self.current_page_num: int = 0
        self.more: bool = True

    async def next_page(self) -> t.Optional[t.Iterable[BaseObject]]:
        if self.more:
            self.current_page_num += 1
            return await self.generate()
        return None

    async def previous_page(self) -> t.Optional[t.Iterable[BaseObject]]:
        if self.current_page_num > 1:
            self.current_page_num -= 1
            return await self.generate()
        return None

    def __aiter__(self) -> Paginator:
        return self

    async def __anext__(self) -> t.Iterable[BaseObject]:
        data = await self.next_page()

        if not data:
            raise ValueError

        return data

    async def generate(self) -> t.Optional[t.Iterable[BaseObject]]:
        self._interface.add_option(page=self.current_page_num)
        data = await self._client.get(self._interface, metadata=True)

        if isinstance(data, tuple):
            self.current_page, self.more, _ = data
            return data[0]
        return None
