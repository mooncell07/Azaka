from ..tools import ReprMixin

__all__ = ("Quote",)


class Quote(ReprMixin):
    __slots__ = ("id", "title", "quote")

    def __init__(self, data) -> None:
        self.id = data["id"]
        self.title = data.get("title")
        self.quote = data.get("quote")
