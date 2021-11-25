import typing as t

from azaka.tools.transformer import make_repr

__all__ = ("DBStats",)


class DBStats:

    __slots__ = (
        "_data",
        "chars",
        "posts",
        "producers",
        "releases",
        "staff",
        "tags",
        "threads",
        "traits",
        "users",
        "vn",
    )

    def __init__(self, _data: t.Mapping[str, t.Any]) -> None:
        self._data = _data
        self.chars: t.Optional[int] = self._data.get("chars")
        self.posts: t.Optional[int] = self._data.get("posts")
        self.producers: t.Optional[int] = self._data.get("producers")
        self.releases: t.Optional[int] = self._data.get("releases")
        self.staff: t.Optional[int] = self._data.get("staff")
        self.tags: t.Optional[int] = self._data.get("tags")
        self.threads: t.Optional[int] = self._data.get("threads")
        self.traits: t.Optional[int] = self._data.get("traits")
        self.users: t.Optional[int] = self._data.get("users")
        self.vn: t.Optional[int] = self._data.get("vn")

    def __repr__(self) -> str:
        return make_repr(self)
