import functools
import typing as t
from collections import namedtuple
from types import TracebackType

import aiohttp
from yarl import URL

from azaka import query
from azaka.exceptions import EXMAP, AzakaException
from azaka.models import AuthInfo, Stats, User
from azaka.utils import Response, RespT, build_objects

__all__ = ("Client",)


class Client:
    __slots__ = ("cs", "token")

    def __init__(self, token: t.Optional[str] = None) -> None:
        """
        Client Constructor.

        Args:
            token: VNDB API access token.

        Attributes:
            cs (t.Optional[aiohttp.ClientSession]): An aiohttp.ClientSession object.
        """
        self.token = token
        self.cs: t.Optional[aiohttp.ClientSession] = None

    @property
    def base_header(self) -> t.Optional[t.Mapping[str, str]]:
        """
        Return a dict. containing Auth. token. if token is supplied else it is [None][]
        """
        return {"Authorization": f"token {self.token}"} if self.token else None

    async def __aenter__(self) -> t.Self:
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
        """
        Return a Mapping containing metadata about API objects and enums.

        Returns:
            data: Mapping of API structure.
        """
        resp = await self._request(query.SCHEMA_URL)
        data = await self._get_data(resp)
        return t.cast(t.Mapping[str, str], data)

    async def get_stats(self) -> Stats:
        """
        Return VNDB database stats.

        Returns:
            stats: A [dataclasses.dataclass][] representation of the [json][] response.
        """
        resp = await self._request(query.STATS_URL)
        data = await self._get_data(resp)
        return Stats(**data)

    async def get_auth_info(self) -> AuthInfo:
        """
        Validate the API token and return information about it.

        Returns:
            authinfo: A [dataclasses.dataclass][] representation of the [json][] response.

        Note:
            - A [TypeError][] is raised if the token is not passed.

            - InvalidAuthTokenError will be raised by the API if token is found invalid.
        """
        if not self.base_header:
            raise TypeError("Missing required argument 'token'")
        resp = await self._request(query.AUTHINFO_URL, headers=self.base_header)
        data = await self._get_data(resp)
        return AuthInfo(**data)

    async def get_user(
        self, *users: str, fields: t.Sequence[str] = ()
    ) -> t.Sequence[User]:
        """
        Find a user by id or username and return information about them.

        Args:
            users: Variable number of username/ids to search for.
            fields: A Sequence type holding all fields to select.

        Accepted fields for the `fields` parameter are:

        - id

        - username

        - lengthvotes

        - lengthvotes_sum

        Note:
            The `id` and `username` fields are always selected and
            should not be explicitly specified.

        Returns:
            user_list: A [list][] of User objects.

        Tip:
            Since API supports multiple user lookup using just one query, you can pass multiple
            users like so: `await client.get_user("u1", "u2", .....)`
        """
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
        """
        Return a Response object containing the results of the query and associated metadata.

        This method is used for searching and querying any database entry. It supports all the
        query routes exposed by the API publicly.


        Note:
            This method dynamically generates the Response.results attribute.
            Only the fields that you specify in the select() function during the
            query will be present in the list of results.

        Note:
            Fields that access data inside another data structure, such as image.url,
            will have the left part become the attribute of the result and the data
            structure associated with the right part will become it's value.
            For example, the Response may look like this:

            `Response(results=[VN(id="v2", image={"url": ...})], ...)`

            The wrapper does not handle nested data.

        Tip:
            If you are new, I recommend reading ... to get a clear
            understanding of how to build queries.

        Args:
            query: A Query object.

        Returns:
            response: A Response object.
        """
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
        """
        Close the internal [aiohttp.ClientSession].

        Danger:
            You must call this method after completing the request if you are not using
            Context Manager.
        """
        if self.cs:
            await self.cs.close()
