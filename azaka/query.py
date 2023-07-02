import enum
import json

__all__ = ("select", "AND", "OR", "Query", "Node")


BASE = "https://api.vndb.org/kana"
ROUTES = {"vn", "release", "producer", "character", "staff", "tag", "trait"}


def AND(*args: tuple) -> list:
    return ["and", *args]


def OR(*args: tuple) -> list:
    return ["or", *args]


class Query:
    __slots__ = ("_route", "_fields", "_filters")

    def __init__(self, route=None, fields=None, filters=None) -> None:
        self._route: str = route
        self._fields: tuple = fields
        self._filters: list = filters

    def frm(self, route):
        route = route.strip().lower()

        if route in ROUTES:
            self._route = route
            return self
        else:
            raise NotImplementedError("Route not available.")

    def where(self, filters: list):
        self._filters = filters
        return self

    @property
    def url(self):
        return f"{BASE}/{self._route}"

    @property
    def body(self):
        return json.dumps({"filters": self._filters, "fields": ", ".join(self._fields)})


class Node:
    __slots__ = ("name",)

    def __init__(self, name: str):
        self.name = name.strip().lower()

    def _fmt(self, op: str, val: str | list) -> list[str | list]:
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
