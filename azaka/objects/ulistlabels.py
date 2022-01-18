import typing as t

from .baseobject import BaseObject

__all__ = ("UlistLabels",)


class UlistLabels(BaseObject):

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
        label (str): The label's name.
        private (bool): The label is private.
    """

    __slots__ = ("uid", "label", "private")

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self.uid: t.Optional[int] = data.get("uid")
        self.label: t.Optional[str] = data.get("label")
        self.private: t.Optional[bool] = data.get("private")
