import query
from client import Client
from typing_extensions import Self
from utils import build_objects


class Paginator:
    def __init__(self, client: Client, max_results: int, query = None, json: bool = False):
        self.client = client
        self.max_results = max_results
        query._body.update({"results": max_results})
        self.query = query
        self.json = json

        self._resp = None

    async def _generate(self):
        self._resp = await self.client.execute(query=self.query, json=True)

        if not self.json:
            return await build_objects(self.query._route, self._resp["results"])
        return self._resp

    async def next(self):
        if not self._resp:
            return await self._generate()

        if self._resp.get("more"):
            self.query._body["page"] += 1
            return await self._generate()
    
    async def previous(self):
        if self.query and self.query._body["page"] > 1:
            self.query._body["page"] -= 1
            return await self._generate()

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self):
        data = await self.next()

        if not data:
            raise StopAsyncIteration

        return data

    async def flatten(self):
        return [i async for i in self]
