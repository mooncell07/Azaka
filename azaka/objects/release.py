import typing as t
from dataclasses import dataclass

from ..tools import AnimationType, Rtype, VoicedType
from .baseobject import BaseObject

__all__ = ("Release",)


@dataclass
class Media:
    """
    A dataclass representing a media.

    Attributes:
        medium: The media's medium.
        qty: The media's quantity. `None` when it is not applicable for the medium.
    """

    qty: t.Optional[int] = None
    medium: t.Optional[str] = None


@dataclass
class ReleaseVN:
    """
    A dataclass representing a releasevn.

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


@dataclass
class ReleaseProducer:
    """
    A dataclass representing a releaseproducer.

    Attributes:
        id: The producer's id.
        name: The producer's name. (romaji)
        original: The producer's original/official name.
        developer: The producer is a developer.
        publisher: The producer is a publisher.
        type: The producer's type.
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

    ## FLAG: NONE
    Attributes:
        id (int): The release's ID.

    ## FLAG: [BASIC](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        title (str): The release's title. (romaji)
        original (str): The release's original/official title.
        released (str): The release date.
        type (str): The release type. (Deprecated)
        patch (bool): Whether the release is a patch.
        freeware (bool): Whether the release is freeware.
        doujin (bool): Whether the release is doujin.
        languages (t.iterable[str]): The release's languages.

    ## FLAG: [DETAILS](../enums.md#azaka.tools.enums.Flags)
    Attributes:
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
        "_vns",
        "_producers",
        "_medias",
        "_animations",
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

        self._vns = data.get("vn")
        self._producers = data.get("producers", [])
        self._medias = data.get("media", [])
        self._animations = data.get("animation", [])

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
        self.platforms: t.Optional[t.List[str]] = data.get("platforms")
        self.resolution: t.Optional[str] = data.get("resolution")
        self.voiced: t.Optional[VoicedType] = (
            VoicedType(data["voiced"]) if data.get("voiced") else None
        )

        self.languages: t.Optional[t.List[str]] = data.get("languages")

    @property
    def animations(self) -> t.List[AnimationType]:
        """
        Returns a [list][] of [AnimationType](../enums.md#azaka.tools.enums.AnimationType) enums.

        Note:
            The [list][] has two members of an
            [enum][] type [AnimationType](../enums.md#azaka.tools.enums.AnimationType),
            the first one indicating the story animations,
            the second the ero scene animations. Both members can be None if unknown or not applicable.

        Info:
            The [list][] is populated only when the command was issued with
            the `DETAILS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        return [AnimationType(data) for data in self._animations]

    @property
    def medias(self) -> t.List[Media]:
        """
        Returns a [list][] of [Media](./#azaka.objects.release.Media) objects.

        Info:
            The [list][] is populated only when the command was issued with
            the `DETAILS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        return [Media(**data) for data in self._medias]

    @property
    def release_vns(self) -> t.List[ReleaseVN]:
        """
        Returns a [list][] of [ReleaseVN](./#azaka.objects.release.ReleaseVN) objects.

        Info:
            The [list][] is populated only when the command was issued with
            the `VN` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        vns = []

        if self._vns:
            for vn in self._vns:
                vn["rtype"] = Rtype(vn["rtype"]) if vn.get("rtype") else None
                vns.append(ReleaseVN(**vn))

        return vns

    @property
    def release_producers(self) -> t.List[ReleaseProducer]:
        """
        Returns a [list][] of [ReleaseProducer](./#azaka.objects.release.ReleaseProducer) objects.

        Info:
            The [list][] is populated only when the command was issued with
            the `PRODUCERS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        return [ReleaseProducer(**data) for data in self._producers]
