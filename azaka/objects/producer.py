import typing as t
from dataclasses import dataclass

from .baseobject import BaseObject

__all__ = ("Producer",)


@dataclass
class ProducerLinks:
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


@dataclass
class ProducerRelation:
    """
    A dataclass representing a producerrelation.

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

    ## FLAG: NONE
    Attributes:
        id (int): The producer's id.

    ## FLAG: [BASIC](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        name (str): The producer's name. (romaji)
        original (str): The producer's original/official name.
        type (str): The producer's type.
        language (str): The producer's primary language.

    ## FLAG: [DETAILS](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        aliases (t.List[str]): [list][] of producer's aliases (alternative names).
        description (str): The producer's description/notes.
    """

    __slots__ = (
        "_link",
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

        self._link = data.get("links")
        self._relations = data.get("relations", [])

        self.name: t.Optional[str] = data.get("name")
        self.original: t.Optional[str] = data.get("original")
        self.type: t.Optional[str] = data.get("type")
        self.language: t.Optional[str] = data.get("language")
        self.aliases: t.List[str] = data.get("aliases", [])
        self.description: t.Optional[str] = data.get("description")

    @property
    def links(self) -> t.Optional[ProducerLinks]:
        """
        Returns the [ProducerLinks](./#azaka.objects.producer.ProducerLinks) object.

        Info:
            This returns a [ProducerLinks](./#azaka.objects.producer.ProducerLinks)
            object only when the command was issued with
            the `DETAILS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is `None`.
        """
        return ProducerLinks(**self._link) if self._link else None

    @property
    def relations(self) -> t.List[ProducerRelation]:
        """
        Returns a [list][] of [ProducerRelation](./#azaka.objects.producer.ProducerRelation) objects.

        Info:
            The [list][] is populated only when the command was issued with
            the `RELATIONS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        return [ProducerRelation(**data) for data in self._relations]
