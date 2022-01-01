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

    def __init__(self, data: t.Mapping[str, t.Any]) -> None:
        self.chars: t.Optional[int] = data.get("chars")
        self.posts: t.Optional[int] = data.get("posts")
        self.producers: t.Optional[int] = data.get("producers")
        self.releases: t.Optional[int] = data.get("releases")
        self.staff: t.Optional[int] = data.get("staff")
        self.tags: t.Optional[int] = data.get("tags")
        self.threads: t.Optional[int] = data.get("threads")
        self.traits: t.Optional[int] = data.get("traits")
        self.users: t.Optional[int] = data.get("users")
        self.vn: t.Optional[int] = data.get("vn")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
