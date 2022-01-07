import typing as t
from dataclasses import dataclass

from .baseobject import BaseObject
from ..tools import VoicedType, AnimationType, Rtype

__all__ = ("Release",)


@dataclass(slots=True)  # type: ignore
class Media:
    """
    A dataclass representing a media.

    Attributes:
        medium: The media's medium.
        qty: The media's quantity. `None` when it is not applicable for the medium.
    """

    qty: t.Optional[int] = None
    medium: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Vn:
    """
    A dataclass representing a vn.

    Note:
        This vn is different from [VN][]. This one is an object returned by the [Release.vn][] property.

    Attributes:
        id: The vn's id.
        title: The vn's title.
        rtype: The vn's release type.
        original: The vn's original title.
    """

    id: int
    title: t.Optional[str] = None
    rtype: t.Optional[str] = None
    original: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Producers:
    """
    A dataclass representing a producers.

    Attributes:
        id: The producers' id.
        name: The producers' name. (romaji)
        original: The producers' original/official name.
        developer: The producer is a developer.
        publisher: The producer is a publisher.
        type: The producers' type.
    """

    id: int
    name: t.Optional[str] = None
    original: t.Optional[str] = None
    developer: t.Optional[bool] = None
    publisher: t.Optional[bool] = None
    type: t.Optional[str] = None


class Release(BaseObject):
    """
    A class representing a release.

    Note:
        This class is not meant to be instantiated directly.

    Note:
        Every Attribute is optional and may return `None`.

    Attributes:
        id (int): The release's ID.
        title (str): The release's title. (romaji)
        original (str): The release's original/official title.
        released (str): The release date.
        type (str): The release type. (Deprecated)
        patch (bool): Whether the release is a patch.
        freeware (bool): Whether the release is freeware.
        doujin (bool): Whether the release is doujin.
        languages (t.iterable[str]): The release's languages.
        website (str): The release's official website url.
        notes (str): The release's notes.
        minage (int): The release's age rating. (0 = all ages)
        gtin (str): The release's JAN/UPC/EAN code.
        catalog (str): The release's catalog number.
        platforms (t.iterable[str]): The release's platforms. (Empty [list][] when platform is unknown)
        resolution (str): The release's resolution.
        voiced (VoicedType): The release's voiced status.

    """

    __slots__ = (
        "_vn",
        "_producers",
        "_media",
        "_animation",
        "title",
        "original",
        "released",
        "languages",
        "type",
        "patch",
        "freeware",
        "doujin",
        "website",
        "notes",
        "minage",
        "gtin",
        "catalog",
        "resolution",
        "voiced",
        "platforms",
    )

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self._vn = data.get("vn")
        self._producers = data.get("producers")
        self._media = data.get("media")
        self._animation: t.Optional[t.Iterable[int]] = data.get("animation")

        self.title: t.Optional[str] = data.get("title")
        self.original: t.Optional[str] = data.get("original")
        self.released: t.Optional[str] = data.get("released")

        self.type: t.Optional[str] = data.get("type")
        self.patch: t.Optional[bool] = data.get("patch")
        self.freeware: t.Optional[bool] = data.get("freeware")
        self.doujin: t.Optional[bool] = data.get("doujin")
        self.website: t.Optional[str] = data.get("website")
        self.notes: t.Optional[str] = data.get("notes")
        self.minage: t.Optional[int] = data.get("minage")
        self.gtin: t.Optional[str] = data.get("gtin")
        self.catalog: t.Optional[str] = data.get("catalog")
        self.platforms: t.Optional[t.Iterable[str]] = data.get("platforms")
        self.resolution: t.Optional[str] = data.get("resolution")
        self.voiced: t.Optional[VoicedType] = (
            VoicedType(data["voiced"]) if data.get("voiced") else None
        )

        self.languages: t.Optional[t.Iterable[str]] = data.get("languages")

    @property
    def animation(self) -> t.Optional[t.List[t.Optional[AnimationType]]]:
        """
        Returns a [list][] of [AnimationType][].

        Note:
            The [list][] has two members of an [enum][] type [AnimationType][],
            the first one indicating the story animations,
            the second the ero scene animations. Both members can be None if unknown or not applicable.
        """
        anims = []
        if self._animation:
            for data in self._animation:
                atype = AnimationType(data) if data else None
                anims.append(atype)
            return anims
        return None

    @property
    def media(self) -> t.Optional[t.Iterable[Media]]:
        """
        Returns a [list][] of [Media][] dataclasses.
        """
        if self._media is not None:
            return [Media(**data) for data in self._media]
        return None

    @property
    def vn(self) -> t.Optional[t.Iterable[Vn]]:
        """
        Returns a [list][] of [Vn][] dataclasses related to this release.
        """
        vns = []
        if self._vn is not None:
            for vn in self._vn:
                vn["rtype"] = Rtype(vn["rtype"]) if vn.get("rtype") else None
                vns.append(Vn(**vn))
            return vns
        return None

    @property
    def producers(self) -> t.Optional[t.Iterable[Producers]]:
        """
        Returns a [list][] of [Producers][] dataclasses.
        """
        if self._producers is not None:
            return [Producers(**data) for data in self._producers]
        return None
