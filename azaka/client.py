import typing as t
from collections import namedtuple
from types import TracebackType

import aiohttp
import query
from exceptions import EXMAP, AzakaException
from models import AuthInfo, Stats, User
from typing_extensions import Self
from yarl import URL

__all__ = ("Client",)


class Client:
    __slots__ = ("base_header", "cs")

    def __init__(self, key: t.Optional[str] = None) -> None:
        self.base_header = {"Authorization": f"token {key}"} if key else None

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

    async def get_schema(self) -> dict[str, str]:
        resp = await self.cs.get(query.SCHEMA_URL)
        data = await self._get_data(resp)
        return data

    async def get_stats(self) -> Stats:
        resp = await self.cs.get(query.STATS_URL)
        data = await self._get_data(resp)
        return Stats(**data)

    async def get_auth_info(self) -> AuthInfo:
        if not self.base_header:
            raise TypeError("Missing required argument 'key'")
        resp = await self.cs.get(query.AUTHINFO_URL, headers=self.base_header)
        data = await self._get_data(resp)
        return AuthInfo(**data)

    async def get_user(self, *users: str, fields: t.Sequence[str] = ()) -> t.Sequence[User]:
        url = URL(query.USER_URL).update_query({"q": users, "fields": fields})
        resp = await self.cs.get(url)
        data = await self._get_data(resp)
        user_list = []

        for user in data:
            u = (
                User(search_term=user, **data[user], FOUND=True)
                if data[user]
                else User(search_term=user, FOUND=False)
            )
            user_list.append(u)
        return user_list

    async def execute(
        self, query: query.Query, json: bool = False
    ) -> t.Sequence[dict[str, t.Any]] | t.Sequence[t.NamedTuple]:
        if self.base_header:
            resp = await self.cs.post(
                query.url, data=query.body, headers=self.base_header
            )
        else:
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
        self, query: query.Query, resp: aiohttp.ClientResponse
    ) -> t.Sequence[t.NamedTuple]:
        structs = []
        jsons = (await self._get_data(resp))["results"]
        for json in jsons:
            struct = namedtuple(query._route.upper(), json)
            structs.append(struct(*json.values()))
        return structs

    async def create_cs(self) -> None:
        self.cs = aiohttp.ClientSession(headers={"Content-Type": "application/json"})
