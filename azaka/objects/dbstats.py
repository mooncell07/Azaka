import typing as t

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
        self.chars: t.Optional[int] = _data.get("chars")
        self.posts: t.Optional[int] = _data.get("posts")
        self.producers: t.Optional[int] = _data.get("producers")
        self.releases: t.Optional[int] = _data.get("releases")
        self.staff: t.Optional[int] = _data.get("staff")
        self.tags: t.Optional[int] = _data.get("tags")
        self.threads: t.Optional[int] = _data.get("threads")
        self.traits: t.Optional[int] = _data.get("traits")
        self.users: t.Optional[int] = _data.get("users")
        self.vn: t.Optional[int] = _data.get("vn")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
