import json


__all__ = ("select", "AND", "OR", "Query", "Node")


BASE = "https://api.vndb.org/kana"


def AND(*args: list) -> list:
    return ["and", *args]


def OR(*args: list) -> list:
    return ["or", *args]


class Query:
    __slots__ = ("route", "_fields", "_filters")

    def __init__(self, route=None, fields=None, filters=None) -> None:
        self.route: str = route
        self._fields: list = fields
        self._filters: list = filters

    def frm(self, route):
        self.route = f"{BASE}/{route}"
        return self

    def where(self, filters: list):
        self._filters = filters
        return self

    @property
    def body(self):
        return json.dumps({"filters": self._filters, "fields": ", ".join(self._fields)})


class Node:
    __slots__ = ("name",)

    def __init__(self, name: str):
        self.name = name

    def _fmt(self, op: str, val: str | list) -> list[str | list]:
        return [self.name, op, val]

    def __eq__(self, val: str | list):
        return self._fmt("=", val)

    def __ne__(self, val: str | list):
        return self._fmt("!=", val)

    def __gt__(self, val: str | list):
        return self._fmt(">", val)

    def __ge__(self, val: str | list):
        return self._fmt(">=", val)

    def __lt__(self, val: str | list):
        return self._fmt("<", val)

    def __le__(self, val: str | list):
        return self._fmt("<=", val)


def select(*fields: str) -> Query:
    query = Query()
    query._fields = fields
    return query
