import typing as t
from dataclasses import dataclass

from .baseobject import BaseObject

__all__ = ("Producer",)


@dataclass(slots=True)  # type: ignore
class Links:
    """
    A dataclass representing a links.

    Attributes:
        homepage: Official homepage.
        wikipedia: Related Wikipedia page. (deprecated)
        wikidata: Wikidata identifier.
    """

    homepage: t.Optional[str] = None
    wikidata: t.Optional[str] = None
    wikipedia: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Relation:
    """
    A dataclass representing a relation.

    Attributes:
        id: The relation's ID.
        name: The relation's name.
        original: The relation's original name.
        relation: Relation to current producer.
    """

    id: int
    relation: t.Optional[str] = None
    name: t.Optional[str] = None
    original: t.Optional[str] = None


class Producer(BaseObject):
    """
    A class representing a producer.

    Note:
        This class is not meant to be instantiated directly.

    Note:
        Every Attribute is optional and may return `None`.

    Attributes:
        id (int): The producer's id.
        name (str): The producer's name. (romaji)
        original (str): The producer's original/official name.
        type (str): The producer's type.
        language (str): The producer's primary language.
        aliases (t.List[str]): [list][] of producer's aliases (alternative names).
        description (str): The producer's description/notes.
    """

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
        """
        Returns the [Links][] dataclass.
        """
        return Links(**self._links)

    @property
    def relations(self) -> t.Optional[t.Iterable[Relation]]:
        """
        Returns a [list][] of [Relations][] dataclasses.
        """
        if self._relations is not None:
            return [Relation(**data) for data in self._relations]
        return None
