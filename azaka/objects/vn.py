import typing as t
from dataclasses import dataclass

from .baseobject import BaseObject


__all__ = ("VN", "ImageFlagging")


@dataclass(slots=True)  # type: ignore
class ImageFlagging:
    votecount: t.Optional[int] = None
    sexual_avg: t.Optional[int] = None
    violence_avg: t.Optional[int] = None


@dataclass(slots=True)  # type: ignore
class Anime:
    id: int
    ann_id: t.Optional[int] = None
    nfo_id: t.Optional[str] = None
    title_romaji: t.Optional[str] = None
    title_kanji: t.Optional[str] = None
    year: t.Optional[int] = None
    type: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Staff:
    sid: t.Optional[str] = None
    aid: t.Optional[int] = None
    name: t.Optional[str] = None
    role: t.Optional[str] = None
    original: t.Optional[str] = None
    note: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Screens:
    image: t.Optional[str] = None
    rid: t.Optional[int] = None
    flagging: t.Optional[ImageFlagging] = None
    height: t.Optional[int] = None
    width: t.Optional[int] = None
    nsfw: t.Optional[bool] = None


@dataclass(slots=True)  # type: ignore
class Relations:
    id: int
    relation: t.Optional[str] = None
    title: t.Optional[str] = None
    official: t.Optional[bool] = None
    original: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Links:
    wikidata: t.Optional[str] = None
    renai: t.Optional[str] = None
    wikipedia: t.Optional[str] = None
    encubed: t.Optional[str] = None


class VN(BaseObject):
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
    )

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self._anime = data.get("anime")
        self._screens = data.get("screens")
        self._relations = data.get("relations")
        self._staff = data.get("staff")
        self._image_flagging = data.get("image_flagging", {})
        self._links = data.get("links", {})

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

    @property
    def anime(self) -> t.Optional[t.Iterable[Anime]]:
        if self._anime is not None:
            return [Anime(**data) for data in self._anime]
        return None

    @property
    def screens(self) -> t.Optional[t.Iterable[Screens]]:
        if self._screens is not None:
            screen_array = []
            for data in self._screens:
                if data.get("flagging"):
                    flagging = ImageFlagging(**data.get("flagging"))
                    data["flagging"] = flagging
                screen_array.append(Screens(**data))
            return screen_array
        return None

    @property
    def relations(self) -> t.Optional[t.Iterable[Relations]]:
        if self._relations is not None:
            return [Relations(**data) for data in self._relations]
        return None

    @property
    def staff(self) -> t.Optional[t.Iterable[Staff]]:
        if self._staff is not None:
            return [Staff(**data) for data in self._staff]
        return None

    @property
    def image_flagging(self) -> ImageFlagging:
        return ImageFlagging(**self._image_flagging)

    @property
    def links(self) -> Links:
        return Links(**self._links)
