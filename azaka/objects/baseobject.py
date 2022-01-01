import typing as t

__all__ = ("BaseObject",)


class BaseObject:

    __slots__ = ("id",)

    def __init__(self, id: int) -> None:
        self.id = id

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"

    def __eq__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)
