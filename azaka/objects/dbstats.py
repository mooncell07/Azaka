import typing as t

__all__ = ("DBStats",)


class DBStats:

    __slots__ = ("_data",)

    def __init__(self, _data: t.Mapping[str, t.Any]) -> None:
        self._data = _data

    @property
    def vn(self) -> t.Optional[int]:
        return self._data.get("vn")

    @property
    def producers(self) -> t.Optional[int]:
        return self._data.get("producers")

    @property
    def users(self) -> t.Optional[int]:
        return self._data.get("users")

    @property
    def traits(self) -> t.Optional[int]:
        return self._data.get("traits")

    @property
    def releases(self) -> t.Optional[int]:
        return self._data.get("releases")

    @property
    def tags(self) -> t.Optional[int]:
        return self._data.get("tags")

    @property
    def chars(self) -> t.Optional[int]:
        return self._data.get("chars")

    @property
    def staff(self) -> t.Optional[int]:
        return self._data.get("staff")

    @property
    def threads(self) -> t.Optional[int]:
        return self._data.get("threads")

    @property
    def posts(self) -> t.Optional[int]:
        return self._data.get("posts")
