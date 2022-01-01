import typing as t
from dataclasses import dataclass
from .baseobject import BaseObject

__all__ = ("Ulist",)


@dataclass(slots=True)  # type: ignore
class Labels:
    id: int
    label: t.Optional[str] = None


class Ulist(BaseObject):

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
        self._labels = data.get("labels")

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
    def labels(self) -> t.Optional[t.Iterable[Labels]]:
        if self._labels is not None:
            return [Labels(**data) for data in self._labels]
        return None
