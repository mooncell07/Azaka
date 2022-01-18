import typing as t
from dataclasses import dataclass

from .baseobject import BaseObject

__all__ = ("VN", "ImageFlagging")


@dataclass
class ImageFlagging:
    """
    A dataclass representing an imageflagging.

    Attributes:
        votecount: The image's vote count.
        sexual_avg: The image's sexual average.
        violence_avg: The image's violence average.
    """

    votecount: t.Optional[int] = None
    sexual_avg: t.Optional[int] = None
    violence_avg: t.Optional[int] = None


@dataclass
class Anime:
    """
    A dataclass representing an anime.

    Attributes:
        id: The anime's id.
        title_romaji: The anime's title. (romaji)
        title_kanji: The anime's title. (kanji)
        ann_id: The anime's AnimeNewsNetwork ID.
        nfo_id: The anime's AnimeNfo ID
        year: The anime's release year.
        type: The anime's type.
    """

    id: int
    ann_id: t.Optional[int] = None
    nfo_id: t.Optional[str] = None
    title_romaji: t.Optional[str] = None
    title_kanji: t.Optional[str] = None
    year: t.Optional[int] = None
    type: t.Optional[str] = None


@dataclass
class VNStaff:
    """
    A dataclass representing a vnstaff.

    Attributes:
        sid: The staff's id.
        aid: The staff's alias id.
        name: The staff's name.
        original: The staff's original name.
        role: The staff's role.
        note: The staff's note.
    """

    sid: t.Optional[str] = None
    aid: t.Optional[int] = None
    name: t.Optional[str] = None
    role: t.Optional[str] = None
    original: t.Optional[str] = None
    note: t.Optional[str] = None


@dataclass
class Screens:
    """
    A dataclass representing a screens.

    Attributes:
        image: URL of the full-size screenshot.
        rid: Release ID.
        flagging: [ImageFlagging](./#azaka.objects,vn.ImageFlagging) object.
        height: Height of the screenshot.
        width: Width of the screenshot.
        nsfw: True if the screenshot is NSFW.
    """

    image: t.Optional[str] = None
    rid: t.Optional[int] = None
    flagging: t.Optional[ImageFlagging] = None
    height: t.Optional[int] = None
    width: t.Optional[int] = None
    nsfw: t.Optional[bool] = None


@dataclass
class VNRelation:
    """
    A dataclass representing a vnrelation.

    Attributes:
        id: The relation's id.
        relation: Relation to the vn.
        title: The relation's title. (romaji)
        original: The relation's original title.
        official: If the relation is an official one.
    """

    id: int
    relation: t.Optional[str] = None
    title: t.Optional[str] = None
    official: t.Optional[bool] = None
    original: t.Optional[str] = None


@dataclass
class VNLinks:
    """
    A dataclass representing a vnlinks.

    Attributes:
        wikidata: The vn's wikidata identifier.
        renai: The name part of the url on renai.us
        wikipedia: Name of the related article on the English Wikipedia. (depricated)
        encubed: The URL-encoded tag used on encubed. (deprecated)
    """

    wikidata: t.Optional[str] = None
    renai: t.Optional[str] = None
    wikipedia: t.Optional[str] = None
    encubed: t.Optional[str] = None


class VN(BaseObject):
    """
    A class representing a vn.

    Note:
        This class is not meant to be instantiated directly.

    Note:
        Every Attribute is optional and may return `None`.

    ## FLAG: NONE
    Attributes:
        id (int): The vn's id.

    ## FLAG: [BASIC](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        title (str): The vn's title.
        original (str): The vn's original/official title.
        released (str): The vn's release date.
        language (t.List[str]): The language(s) the vn is available in.
        orig_lang (t.List[str]): The vn's original language.
        platform (t.List[str]): The platforms on which the vn is available on.

    ## FLAG: [DETAILS](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        description (str): The vn's description.
        image (str): The vn's image url.
        tags (t.List[t.List[int]]): The vn's tags.

    ## FLAG: [STATS](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        votecount (int): The vn's vote count.
        popularity (int): The vn's popularity.
        rating (int): The vn's rating.
    """

    __slots__ = (
        "_anime",
        "_screens",
        "_relations",
        "_staff",
        "_image_flagging",
        "_links",
        "description",
        "tags",
        "title",
        "original",
        "released",
        "languages",
        "orig_lang",
        "platforms",
        "aliases",
        "length",
        "image",
        "popularity",
        "rating",
        "votecount",
    )

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self._anime = data.get("anime", [])
        self._screens = data.get("screens")
        self._relations = data.get("relations", [])
        self._staff = data.get("staff", [])
        self._image_flagging = data.get("image_flagging", {})
        self._links = data.get("links")

        self.description: t.Optional[str] = data.get("description")
        self.title: t.Optional[str] = data.get("title")
        self.original: t.Optional[str] = data.get("original")
        self.released: t.Optional[str] = data.get("released")
        self.orig_lang: t.Optional[str] = data.get("orig_lang")
        self.aliases: t.Optional[str] = data.get("aliases")
        self.length: t.Optional[int] = data.get("length")
        self.image: t.Optional[str] = data.get("image")

        self.platforms: t.Optional[t.Iterable[str]] = data.get("platforms")
        self.languages: t.Optional[t.Iterable[str]] = data.get("languages")
        self.tags: t.Optional[t.Iterable[t.Iterable[int]]] = data.get("tags")
        self.popularity: t.Optional[int] = data.get("popularity")
        self.rating: t.Optional[int] = data.get("rating")
        self.votecount: t.Optional[int] = data.get("votecount")

    @property
    def anime(self) -> t.List[Anime]:
        """
        Returns a [list][] of [Anime](./#azaka.objects.vn.Anime) objects associated with this VN.

        Info:
            The [list][] is populated only when the command was issued with
            the `ANIME` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        return [Anime(**data) for data in self._anime]

    @property
    def screens(self) -> t.List[Screens]:
        """
        Returns a [list][] of [Screens](./#azaka.objects.vn.Screens) objects associated with this VN.

        Info:
            The [list][] is populated only when the command was issued with
            the `SCREENS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        screen_array = []

        if self._screens is not None:
            for data in self._screens:
                if data.get("flagging"):
                    flagging = ImageFlagging(**data.get("flagging"))
                    data["flagging"] = flagging
                screen_array.append(Screens(**data))

        return screen_array

    @property
    def relations(self) -> t.List[VNRelation]:
        """
        Returns a [list][] of [VNRelation](./#azaka.objects.vn.VNRelation) objects associated with this VN.

        Info:
            The [list][] is populated only when the command was issued with
            the `RELATIONS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        return [VNRelation(**data) for data in self._relations]

    @property
    def staff(self) -> t.List[VNStaff]:
        """
        Returns a [list][] of [VNStaff](./#azaka.objects.vn.VNStaff) objects associated with this VN.

        Info:
            The [list][] is populated only when the command was issued with
            the `STAFF` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        return [VNStaff(**data) for data in self._staff]

    @property
    def image_flagging(self) -> t.Optional[ImageFlagging]:
        """
        Returns the [ImageFlagging](./#azaka.objects.vn.ImageFlagging) object associated with this VN.

        Info:
            This returns an [ImageFlagging](./#azaka.objects.vn.ImageFlagging)
            object only when the command was issued with
            the `DETAILS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is `None`.
        """
        return ImageFlagging(**self._image_flagging) if self._image_flagging else None

    @property
    def links(self) -> t.Optional[VNLinks]:
        """
        Returns the [VNLinks](./#azaka.objects.vn.VNLinks) object.

        Info:
            This returns a [VNLinks](./#azaka.objects.vn.VNLinks)
            object only when the command was issued with
            the `DETAILS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is `None`.
        """
        return VNLinks(**self._links) if self._links else None
