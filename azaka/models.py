import typing as t
from dataclasses import dataclass, field

__all__ = ("Stats", "AuthInfo", "User", "Response")


@dataclass
class Stats:
    """
    Stats [dataclasses.dataclass][] containing statistics about the VNDB database.

    Attributes:
        chars int: Number of character entries.
        producers int: Number of producer entries.
        releases int: Number of release entries.
        staff int: Number of staff entries.
        tags int: Number of tag entries.
        traits int: Number of trait entries.
        vn int: Number of visual novel entries.
    """

    chars: int
    producers: int
    releases: int
    staff: int
    tags: int
    traits: int
    vn: int


@dataclass
class AuthInfo:
    """
    AuthInfo [dataclasses.dataclass][] containing information about the API Token.

    Attributes:
        id str: User ID in "u123" format.
        username str: Username.
        permissions list[str]: List of permissions granted to the API Token.

    Info:
        There are two types of permissions:

        - `listread`: Allows read access to private labels and entries in the user's visual novel list.

        - `listwrite`: Allows write access to the user's visual novel list.

    """

    id: str
    username: str
    permissions: list[str]


@dataclass
class User:
    """
    User [dataclasses.dataclass][] containing information about a user.

    Attributes:
        FOUND bool: If the user was found or not.
        search_term str: The search term used.
        id str: User ID in "u123" format.
        username str: Username.
        lengthvotes int: Number of play time votes the user has submitted.
        lengthvotes_sum int: Sum of the user's play time votes, in minutes.

    Info:
        Strings that look like user IDs are not valid usernames, so the lookup is unambiguous. Usernames matching is case-insensitive.
    """

    FOUND: bool

    search_term: str
    id: t.Optional[str] = None
    username: t.Optional[str] = None
    lengthvotes: t.Optional[int] = None
    lengthvotes_sum: t.Optional[int] = None


@dataclass
class Response:
    """
    Response [dataclasses.dataclass][] containing the results and metadata of a query.

    Attributes:
        results list[t.NamedTuple]: A [list][] of nametuples dynamically created from the response representing the query results.
        more bool: If there are more results. Used for pagination.
        count int: Indicates the total number of entries that matched the given filters. Defaults to `1` if count is not explicitly set to true in the query.
        compact_filters Optional[str]: This is a compact string representation of the filters given in the query. Defaults to `None` if `compact_filters` is not explicitly set to `true` in the query.
        normalized_filters list[str]: This is a normalized JSON representation of the filters given in the query. Defaults to an `empty list` if `normalized_filters` is not explicitly set to `true` in the query.
    """

    results: t.Sequence[t.NamedTuple]
    more: bool = False
    count: int = 1
    compact_filters: t.Optional[str] = None
    normalized_filters: list[str] = field(default_factory=list)
