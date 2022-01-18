import typing as t

from .baseobject import BaseObject

__all__ = ("User",)


class User(BaseObject):

    """
    A class representing a user.

    Note:
        This class is not meant to be instantiated directly.

    Note:
        Every Attribute is optional and may return `None`.

    ## FLAG: NONE
    Attributes:
        id (int): The user's ID.

    ## FLAG: [BASIC](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        username (str): The user's username.

    """

    __slots__ = ("username",)

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self.username: t.Optional[str] = data.get("username")
