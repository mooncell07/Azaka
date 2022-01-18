import typing as t

__all__ = ("BaseObject",)


class BaseObject:
    """
    A base object for all the models in this directory. (except [DBStats](../dbstats/))

    Note:
        This class is not meant to be instantiated directly.

    Attributes:
        id (int): The id of the item. (It will never be `None`.)
    """

    __slots__ = ("id",)

    def __init__(self, id: int) -> None:
        self.id = id

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
