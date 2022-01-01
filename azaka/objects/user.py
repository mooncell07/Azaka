import typing as t
from .baseobject import BaseObject


__all__ = ("User",)


class User(BaseObject):

    __slots__ = ("username",)

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self.username: t.Optional[str] = data.get("username")
