import typing as t

__all__ = ("BaseObject", "SENTINEL")

SENTINEL = object()


class BaseObject:
    """
    A base object for all the models in this directory. (except [DBStats](../dbstats/))

    Note:
        This class is not meant to be instantiated directly.

    Attributes:
        data (t.Mapping[str, t.Any]): The entire [dict][] of data API returned.
        id (int): The id or uid of the item. (It will never be `None`.)
    """

    __slots__ = ("data", "id")

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        self.data = data
        self.id: int = data.get("id") or data["uid"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"

    def __eq__(self, other: t.Any) -> bool:
        """
        Compares two objects using their id.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self) -> int:
        """
        Returns the hashed id of the object.

        Returns:
            int: The hashed id of the object.
        """
        return hash(self.id)

    def __ne__(self, other: t.Any) -> bool:
        """
        Compares two objects using their id.

        Returns:
            bool: True if the objects are not equal, False otherwise.
        """
        return not self.__eq__(other)
