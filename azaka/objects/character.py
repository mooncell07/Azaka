import typing as t
from dataclasses import dataclass
from ..tools import ReprMixin
from .visualnovel import ImageFlagging


@dataclass(slots=True)  # type: ignore
class Voiced:
    id: t.Optional[int] = None
    aid: t.Optional[int] = None
    vid: t.Optional[int] = None
    note: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Instances:
    id: t.Optional[int] = None
    spoiler: t.Optional[int] = None
    name: t.Optional[str] = None
    original: t.Optional[str] = None


class Character(ReprMixin):
    __slots__ = (
        "_links",
        "_relations",
        "id",
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

    def __init__(self, data) -> None:
        self._image_flagging = data.get("image_flagging", {})
        self._voiced = data.get("voiced")
        self._instances = data.get("instances")

        self.id = data["id"]
        self.name = data.get("name")
        self.original = data.get("original")
        self.gender = data.get("gender")
        self.spoil_gender = data.get("spoil_gender")
        self.bloodt = data.get("bloodt")
        self.birthday = data.get("birthday")
        self.aliases = data.get("aliases")
        self.description = data.get("description")
        self.age = data.get("age")
        self.image = data.get("image")

        self.bust = data.get("bust")
        self.waist = data.get("waist")
        self.hip = data.get("hip")
        self.cup_size = data.get("cup_size")
        self.weight = data.get("weight")
        self.height = data.get("height")

        self.traits = data.get("traits")
        self.vns = data.get("vns")

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
