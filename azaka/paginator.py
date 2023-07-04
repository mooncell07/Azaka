import typing as t

from typing_extensions import Self

from azaka import query
from azaka.client import Client
from azaka.utils import Response, build_objects

__all__ = ("Paginator",)


class Paginator:
    __slots__ = ("client", "max_results", "query", "_resp")

    def __init__(self, client: Client, query: query.Query, max_results: int) -> None:
        self.client = client
        self.max_results = max_results
        query._body["results"] = max_results
        self.query = query
        self._resp: t.Optional[Response] = None

    async def _generate(self) -> Response:
        self._resp = await self.client.execute(query=self.query)
        return self._resp

    async def next(self) -> t.Optional[Response]:
        if not self._resp:
            return await self._generate()

        if self._resp.more:
            self.query._body["page"] += 1
            return await self._generate()

        return None

    async def previous(self) -> t.Optional[Response]:
        if self.query and self.query._body["page"] > 1:
            self.query._body["page"] -= 1
            return await self._generate()
        return None

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> Response:
        data = await self.next()

        if not data:
            raise StopAsyncIteration

        return data

    def current(self) -> t.Optional[Response]:
        return self._resp

    async def flatten(self) -> list[Response]:
        return [i async for i in self]
