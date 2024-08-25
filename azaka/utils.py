import typing as t
from collections import namedtuple

from azaka.models import Response

__all__ = ("clean_string", "build_objects", "FT", "RespT")

T = t.TypeVar("T")
FT = list[T | "FT[T]"]


class RespT(t.TypedDict):
    results: t.Sequence[t.Mapping[str, t.Any]]
    more: bool
    count: int
    compact_filters: str
    normalized_filters: list[str]


def clean_string(string: str) -> str:
    return string.strip().lower()


def build_objects(route: str, json: dict[str, t.Any]) -> Response:
    objects = []
    for res in json["results"]:
        object = namedtuple(route.upper(), res)  # type: ignore
        objects.append(object(*res.values()))

    del json["results"]
    resp = Response(results=objects, **json)
    return resp
