from __future__ import annotations

import typing as t
from .interface import Interface, T

if t.TYPE_CHECKING:
    from .client import Client

__all__ = ("Paginator",)


class Paginator(t.Generic[T]):
    """
    A pagination wrapper over [Client.get](../client#azaka.client.Client.get)
    which provides async stateful iteration over the results.

    Attributes:
        current_page (t.Optiona[t.Iterable[BaseObject]]): The current page of results.
        current_page_num (int): The current page number.
        more (bool): If there are more pages to fetch.

    Example:
    ```py
    async for page in Paginator(client, interface):
        ...
    ```
    """

    __slots__ = ("_client", "_interface", "current_page", "current_page_num", "more")

    def __init__(self, client: Client, interface: Interface) -> None:
        self._client = client
        self._interface = interface
        self.current_page: t.Optional[t.Iterable[T]] = None
        self.current_page_num: int = 0
        self.more: bool = True

    async def next(self) -> t.Optional[t.Iterable[T]]:
        """
        Fetches the next page of results.

        Returns:
            The next page of results.
        """
        if self.more:
            self.current_page_num += 1
            return await self._generate()
        return None

    async def previous(self) -> t.Optional[t.Iterable[T]]:
        """
        Fetches the previous page of results.

        Returns:
            The previous page of results.
        """
        if self.current_page_num > 1:
            self.current_page_num -= 1
            return await self._generate()
        return None

    async def compress(self) -> t.List[t.Iterable[T]]:
        """
        Fetches all the pages of results.

        Returns:
            A list of pages of results.
        """
        return [datas async for datas in self]

    def __aiter__(self) -> Paginator:
        return self

    async def __anext__(self) -> t.Iterable[T]:
        data = await self.next()

        if not data:
            raise StopAsyncIteration

        return data

    async def _generate(self) -> t.Optional[t.List[T]]:
        """
        Generates the page of results.

        Returns:
            The page of results.
        """
        self._interface.add_option(page=self.current_page_num)
        data: t.Tuple[t.List[T], bool, int] = await self._client.get(self._interface, metadata=True)  # type: ignore

        if isinstance(data, tuple):
            self.current_page, self.more, _ = data
            return data[0]
        return None
