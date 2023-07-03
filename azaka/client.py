import typing as t
from collections import namedtuple
from types import TracebackType

import aiohttp
from exceptions import EXMAP, AzakaException
from query import Query
from typing_extensions import Self

__all__ = ("Client",)


class Client:
    __slots__ = ("key", "cs")

    def __init__(self, key: t.Optional[str] = None) -> None:
        self.key = key

    async def __aenter__(self) -> Self:
        await self.create_cs()
        return self

    async def __aexit__(
        self,
        exc: t.Optional[t.Type[BaseException]],
        exc_val: t.Optional[BaseException],
        tb: t.Optional[TracebackType],
    ) -> None:
        await self.cs.close()

    async def execute(
        self, query: Query, json: bool = False
    ) -> t.Sequence[dict[str, t.Any]] | t.Sequence[t.NamedTuple]:
        resp = await self.cs.post(query.url, data=query.body)

        if json:
            return (await self._get_data(resp))["results"]
        else:
            return await self._make_object(query, resp)

    async def _get_data(self, resp: aiohttp.ClientResponse) -> dict[str, t.Any]:
        status = resp.status
        if 400 > status >= 200:
            return await resp.json()
        else:
            msg = await resp.text()
            error = EXMAP.get(status)
            if error:
                raise error(msg)
            else:
                raise AzakaException(msg, status)

    async def _make_object(
        self, query: Query, resp: aiohttp.ClientResponse
    ) -> t.Sequence[t.NamedTuple]:
        structs = []
        jsons = (await self._get_data(resp))["results"]
        for json in jsons:
            struct = namedtuple(query._route.upper(), json)
            structs.append(struct(*json.values()))
        return structs

    async def create_cs(self) -> None:
        self.cs = aiohttp.ClientSession(headers={"Content-Type": "application/json"})
