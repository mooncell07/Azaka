import typing as t
from collections import namedtuple
from dataclasses import dataclass, field

__all__ = ("Response", "clean_string", "build_objects")


@dataclass
class Response:
    results: t.Sequence[t.NamedTuple]
    more: bool = False
    count: int = 1
    compact_filters: str = ""
    normalized_filters: list[str] = field(default_factory=list)


def clean_string(string: str) -> str:
    return string.strip().lower()


async def build_objects(route: str, json: dict[str, t.Any]) -> Response:
    objects = []
    for res in json["results"]:
        object = namedtuple(route.upper(), res)
        objects.append(object(*res.values()))

    del json["results"]
    resp = Response(results=objects, **json)
    return resp
