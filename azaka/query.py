import enum
import json
import typing as t

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
    __slots__ = ("_route", "_fields", "_filters")

    def __init__(
        self,
        route: t.Optional[str] = None,
        fields: t.Optional[tuple[str, ...]] = None,
        filters: t.Optional[list] = None,
    ) -> None:
        self._route = route
        self._fields = fields
        self._filters = filters

    def frm(self, route: str) -> Self:
        self._route = route.strip().lower()
        return self

    def where(self, filters: list) -> Self:
        self._filters = filters
        return self

    @property
    def url(self) -> str:
        return f"{BASE}/{self._route}"

    @property
    def body(self) -> str:
        if not self._fields:
            raise TypeError("Missing required data item: 'field'")
        return json.dumps({"filters": self._filters, "fields": ", ".join(self._fields)})


class Node:
    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name.strip().lower()

    def _fmt(self, op: str, val: str | list) -> list:
        clean_val: str | list

        if isinstance(val, list):
            clean_val = [i.strip().lower() for i in val]
        else:
            clean_val = val.strip().lower()
        return [self.name, op, clean_val]

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
    query._fields = fields
    return query
