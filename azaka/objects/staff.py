import typing as t
from dataclasses import dataclass

from .baseobject import BaseObject

__all__ = ("Staff",)


@dataclass(slots=True)  # type: ignore
class Links:
    homepage: t.Optional[str] = None
    wikidata: t.Optional[str] = None
    wikipedia: t.Optional[str] = None
    twitter: t.Optional[str] = None
    anidb: t.Optional[str] = None
    pixiv: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Vns:
    id: int
    aid: t.Optional[int] = None
    role: t.Optional[str] = None
    note: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Voiced:
    id: int
    cid: int
    aid: t.Optional[int] = None
    note: t.Optional[str] = None


class Staff(BaseObject):
    __slots__ = (
        "_links",
        "_vns",
        "_voiced",
        "name",
        "original",
        "gender",
        "language",
        "description",
        "aliases",
        "main_alias",
    )

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self._links = data.get("links", {})
        self._vns = data.get("vns")
        self._voiced = data.get("voiced")

        self.name: t.Optional[str] = data.get("name")
        self.original: t.Optional[str] = data.get("original")
        self.gender: t.Optional[str] = data.get("gender")
        self.language: t.Optional[str] = data.get("language")
        self.description: t.Optional[str] = data.get("description")
        self.aliases: t.Optional[t.Iterable[t.Iterable[int]]] = data.get("aliases")
        self.main_alias: t.Optional[t.Iterable[t.Iterable[int]]] = data.get(
            "main_alias"
        )

    @property
    def links(self) -> Links:
        return Links(**self._links)

    @property
    def vns(self) -> t.Optional[t.Iterable[Vns]]:
        if self._vns is not None:
            return [Vns(**data) for data in self._vns]
        return None

    @property
    def voiced(self) -> t.Optional[t.Iterable[Voiced]]:
        if self._voiced is not None:
            return [Voiced(**data) for data in self._voiced]
        return None
