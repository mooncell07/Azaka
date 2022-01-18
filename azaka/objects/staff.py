import typing as t
from dataclasses import dataclass

from ..tools import Gender
from .baseobject import BaseObject

__all__ = ("Staff",)


@dataclass
class StaffLinks:
    """
    A dataclass representing a link.

    Attributes:
        homepage: Official homepage.
        wikidata: Wikidata identifier.
        wikipedia: Related Wikipedia page. (deprecated)
        twitter: Twitter account.
        anidb: AniDB account.
        pixiv: Pixiv account.
    """

    homepage: t.Optional[str] = None
    wikidata: t.Optional[str] = None
    wikipedia: t.Optional[str] = None
    twitter: t.Optional[str] = None
    anidb: t.Optional[str] = None
    pixiv: t.Optional[str] = None


@dataclass
class StaffVN:
    """
    A dataclass representing a staffvn.

    Attributes:
        id: VN ID.
        aid: Staff Alias ID.
        role: The staff role.
        note: The staff note.
    """

    id: int
    aid: t.Optional[int] = None
    role: t.Optional[str] = None
    note: t.Optional[str] = None


@dataclass
class StaffVoiced:
    """
    A dataclass representing a staffvoiced.

    Attributes:
        id: The voiced's id.
        cid: The character's id.
        aid: The alias's id.
        note: note.
    """

    id: int
    cid: int
    aid: t.Optional[int] = None
    note: t.Optional[str] = None


class Staff(BaseObject):
    """
    A class representing a staff.

    Note:
        This class is not meant to be instantiated directly.

    Note:
        Every Attribute is optional and may return `None`.

    ## FLAG: NONE
    Attributes:
        id (int): The staff's id.

    ## FLAG: [BASIC](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        name (str): The staff's name. (romaji)
        original (str): The staff's original/official name.
        gender (Gender): The staff's gender. Returns an [enum][] [Gender](../enums.md#azaka.tools.enums.Gender)
        language (str): The staff's primary language.

    ## FLAG: [DETAILS](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        description (str): Description/notes of the staff.
        aliases (t.List[t.List[int]]) : Aliases of the staff.
        main_alias (int): The staff's main alias. (ID of the primary name.)

    """

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

        self._links = data.get("links")
        self._vns = data.get("vns", [])
        self._voiced = data.get("voiced", [])

        self.name: t.Optional[str] = data.get("name")
        self.original: t.Optional[str] = data.get("original")
        self.gender: t.Optional[Gender] = (
            Gender(data["gender"]) if data.get("gender") else None
        )
        self.language: t.Optional[str] = data.get("language")
        self.description: t.Optional[str] = data.get("description")
        self.aliases: t.List[t.List[int]] = data.get("aliases", [])
        self.main_alias: t.Optional[int] = data.get("main_alias")

    @property
    def links(self) -> t.Optional[StaffLinks]:
        """
        Returns the [StaffLinks](./#azaka.objects.staff.StaffLinks) object.

        Info:
            This returns a [StaffLinks](./#azaka.objects.staff.StaffLinks)
            object only when the command was issued with
            the `DETAILS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is `None`.
        """
        return StaffLinks(**self._links) if self._links else None

    @property
    def staff_vns(self) -> t.List[StaffVN]:
        """
        Returns a [list][] of [StaffVN](./#azaka.objects.staff.StaffVN) objects.

        Info:
            The [list][] is populated only when the command was issued with
            the `VNS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        return [StaffVN(**data) for data in self._vns]

    @property
    def voiced(self) -> t.List[StaffVoiced]:
        """
        Returns the [list][] of [StaffVoiced](./#azaka.objects.staff.StaffVoiced) objects.

        Info:
            The [list][] is populated only when the command was issued with
            the `VOICED` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        return [StaffVoiced(**data) for data in self._voiced]
