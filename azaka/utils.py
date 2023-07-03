import typing as t
from collections import namedtuple

__all__ = ("clean_string", "build_objects")


def clean_string(string: str) -> str:
    return string.strip().lower()

async def build_objects(route: str, jsons: list[dict[str, t.Any]]) -> t.Sequence[t.NamedTuple]:
    structs = []
    for json in jsons:
        struct = namedtuple(route.upper(), json)
        structs.append(struct(*json.values()))
    return structs
