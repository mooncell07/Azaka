import typing as t

__all__ = ("DBStats",)


class DBStats:
    """
    A class representing a dbstats.

    Note:
        This class is not meant to be instantiated directly.

    Note:
        Every Attribute is optional and may return `None`.

    Attributes:
        chars (int): The number of characters.
        posts (int): The number of posts.
        producers (int): The number of producers.
        releases (int): The number of releases.
        staff (int): The number of staff.
        tags (int): The number of tags.
        threads (int): The number of threads.
        traits (int): The number of traits.
        users (int): The number of users.
        vn (int): The number of VNs.
    """

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
