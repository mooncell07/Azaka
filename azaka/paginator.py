import typing as t

from azaka.query import Query
from azaka.client import Client
from azaka.utils import Response

__all__ = ("Paginator",)


class Paginator:
    """
    Paginator class for starting a pagination session.

    Example:
        ```python
        async def main() -> None:
            query = (select("id", "title")
                    .frm("vn")
                    .where(Node("olang") == "en"))

            async with Client() as client:
                paginator = Paginator(
                    client, query=query, max_results_per_page=2, exit_after=3
                )
                async for page in paginator:
                    for vn in page.results:
                        print(vn.title)

        ```
    """

    __slots__ = ("client", "query", "_resp", "_exit_after")

    def __init__(
        self,
        client: Client,
        query: Query,
        max_results_per_page: int,
        exit_after: t.Optional[int] = None,
    ) -> None:
        """
        Paginator constructor.

        Args:
            client: The [Client](./client.md) object.
            query: The Query for the pagination.
            max_results_per_page: Maximum number of results per page.
            exit_after: Exit after a certain number of pages.
        """
        self.client = client
        query._body["results"] = max_results_per_page
        self.query = query
        self._resp: t.Optional[Response] = None
        self._exit_after = exit_after

    async def _generate(self) -> Response:
        self._resp = await self.client.execute(query=self.query)
        return self._resp

    async def next(self) -> t.Optional[Response]:
        """
        Progress to the next page of results.

        Returns:
            Optional[Response]: A Response object.
        """
        if not self._resp:
            return await self._generate()

        if self._resp.more:
            self.query._body["page"] += 1
            return await self._generate()

        return None

    async def previous(self) -> t.Optional[Response]:
        """
        Move back to the previous page of results.

        Returns:
            Optional[Response]: A Response object.
        """
        if self.query and self.query._body["page"] > 1:
            self.query._body["page"] -= 1
            return await self._generate()
        return None

    def __aiter__(self) -> t.Self:
        return self

    async def __anext__(self) -> Response:
        data = await self.next()
        if not data or self._handle_counter():
            raise StopAsyncIteration

        return data

    def _handle_counter(self) -> bool:
        if self._exit_after is None:
            return False
        if not isinstance(self._exit_after, int) or self._exit_after < 0:
            raise ValueError("'exit_after' must be a positive integer")
        if self._exit_after == 0:
            return True
        self._exit_after -= 1
        return False

    def current(self) -> t.Optional[Response]:
        """
        Get the current page of results.

        Returns:
            Optional[Response]: A Response object.
        """
        return self._resp

    async def flatten(self) -> list[Response]:
        """
        Flatten the results of the pagination into a [list][].

        Returns:
            list[Response]: A [list][] of Response objects.
        """
        return [i async for i in self]
