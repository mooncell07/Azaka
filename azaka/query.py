import enum
import typing as t
import json
from utils import clean_string

from typing_extensions import Self

__all__ = ("select", "AND", "OR", "Node")
BASE = "https://api.vndb.org/kana"


# GET - ENDPOINTS
SCHEMA_URL = f"{BASE}/schema"
STATS_URL = f"{BASE}/stats"
AUTHINFO_URL = f"{BASE}/authinfo"
USER_URL = f"{BASE}/user"


def AND(*args: tuple) -> list:
    return ["and", *args]


def OR(*args: tuple) -> list:
    return ["or", *args]


class Query:
    __slots__ = ("_route", "_body")

    def __init__(self, route = "", body = {}) -> None:
        self._route = route
        self._body = body or self._defaults()

    def _defaults(self):
        return {
        "filters": [],
        "fields": "id",
        "sort": "id",
        "reverse": False,
        "results": 10,
        "page": 1,
        "user": None,
        "count": False,
        "compact_filters": False,
        "normalized_filters": False
        }

    def frm(self, route: str) -> Self:
        self._route = clean_string(route)
        return self

    def where(self, filters: list) -> Self:
        self._body["filters"] = filters
        return self
    
    def sort(self, key: str) -> Self:
        self._body["sort"] = key
        return self

    @property
    def url(self) -> str:
        return f"{BASE}/{self._route}"

    @property
    def parse_body(self) -> str:
        if not self._body["fields"]:
            raise TypeError("Missing required data item: 'fields'")
        return json.dumps(self._body)


class Node:
    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = clean_string(name)

    def _fmt(self, op: str, val: str | list) -> list:
        return [self.name, op, val]

    def __eq__(self, val: object):
        if isinstance(val, (str, list)):
            return self._fmt("=", val)

    def __ne__(self, val: object):
        if isinstance(val, (str, list)):
            return self._fmt("!=", val)

    def __gt__(self, val: object):
        if isinstance(val, (str, list)):
            return self._fmt(">", val)

    def __ge__(self, val: object):
        if isinstance(val, (str, list)):
            return self._fmt(">=", val)

    def __lt__(self, val: object):
        if isinstance(val, (str, list)):
            return self._fmt("<", val)

    def __le__(self, val: object):
        if isinstance(val, (str, list)):
            return self._fmt("<=", val)


def select(*fields: str) -> Query:
    query = Query()
    if fields:
        query._body["fields"] = ", ".join(fields)
    return query
