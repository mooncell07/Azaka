import typing as t
from .baseobject import BaseObject

__all__ = ("Quote",)


class Quote(BaseObject):

    __slots__ = ("title", "quote")

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self.title: t.Optional[str] = data.get("title")
        self.quote: t.Optional[str] = data.get("quote")
