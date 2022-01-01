import typing as t
from dataclasses import dataclass

from .baseobject import BaseObject

__all__ = ("Producer",)


@dataclass(slots=True)  # type: ignore
class Links:
    homepage: t.Optional[str] = None
    wikidata: t.Optional[str] = None
    wikipedia: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Relation:
    id: int
    relation: t.Optional[str] = None
    name: t.Optional[str] = None
    original: t.Optional[str] = None


class Producer(BaseObject):
    __slots__ = (
        "_links",
        "_relations",
        "name",
        "original",
        "type",
        "language",
        "aliases",
        "description",
    )

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self._links = data.get("links", {})
        self._relations = data.get("relations")

        self.name = data.get("name")
        self.original = data.get("original")
        self.type = data.get("type")
        self.language = data.get("language")
        self.aliases = data.get("aliases")
        self.description = data.get("description")

    @property
    def links(self) -> Links:
        return Links(**self._links)

    @property
    def relations(self) -> t.Optional[t.Iterable[Relation]]:
        if self._relations is not None:
            return [Relation(**data) for data in self._relations]
        return None
