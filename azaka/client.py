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

    async def execute(self, query: Query):
        response = await self.cs.post(query.route, data=query.body)
        return response

    async def create_cs(self):
        self.cs = aiohttp.ClientSession(headers={"Content-Type": "application/json"})
