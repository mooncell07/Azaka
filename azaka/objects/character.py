import typing as t
from dataclasses import dataclass

from .vn import ImageFlagging
from .baseobject import BaseObject


@dataclass(slots=True)  # type: ignore
class Voiced:
    id: int
    vid: int
    aid: t.Optional[int] = None
    note: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Instances:
    id: int
    spoiler: t.Optional[int] = None
    name: t.Optional[str] = None
    original: t.Optional[str] = None


class Character(BaseObject):
    __slots__ = (
        "_links",
        "_relations",
        "name",
        "original",
        "type",
        "language",
        "aliases",
        "description",
        "_voiced",
        "_instances",
        "_image_flagging",
        "bust",
        "waist",
        "hip",
        "cup_size",
        "weight",
        "height",
        "traits",
        "vns",
    )

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self._image_flagging = data.get("image_flagging", {})
        self._voiced = data.get("voiced")
        self._instances = data.get("instances")

        self.name: t.Optional[str] = data.get("name")
        self.original: t.Optional[str] = data.get("original")
        self.gender: t.Optional[str] = data.get("gender")
        self.spoil_gender: t.Optional[str] = data.get("spoil_gender")
        self.bloodt: t.Optional[str] = data.get("bloodt")
        self.birthday: t.Optional[t.Iterable[int]] = data.get("birthday")
        self.aliases: t.Optional[str] = data.get("aliases")
        self.description: t.Optional[str] = data.get("description")
        self.age: t.Optional[int] = data.get("age")
        self.image: t.Optional[str] = data.get("image")

        self.bust: t.Optional[int] = data.get("bust")
        self.waist: t.Optional[int] = data.get("waist")
        self.hip: t.Optional[int] = data.get("hip")
        self.cup_size: t.Optional[str] = data.get("cup_size")
        self.weight: t.Optional[int] = data.get("weight")
        self.height: t.Optional[int] = data.get("height")

        self.traits: t.Optional[t.Iterable[t.Iterable[int]]] = data.get("traits")
        self.vns: t.Optional[t.Iterable[t.Iterable[int]]] = data.get("vns")

    @property
    def image_flagging(self) -> ImageFlagging:
        return ImageFlagging(**self._image_flagging)

    @property
    def voiced(self) -> t.Optional[t.Iterable[Voiced]]:
        if self._voiced is not None:
            return [Voiced(**data) for data in self._voiced]
        return None

    @property
    def instances(self) -> t.Optional[t.Iterable[Instances]]:
        if self._instances is not None:
            return [Instances(**data) for data in self._instances]
        return None
