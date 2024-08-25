import json
import typing as t

from azaka.utils import FT, clean_string

__all__ = ("select", "AND", "OR", "Node", "Query")

BASE = "https://api.vndb.org/kana"


# GET - ENDPOINTS
SCHEMA_URL = f"{BASE}/schema"
STATS_URL = f"{BASE}/stats"
AUTHINFO_URL = f"{BASE}/authinfo"
USER_URL = f"{BASE}/user"


def AND(*args: FT[str]) -> FT[str]:
    """
    The `AND` function is used to combine multiple [Node](./query.md#azaka.query.Node)s in a query. Only those results are returned
    that satisfy ALL the conditions.

    Note:
        This function uses Prefix Notation.
    
    Args:
        args: A variable length argument of all the [Node](./query.md#azaka.query.Node)s to be combined.
    
    Returns:
        A [list][] of [Node](./query.md#azaka.query.Node)s combined using the `and` operator.
    
    Example:
        ```python
        AND(
            Node("id") >"v2002",
            Node("lang") == "en",
            Node("olang") != "ja",
        )
        ```
    """
    return ["and", *args]


def OR(*args: FT[str]) -> FT[str]:
    """
    The `OR` function is used to combine multiple [Node](./query.md#azaka.query.Node)s in a query.
    All those results are returned that satisfy ANY of the conditions.

    Note:
        This function uses Prefix Notation.

    Args:
        args: A variable length argument of all the [Node](./query.md#azaka.query.Node)s to be combined.
    
    Returns:
        A [list][] of [Node](./query.md#azaka.query.Node)s combined using the `or` operator.

    Example:
        ```python
        OR(
            Node("id") >"v2002",
            Node("lang") == "en",
            Node("olang") != "ja",
        )
        ```
    """
    return ["or", *args]


class Body(t.TypedDict):
    filters: FT[str]
    fields: str
    sort: str
    reverse: bool
    results: int
    page: int
    user: t.Optional[str]
    count: bool
    compact_filters: bool
    normalized_filters: bool


class Query:
    """
    Query class for building a query to be executed on the VNDB API.

    Danger:
        This class is not meant to be instantiated directly but rather through the [select](./query.md#azaka.query.select) function.
    """
    __slots__ = ("_route", "_body")

    def __init__(self, route: str = "", body: t.Optional[Body] = None) -> None:
        self._route = route
        self._body: Body = body or self._defaults()

    def _defaults(self) -> Body:
        return {
            "filters": [],
            "fields": "id, ",
            "sort": "id",
            "reverse": False,
            "results": 10,
            "page": 1,
            "user": None,
            "count": False,
            "compact_filters": False,
            "normalized_filters": False,
        }

    def frm(self, route: str) -> t.Self:
        """
        The `frm` directive is used to specify the route of the query. 
        It comes after the [select](./query.md#azaka.query.select) function in query call chain.
        Unlike other directives, you can't leave it empty.

        tip:
            Consult the Official VNDB API Reference to find out what routes are supported for querying.

        Args:
            route: The route of the query.

        Returns:
            The [Query](./query.md#azaka.query.Query) object.

        Example:
            ```python
            query = select().frm("vn")
            ```
        """
        self._route = clean_string(route)
        return self

    def where(self, filters: t.Optional[FT[str]] = None) -> t.Self:
        """
        The `where` directive is used to specify the filters for the query.

        You make filters by using the [Node](./query.md#azaka.query.Node) class and running 
        comparisons (`==`, `!=` `>`, `<`, `>=`, `<=`) on it like so:

        `Node("filter_name") == "value"`

        or by passing a list of conditions like how API does it:
        
        `["filter_name", "=", "value"]`

        tip:
            Consult the Official VNDB API Reference to find out what filters are supported for what
            routes.

        Args:
            filters: A [list][] of filters or [Node](./query.md#azaka.query.Node) objects.

        Returns:
            The [Query](./query.md#azaka.query.Query) object.
        
        Example:
            ```python
            # With Node object
            query = select().frm("vn").where(Node("id") == "v2002")

            # With list
            query = select().frm("vn").where(["id", "=", "v2002"])
            ```
        """
        if filters:
            self._body["filters"] = filters
        return self

    def sort(self, key: t.Optional[str] = None) -> t.Self:
        """
        The `sort` directive is used to specify the key for sorting the results. It is an
        `optional` directive. Supported values depend on the type of data being queried.

        tip:
            Consult the Official VNDB API Reference to find out what sorting key is supported for what
            routes.
        
        Args:
            key: The key for sorting the results.
        
        Returns:
            The [Query](./query.md#azaka.query.Query) object.
        
        Example:
            ```python
            query = select("title").frm("vn").sort("title")
            ```
        """
        if key:
            self._body["sort"] = key
        return self

    def set_flags(
        self,
        reverse: bool = False,
        count: bool = False,
        compact_filters: bool = False,
        normalized_filters: bool = False,
    ) -> None:
        """
        Used to set flags for the query.

        Args:
            reverse: Reverse the order of results.
            count: Get the count of the results.
            compact_filters: Request for Compact filters of the query.
            normalized_filters: Request for Normalized Filters of the query.
        
        Example:
            ```python
            query = select().frm("vn").where(Node("id") == "v1")
            query.set_flags(reverse=True, count=True, compact_filters=True, normalized_filters=True)
            ```
        """
        self._body["reverse"] = reverse
        self._body["count"] = count
        self._body["compact_filters"] = compact_filters
        self._body["normalized_filters"] = normalized_filters

    @property
    def url(self) -> str:
        """
        The route being used for the query.
        """
        return f"{BASE}/{self._route}"

    @property
    def parse_body(self) -> str:
        """
        Returns the low level representation of the query body.
        """
        if not self._body["fields"]:
            raise ValueError("'fields' cannot be empty.")
        return json.dumps(self._body)


class Node:
    """
    The Node class acts as an abstraction over the lower level List representation of the query filters.
    Node constructor takes the name of the filter as an argument and provides comparison methods against
    the values used for filtering.

    Nodes are passed to the [where](./query.md#azaka.query.Query.where) directive of the [Query](./query.md#azaka.query.Query) object.

    It supports following list of predicates:

    - `==` (Equality): Used to fetch all entries that match the given filter value.

    Usage:
        ```python
        Node("id") == "v2002"
        ```
    - `!=` (Inequality): Used to fetch all entries that do not match the given filter value.

    Usage:
        ```python
        Node("id") != "v2002"
        ```
    
    - `>` (Greater Than): Used to fetch all entries that are greater than the given filter value.

    Usage:
        ```python
        Node("released") > "2020-01-01"
        ```

    - `>=` (Greater Than or Equal): Used to fetch all entries that are greater than or equal to the given filter value.

    Usage:
        ```python
        Node("votecount") >= "10"
        ```

    Same goes for `<` (Less Than) and `<=` (Less Than or Equal).

    Example:
        ```python
        #https://api.vndb.org/kana#filters

        query = (
            select("id", "average")
            .frm("vn")
            .where(
                AND(
                    OR(
                        Node("lang") == "en", 
                        Node("lang") == "de",
                        Node("lang") == "fr"
                    ),

                    Node("olang") != "ja",
                    
                    Node("release") == AND(
                        Node("released") >= "2020-01-01",
                        Node("producer") == (Node("id") == "p30"),
                    ),
                )
            )
        )

        ```
    """
    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        """
        Node Constructor.

        Args:
            name: The name of the filter.
        """
        self.name = clean_string(name)

    def guard(self, value: object) -> t.TypeGuard[str | FT[str]]:
        return isinstance(value, (str, list))

    def _fmt(self, op: str, val: str | FT[str]) -> FT[str]:
        return [self.name, op, val]

    def __eq__(self, val: object):
        if self.guard(val):
            return self._fmt("=", val)

    def __ne__(self, val: object):
        if self.guard(val):
            return self._fmt("!=", val)

    def __gt__(self, val: object):
        if self.guard(val):
            return self._fmt(">", val)

    def __ge__(self, val: object):
        if self.guard(val):
            return self._fmt(">=", val)

    def __lt__(self, val: object):
        if self.guard(val):
            return self._fmt("<", val)

    def __le__(self, val: object):
        if self.guard(val):
            return self._fmt("<=", val)


def select(*fields: str) -> Query:
    """
    The `select` function is used to specify the fields to be returned in the query results.
    In the Query call chain, it must be the first function to be called. If no fields are specified,
    the `id` field is used by default.

    tip:
        Consult the Official VNDB API Reference to find out what fields are supported for what
        routes.
        
    Args:
        fields: The fields that you want to fetch in the query results.
    
    Returns:
        The [Query](./query.md#azaka.query.Query) object.

    Example:
        ```python
        query = select("id", "title").frm("vn")
        ```
    """
    query = Query()
    if fields:
        query._body["fields"] += ", ".join([clean_string(i) for i in fields])
    else:
        query._body["fields"] = "id"
    return query
