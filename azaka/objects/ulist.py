import typing as t
from dataclasses import dataclass

from .baseobject import BaseObject

__all__ = ("Ulist",)


@dataclass
class Label:
    """
    A dataclass representing a labels.

    Attributes:
        id: The label's id.
        label: The label's name.
    """

    id: int
    label: str


class Ulist(BaseObject):

    """
    A class representing a ulist.

    Note:
        This class is not meant to be instantiated directly.

    Note:
        Every Attribute is optional and may return `None`.

    ## FLAG: NONE
    Attributes:
        id (int): The ulist's ID.

    ## FLAG: [BASIC](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        uid (int): The ulist's ID.
        vn (int): The VN's ID.
        added (int): The date the ulist was added.
        lastmod (int): The date the ulist was last modified.
        voted (int): The date the ulist was voted.
        vote (int): The vote of the ulist.
        notes (str): The notes of the ulist.
        started (str): The date the ulist was started.
        finished (str): The date the ulist was finished.
    """

    __slots__ = (
        "_labels",
        "uid",
        "vn",
        "added",
        "lastmod",
        "voted",
        "vote",
        "notes",
        "started",
        "finished",
    )

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["uid"])
        self._labels = data.get("labels", [])

        self.uid: t.Optional[int] = data["uid"]
        self.vn: t.Optional[int] = data.get("vn")
        self.added: t.Optional[int] = data.get("added")
        self.lastmod: t.Optional[int] = data.get("lastmod")
        self.voted: t.Optional[int] = data.get("voted")
        self.vote: t.Optional[int] = data.get("vote")
        self.notes: t.Optional[str] = data.get("notes")
        self.started: t.Optional[str] = data.get("started")
        self.finished: t.Optional[str] = data.get("finished")

    @property
    def labels(self) -> t.Iterable[Label]:
        """
        Returns the [list][] of [Label](./#azaka.objects.ulist.Label)s of the ulist.

        Info:
            The [list][] is populated only when the command was issued with
            the `LABELS` [Flags](../enums.md#azaka.tools.enums.Flags) otherwise it is empty.
        """
        return [Label(**label) for label in self._labels]
