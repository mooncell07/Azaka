import enum
import functools
import json
import typing as t
from dataclasses import dataclass, field

from azaka.utils import FT, clean_string

__all__ = ("select", "AND", "OR", "Node")
BASE = "https://api.vndb.org/kana"


# GET - ENDPOINTS
SCHEMA_URL = f"{BASE}/schema"
STATS_URL = f"{BASE}/stats"
AUTHINFO_URL = f"{BASE}/authinfo"
USER_URL = f"{BASE}/user"


def AND(*args: FT[str]) -> FT[str]:
    return ["and", *args]


def OR(*args: FT[str]) -> FT[str]:
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
        self._route = clean_string(route)
        return self

    def where(self, filters: t.Optional[FT[str]] = None) -> t.Self:
        if filters:
            self._body["filters"] = filters
        return self

    def sort(self, key: t.Optional[str] = None) -> t.Self:
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
        self._body["reverse"] = reverse
        self._body["count"] = count
        self._body["compact_filters"] = compact_filters
        self._body["normalized_filters"] = normalized_filters

    @property
    def url(self) -> str:
        return f"{BASE}/{self._route}"

    @property
    def parse_body(self) -> str:
        if not self._body["fields"]:
            raise ValueError("'fields' cannot be empty.")
        return json.dumps(self._body)


class Node:
    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
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
    query = Query()
    if fields:
        query._body["fields"] += ", ".join([clean_string(i) for i in fields])
    else:
        query._body["fields"] = "id"
    return query
