import typing as t
from dataclasses import dataclass

from .baseobject import BaseObject
from ..tools import VoicedType, AnimationType, Rtype

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
class PartialVN:
    """
    A dataclass representing a partialvn.

    Note:
        This vn is different from [VN][].
        This one is an object returned by the [Release.partial_vns](./#azaka.objects.release.Release.partial_vns)
        property and doesn't contain all the attributes of the VN.

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
class PartialProducer:
    """
    A dataclass representing a partialproducer.

    Note:
        This producer is different from [VN][]. This one is an object returned by the
        [Release.partial_producers](./#azaka.objects.release.Release.partial_producers)
        property and doesn't contain all the attributes of the producer.

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
        self.platforms: t.Optional[t.Iterable[str]] = data.get("platforms")
        self.resolution: t.Optional[str] = data.get("resolution")
        self.voiced: t.Optional[VoicedType] = (
            VoicedType(data["voiced"]) if data.get("voiced") else None
        )

        self.languages: t.Optional[t.Iterable[str]] = data.get("languages")

    @property
    def animations(self) -> t.List[AnimationType]:
        """
        Returns a [list][] of [AnimationType](../enums.md#azaka.tools.enums.AnimationType) enums.

        Note:
            The [list][] has two members of an [enum][] type [AnimationType][],
            the first one indicating the story animations,
            the second the ero scene animations. Both members can be None if unknown or not applicable.
        """
        return [AnimationType(data) for data in self._animations]

    @property
    def medias(self) -> t.List[Media]:
        """
        Returns a [list][] of [Media](./#azaka.objects.release.Media) objects.
        """
        return [Media(**data) for data in self._medias]

    @property
    def partial_vns(self) -> t.List[PartialVN]:
        """
        Returns a [list][] of [PartialVN](./#azaka.objects.release.PartialVN) objects.

        Info:
            The [list][] is populated only when the command was issued with
            the `VN` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        vns = []

        if self._vns:
            for vn in self._vns:
                vn["rtype"] = Rtype(vn["rtype"]) if vn.get("rtype") else None
                vns.append(PartialVN(**vn))

        return vns

    @property
    def partial_producers(self) -> t.List[PartialProducer]:
        """
        Returns a [list][] of [PartialProducer](./#azaka.objects.release.PartialProducer) objects.

        Info:
            The [list][] is populated only when the command was issued with
            the `PRODUCERS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        return [PartialProducer(**data) for data in self._producers]
