import typing as t
from collections import namedtuple
from types import TracebackType

import aiohttp
from typing_extensions import Self
from yarl import URL

from azaka import query
from azaka.exceptions import EXMAP, AzakaException
from azaka.models import AuthInfo, Stats, User
from azaka.utils import Response, RespT, build_objects

__all__ = ("Client",)


class Client:
    __slots__ = ("base_header", "cs")

    def __init__(self, token: t.Optional[str] = None) -> None:
        self.base_header: t.Optional[t.Mapping[str, str]] = (
            {"Authorization": f"token {token}"} if token else None
        )

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

    async def get_schema(self) -> t.Mapping[str, str]:
        resp = await self.cs.get(query.SCHEMA_URL)
        data = await self._get_data(resp)
        return t.cast(t.Mapping[str, str], data)

    async def get_stats(self) -> Stats:
        resp = await self.cs.get(query.STATS_URL)
        data = await self._get_data(resp)
        return Stats(**data)

    async def get_auth_info(self) -> AuthInfo:
        if not self.base_header:
            raise TypeError("Missing required argument 'token'")
        resp = await self.cs.get(query.AUTHINFO_URL, headers=self.base_header)
        data = await self._get_data(resp)
        return AuthInfo(**data)

    async def get_user(
        self, *users: str, fields: t.Sequence[str] = ()
    ) -> t.Sequence[User]:
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

    async def execute(self, query: query.Query) -> Response:
        if self.base_header:
            resp = await self.cs.post(
                query.url, data=query.parse_body, headers=self.base_header
            )
        else:
            resp = await self.cs.post(query.url, data=query.parse_body)

        data = await self._get_data(resp)
        return await build_objects(query._route, data)

    async def _get_data(self, resp: aiohttp.ClientResponse) -> dict[str, RespT]:
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

    async def create_cs(self) -> None:
        self.cs = aiohttp.ClientSession(headers={"Content-Type": "application/json"})
