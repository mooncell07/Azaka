import typing as t
from .baseobject import BaseObject

__all__ = ("UlistLabels",)


class UlistLabels(BaseObject):

    __slots__ = ("uid", "label", "private")

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self.uid: t.Optional[int] = data.get("uid")
        self.label: t.Optional[str] = data.get("label")
        self.private: t.Optional[bool] = data.get("private")
