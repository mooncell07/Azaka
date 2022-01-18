import typing as t

from .baseobject import BaseObject

__all__ = ("Quote",)


class Quote(BaseObject):
    """
    A class representing a quote.

    Note:
        This class is not meant to be instantiated directly.

    Note:
        Every Attribute is optional and may return `None`.

    ## FLAG: NONE
    Attributes:
        id (int): The quote's id.

    ## FLAG: [BASIC](../enums.md#azaka.tools.enums.Flags)
    Attributes:
        title (str): The quote's title.
        quote (str): The quote's text.
    """

    __slots__ = ("title", "quote")

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        super().__init__(data["id"])

        self.title: t.Optional[str] = data.get("title")
        self.quote: t.Optional[str] = data.get("quote")
