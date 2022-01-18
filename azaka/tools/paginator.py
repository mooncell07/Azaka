from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from ..client import Client
    from ..interface import Interface
    from ..objects import BaseObject

__all__ = ("Paginator",)


class Paginator:
    """
    A Paginator returned by the [Client.get](../client#azaka.client.Client.get) method
    used to provide async and stateful iteration over the results of `get` command (s).

    Attributes:
        current_page (t.Optiona[t.Iterable[BaseObject]]): The current page of results.
        current_page_num (int): The current page number.
        more (bool): If there are more pages to fetch.
    """

    __slots__ = ("_client", "_interface", "current_page", "current_page_num", "more")

    def __init__(self, client: Client, interface: Interface) -> None:
        self._client = client
        self._interface = interface
        self.current_page: t.Optional[t.Iterable[BaseObject]] = None
        self.current_page_num: int = 0
        self.more: bool = True

    async def next(self) -> t.Optional[t.Iterable[BaseObject]]:
        """
        Fetches the next page of results.

        Returns:
            The next page of results.
        """
        if self.more:
            self.current_page_num += 1
            return await self._generate()
        return None

    async def previous(self) -> t.Optional[t.Iterable[BaseObject]]:
        """
        Fetches the previous page of results.

        Returns:
            The previous page of results.
        """
        if self.current_page_num > 1:
            self.current_page_num -= 1
            return await self._generate()
        return None

    async def compress(self) -> t.List[t.Iterable[BaseObject]]:
        """
        Fetches all the pages of results.

        Returns:
            A list of pages of results.
        """
        return [datas async for datas in self]

    def __aiter__(self) -> Paginator:
        return self

    async def __anext__(self) -> t.Iterable[BaseObject]:
        data = await self.next()

        if not data:
            raise StopAsyncIteration

        return data

    async def _generate(self) -> t.Optional[t.List[BaseObject]]:
        """
        Generates the page of results.

        Returns:
            The page of results.
        """
        self._interface.add_option(page=self.current_page_num)
        data = await self._client.get(self._interface, metadata=True)

        if isinstance(data, tuple):
            self.current_page, self.more, _ = data
            return data[0]
        return None
