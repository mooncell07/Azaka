import typing as t
from dataclasses import dataclass

from ..tools import Gender, Roles, Spoiler
from .baseobject import BaseObject
from .vn import ImageFlagging


@dataclass
class CharacterVoiced:
    """
    A dataclass representing a charactervoiced.

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


@dataclass
class Instance:
    """
    A dataclass representing an instance.

    Attributes:
        id: staff ID.
        spoiler: A [Spoiler](../enums.md#azaka.tools.enums.Spoiler) object representing the sevearity of spoiler.
        name: Character name.
        original: Character's original name.
    """

    id: int
    spoiler: t.Optional[Spoiler] = None
    name: t.Optional[str] = None
    original: t.Optional[str] = None


class Character(BaseObject):
    """
    A class representing a character.

    Note:
        This class is not meant to be instantiated directly.

    Note:
        Every Attribute except `id` is optional and may return `None`.

    ## FLAG: NONE
    Attributes:
        id (int): The character's ID.

    ## FLAG: [BASIC](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        name (str): The character's name (romaji).
        original (str): The character's original (kana/kanji) name.
        gender (Gender): Character's sex.
        spoil_gender (int): Actual sex if this is a spoiler.
        bloodt (str): Blood type of the character (can be one of `a`, `b`, `ab` or `o`)
        birthday (t.List[int]): [list][] of two integers: day of the month (1-31) and the month (1-12). Either can be `None`.

    ## FLAG: [DETAILS](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        aliases (str): Aliases of the character.
        description (str): Description of the character.
        age (int): Age of the character in years.
        image (str): URL of the character's image.

    ## FLAG: [MEAS](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        bust (int): Bust size of the character in cm.
        waist (int): Waist size of the character in cm.
        hip (int): Hip size of the character in cm.
        cup_size (str): Cup size of the character.
        weight (int): Weight of the character in kg.
        height (int): Height of the character in cm.

    ## FLAG: [TRAITS](../enums.md#azaka.tools.enums.Flags)

    Attributes:
        traits (t.list[t.List[int]]): [list][] of traits linked to this character. Each trait is represented as a [list][] of two elements: The trait id ([int][]) and the spoiler level ([int][], 0-2).
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

        self._image_flagging = data.get("image_flagging")
        self._voiced = data.get("voiced", [])
        self._instances = data.get("instances", [])
        self._vns: t.List[t.List[int]] = data.get("vns", [])

        self.name: t.Optional[str] = data.get("name")
        self.original: t.Optional[str] = data.get("original")
        self.gender: t.Optional[Gender] = (
            Gender(data["gender"]) if data.get("gender") else None
        )
        self.spoil_gender: t.Optional[str] = data.get("spoil_gender")
        self.bloodt: t.Optional[str] = data.get("bloodt")
        self.birthday: t.Optional[t.List[int]] = data.get("birthday")
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

        self.traits: t.List[t.List[int]] = data.get("traits", [[]])

    @property
    def vns(self) -> t.List[t.List[int]]:
        """
        Returns [list][] of visual novels linked to this character.
        Each VN is a [list][] of 4 elements: VN id, release ID (0 = all releases),
        spoiler level ([Spoiler](../enums.md#azaka.tools.enums.Spoiler))
        and the role ([Roles](../enums.md#azaka.tools.enums.Roles)).

        Info:
            The [list][] is populated only when the command was issued with
            the `VNS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        vn_list = []

        if self._vns:
            for data in self._vns:
                if data:
                    data[2:4] = Spoiler(data[2]), Roles(data[3])  # type: ignore
                    vn_list.append(data)

        return vn_list

    @property
    def image_flagging(self) -> t.Optional[ImageFlagging]:
        """
        Returns the [ImageFlagging](../objects/vn.md#azaka.objects.vn.ImageFlagging) of the character.

        Info:
            This returns an [ImageFlagging](../objects/vn.md#azaka.objects.vn.ImageFlagging)
            object only when the command was issued with
            the `DETAILS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is `None`.
        """
        return ImageFlagging(**self._image_flagging) if self._image_flagging else None

    @property
    def voiced(self) -> t.List[CharacterVoiced]:
        """
        Returns the [list][] of [CharacterVoiced](./#azaka.objects.character.CharacterVoiced) objects..

        Info:
            The [list][] is populated only when the command was issued with
            the `VOICED` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        return [CharacterVoiced(**data) for data in self._voiced]

    @property
    def instances(self) -> t.List[Instance]:
        """
        Returns the [list][] of [Instance](./#azaka.objects.character.Instance)s of the character.

        Info:
            The [list][] is populated only when the command was issued with
            the `INSTANCES` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        incs = []

        if self._instances:
            for data in self._instances:
                data["spoiler"] = (
                    Spoiler(data["spoiler"]) if data.get("spoiler") else None
                )
                incs.append(Instance(**data))

        return incs
