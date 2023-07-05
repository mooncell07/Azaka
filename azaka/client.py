import functools
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
    __slots__ = ("cs", "token")

    def __init__(self, token: t.Optional[str] = None) -> None:
        self.token = token
        self.cs: t.Optional[aiohttp.ClientSession] = None

    @property
    def base_header(self) -> t.Optional[t.Mapping[str, str]]:
        return {"Authorization": f"token {self.token}"} if self.token else None

    async def __aenter__(self) -> Self:
        await self._create_cs()
        return self

    async def __aexit__(
        self,
        exc: t.Optional[t.Type[BaseException]],
        exc_val: t.Optional[BaseException],
        tb: t.Optional[TracebackType],
    ) -> None:
        await self.close_cs()

    async def get_schema(self) -> t.Mapping[str, str]:
        resp = await self._request(query.SCHEMA_URL)
        data = await self._get_data(resp)
        return t.cast(t.Mapping[str, str], data)

    async def get_stats(self) -> Stats:
        resp = await self._request(query.STATS_URL)
        data = await self._get_data(resp)
        return Stats(**data)

    async def get_auth_info(self) -> AuthInfo:
        if not self.base_header:
            raise TypeError("Missing required argument 'token'")
        resp = await self._request(query.AUTHINFO_URL, headers=self.base_header)
        data = await self._get_data(resp)
        return AuthInfo(**data)

    async def get_user(
        self, *users: str, fields: t.Sequence[str] = ()
    ) -> t.Sequence[User]:
        url = URL(query.USER_URL).update_query({"q": users, "fields": fields})
        resp = await self._request(url)
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
        if not query._route:
            raise TypeError("'route' cannot be empty")

        fn = functools.partial(
            self._request, url=query.url, post=True, data=query.parse_body
        )
        resp = await (fn(headers=self.base_header) if self.base_header else fn())

        data = await self._get_data(resp)
        return build_objects(query._route, data)

    async def _get_data(self, resp: aiohttp.ClientResponse) -> dict[str, RespT]:
        status = resp.status
        if 400 > status >= 200 and resp.content_type == "application/json":
            return await resp.json()
        else:
            msg = await resp.text()
            error = EXMAP.get(status)
            if error:
                raise error(msg)
            else:
                raise AzakaException(msg, status)

    async def _request(
        self,
        url: str | URL,
        post: bool = False,
        data: t.Optional[str] = None,
        headers: t.Optional[t.Mapping[str, str]] = None,
    ) -> aiohttp.ClientResponse:
        await self._create_cs()
        assert self.cs
        if post:
            return await self.cs.post(url=url, data=data, headers=headers)
        return await self.cs.get(url=url, headers=headers)

    async def _create_cs(self) -> None:
        if not self.cs:
            self.cs = aiohttp.ClientSession(
                headers={"Content-Type": "application/json"}
            )

    async def close_cs(self) -> None:
        if self.cs:
            await self.cs.close()
