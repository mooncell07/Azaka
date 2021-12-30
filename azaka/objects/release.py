import typing as t
from dataclasses import dataclass

from ..tools import ReprMixin

__all__ = ("Release",)


@dataclass(slots=True)  # type: ignore
class Media:
    qty: t.Optional[int] = None
    medium: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Vn:
    title: t.Optional[str] = None
    rtype: t.Optional[str] = None
    id: t.Optional[int] = None
    original: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Producers:
    id: t.Optional[int] = None
    name: t.Optional[str] = None
    original: t.Optional[str] = None
    developer: t.Optional[bool] = None
    publisher: t.Optional[bool] = None
    type: t.Optional[str] = None


class Release(ReprMixin):
    __slots__ = (
        "_vn",
        "_producers",
        "_media",
        "id",
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
        "animation",
    )

    def __init__(self, data) -> None:
        self._vn = data.get("vn")
        self._producers = data.get("producers")
        self._media = data.get("media")

        self.id: int = data["id"]
        self.title: t.Optional[str] = data.get("title")
        self.original: t.Optional[str] = data.get("original")
        self.released: t.Optional[str] = data.get("released")
        self.languages: t.Optional[t.Iterable[str]] = data.get("languages")
        self.type: t.Optional[str] = data.get("type")
        self.patch: t.Optional[bool] = data.get("patch")
        self.freeware: t.Optional[bool] = data.get("freeware")
        self.doujin: t.Optional[bool] = data.get("doujin")
        self.website: t.Optional[str] = data.get("website")
        self.notes: t.Optional[str] = data.get("notes")
        self.minage: t.Optional[int] = data.get("minage")
        self.gtin: t.Optional[str] = data.get("gtin")
        self.catalog: t.Optional[str] = data.get("catalog")
        self.resolution: t.Optional[str] = data.get("resolution")
        self.voiced: t.Optional[int] = data.get("voiced")
        self.animation: t.Optional[t.Iterable[int]] = data.get("animation")

        super(ReprMixin, self).__init__()

    @property
    def media(self) -> t.Optional[t.Iterable[Media]]:
        if self._media is not None:
            return [Media(**data) for data in self._media]
        return None

    @property
    def vn(self) -> t.Optional[t.Iterable[Vn]]:
        if self._vn is not None:
            return [Vn(**data) for data in self._vn]
        return None

    @property
    def producers(self) -> t.Optional[t.Iterable[Producers]]:
        if self._producers is not None:
            return [Producers(**data) for data in self._producers]
        return None
