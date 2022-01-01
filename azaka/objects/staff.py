import typing as t
from dataclasses import dataclass
from ..tools import ReprMixin


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
    id: t.Optional[int] = None
    aid: t.Optional[int] = None
    role: t.Optional[str] = None
    note: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Voiced:
    id: t.Optional[int] = None
    aid: t.Optional[int] = None
    cid: t.Optional[int] = None
    note: t.Optional[str] = None


class Staff(ReprMixin):
    __slots__ = (
        "_links",
        "_vns",
        "_voiced",
        "id",
        "name",
        "original",
        "gender",
        "language",
        "description",
        "aliases",
        "main_alias",
    )

    def __init__(self, data):
        self._links = data.get("links", {})
        self._vns = data.get("vns")
        self._voiced = data.get("voiced")

        self.id = data["id"]
        self.name = data.get("name")
        self.original = data.get("original")
        self.gender = data.get("gender")
        self.langauage = data.get("language")
        self.description = data.get("description")
        self.aliases = data.get("aliases")
        self.main_alias = data.get("main_alias")

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
