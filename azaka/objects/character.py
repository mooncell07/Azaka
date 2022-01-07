import typing as t
from dataclasses import dataclass

from .vn import ImageFlagging
from .baseobject import BaseObject
from ..tools import Gender, Spoiler, Roles


@dataclass(slots=True)  # type: ignore
class Voiced:
    """
    A dataclass representing a Voiced.

    Attributes:
        id: staff ID.
        vid: VN ID.
        AID: The staff alias ID being used.
        note: The staff note.
    """

    id: int
    vid: int
    aid: t.Optional[int] = None
    note: t.Optional[str] = None


@dataclass(slots=True)  # type: ignore
class Instances:
    """
    A dataclass representing a Instances.

    Attributes:
        id: staff ID.
        spoiler: A [Spoiler][] object representing the sevearity of spoiler.
        name: Character name.
        original: Character's original name.
    """

    id: int
    spoiler: t.Optional[int] = None
    name: t.Optional[str] = None
    original: t.Optional[str] = None


class Character(BaseObject):
    """
    A class representing a character.

    Note:
        This class is not meant to be instantiated directly.

    Note:
        Every Attribute except `id` is optional and may return `None`.

    Attributes:
        id (int): The character's ID.
        name (str): The character's name (romaji).
        original (str): The character's original (kana/kanji) name.
        gender (Gender): Character's sex.
        spoil_gender (int): Actual sex if this is a spoiler.
        bloodt (str): Blood type of the character (can be one of `a`, `b`, `ab` or `o`)
        birthday (t.Iterable[int]): [list][] of two integers: day of the month (1-31) and the month (1-12). Either can be `None`.
        aliases (str): Aliases of the character.
        description (str): Description of the character.
        age (int): Age of the character in years.
        image (str): URL of the character's image.
        bust (int): Bust size of the character in cm.
        waist (int): Waist size of the character in cm.
        hip (int): Hip size of the character in cm.
        cup_size (str): Cup size of the character.
        weight (int): Weight of the character in kg.
        height (int): Height of the character in cm.
        traits (t.Iterable[t.Iterable[int]]): [list][] of traits linked to this character. Each trait is represented as a [list][] of two elements: The trait id ([int][]) and the spoiler level ([int][], 0-2).
    """  # noqa

    __slots__ = (
        "_links",
        "_relations",
        "_vns",
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
        "gender",
        "spoil_gender",
        "bloodt",
        "birthday",
        "age",
        "image",
    )

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self._image_flagging = data.get("image_flagging", {})
        self._voiced = data.get("voiced")
        self._instances = data.get("instances")
        self._vns: t.Optional[t.List[t.List[int]]] = data.get("vns")

        self.name: t.Optional[str] = data.get("name")
        self.original: t.Optional[str] = data.get("original")
        self.gender: t.Optional[Gender] = (
            Gender(data["gender"]) if data.get("gender") else None
        )
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

    @property
    def vns(self) -> t.Optional[t.List[t.List[int]]]:
        """
        List of VNs linked to this character.
        Each VN is a [list][] of 4 elements: VN id, release ID (0 = all releases),
        spoiler level ([Spoiler][]) and the role ([Roles][]).
        """
        vn_list = []
        if self._vns:
            for data in self._vns:
                data[2:4] = Spoiler(data[2]), Roles(data[3])  # type: ignore
                vn_list.append(data)
            return vn_list
        return None

    @property
    def image_flagging(self) -> ImageFlagging:
        """
        Returns the ImageFlagging of the character.
        """
        return ImageFlagging(**self._image_flagging)

    @property
    def voiced(self) -> t.Optional[t.List[Voiced]]:
        """
        Returns the [list][] of Voiced info. of the character.
        """
        if self._voiced:
            return [Voiced(**data) for data in self._voiced]
        return None

    @property
    def instances(self) -> t.Optional[t.List[Instances]]:
        """
        Returns the [list][] of Instances of the character.
        """
        incs = []
        if self._instances:
            for data in self._instances:
                data["spoiler"] = (
                    Spoiler(data["spoiler"]) if data.get("spoiler") else None
                )
                incs.append(Instances(**data))
            return incs
        return None
