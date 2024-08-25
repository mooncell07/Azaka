import functools
import typing as t
from types import TracebackType

import aiohttp
from yarl import URL

from azaka import query
from azaka.exceptions import EXMAP, AzakaException
from azaka.models import AuthInfo, Response, Stats, User
from azaka.utils import RespT, build_objects

__all__ = ("Client",)


class Client:
    """
    Client class for interacting with the VNDB API.
    """

    __slots__ = ("cs", "token")

    def __init__(self, token: t.Optional[str] = None) -> None:
        """
        Client constructor.

        Args:
            token: VNDB API access token.

        Attributes:
            cs (Optional[aiohttp.ClientSession]): An [aiohttp.ClientSession](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession) object.
        """
        self.token = token
        self.cs: t.Optional[aiohttp.ClientSession] = None

    @property
    def base_header(self) -> t.Optional[dict[str, str]]:
        """
        Returns a [dict][] containing the Authorization header.

        Note:
            If the token is not passed, it will return [None][].
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

    async def get_schema(self) -> dict[str, str]:
        """
        Fetches the schema of the API Database.

        Returns:
            A [dict][] containing the schema of the API Database.
        """
        resp = await self._request(query.SCHEMA_URL)
        data = await self._get_data(resp)
        return t.cast(dict[str, str], data)

    async def get_stats(self) -> Stats:
        """
        Fetches the statistics of the API's Database.

        Returns:
            A [Stats](./models.md#azaka.models.Stats) object.
        """
        resp = await self._request(query.STATS_URL)
        data = await self._get_data(resp)
        return Stats(**data)

    async def get_auth_info(self) -> AuthInfo:
        """
        Validates and Returns information about the given API Token.

        Returns:
            An [AuthInfo](./models.md#azaka.models.AuthInfo) object.

        Exceptions:
            TypeError: A [TypeError][] is raised if the token is not passed.

            InvalidAuthTokenError: [InvalidAuthTokenError](./exceptions.md#azaka.exceptions.InvalidAuthTokenError) is raised by the API if token is found invalid.
        """
        if not self.base_header:
            raise TypeError("Missing required argument 'token'")
        resp = await self._request(query.AUTHINFO_URL, headers=self.base_header)
        data = await self._get_data(resp)
        return AuthInfo(**data)

    async def get_user(self, *users: str, fields: list[str] = ()) -> list[User]:
        """
        Looks up user(s) by id or username and returns information about them.

        Args:
            users: A variable length argument of user ids or usernames as [str][]s.
            fields: A [list][] of fields to select.

        Accepted fields for the `fields` parameter are:

        - id

        - username

        - lengthvotes

        - lengthvotes_sum

        Note:
            The `id` and `username` fields are always selected and
            should not be explicitly specified.

        Returns:
            A [list][] of [User](./models.md#azaka.models.User) objects.

        Tip:
            Since API supports multiple user lookup using just one query, you can pass multiple
            users like so:

            `await client.get_user("u1", "u2", .....)`
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
        Sends the query to the VNDB API.

        Note:
            This method dynamically generates the Response.results attribute.
            Only the fields that you specify in the `select()` function at the time of building
            the query will be present in the list of results.

        Note:
            Some fields utilize dot notation to access nested data such as `image.url`.
            For such fields, we use the parent field name (`image` in this case) as an attribute of the
            result, and a dictionary containing the child fields (`url` in this case)
            as the value of the said attribute. Example:

            `VN(id="v2", image={"url": ...})`

        See Also:
            [Response](./models.md#azaka.models.Response), [Query](./query.md#azaka.query.Query)

        Args:
            query: A [Query](./query.md#azaka.query.Query) object.

        Returns:
            A [Response](./models.md#azaka.models.Response) object containing the results of the query and associated metadata.
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
        headers: t.Optional[dict[str, str]] = None,
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
        Close the internal [aiohttp.ClientSession](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession) object.
        Danger:
            You must call this method after completing the request if you are not using
            Context Manager.
        """
        if self.cs:
            await self.cs.close()
