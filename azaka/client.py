from collections import namedtuple

import aiohttp
from query import Query

__all__ = ("Client",)


class Client:
    __slots__ = ("key", "cs")

    def __init__(self, key=None) -> None:
        self.key = key

    async def __aenter__(self):
        await self.create_cs()
        return self

    async def __aexit__(self, exc, exc_val, tb):
        await self.cs.close()

    async def execute(self, query: Query, json: bool = False):
        resp = await self.cs.post(query.url, data=query.body)

        if json:
            obj = await self._get_data(resp)
        else:
            obj = await self._make_object(query, resp)

        return obj["results"]

    async def _get_data(self, resp: aiohttp.ClientResponse):
        if 400 > resp.status >= 200:
            return await resp.json()
        else:
            raise NotImplementedError(await resp.text())

    async def _make_object(self, query: Query, resp: aiohttp.ClientResponse):
        structs = []
        jsons = (await self._get_data(resp))["results"]
        for json in jsons:
            struct = namedtuple(query._route.upper(), json)
            structs.append(struct(*json.values()))
        return structs

    async def create_cs(self):
        self.cs = aiohttp.ClientSession(headers={"Content-Type": "application/json"})
