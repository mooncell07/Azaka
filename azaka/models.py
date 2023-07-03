import typing as t
from dataclasses import dataclass

__all__ = ("Stats", "AuthInfo", "User")


@dataclass
class Stats:
    chars: int
    producers: int
    releases: int
    staff: int
    tags: int
    traits: int
    vn: int


@dataclass
class AuthInfo:
    id: str
    username: str
    permissions: list[str]


@dataclass
class User:
    FOUND: bool

    search_term: str
    id: t.Optional[str] = None
    username: t.Optional[str] = None
    lengthvotes: t.Optional[int] = None
    lengthvotes_sum: t.Optional[int] = None
