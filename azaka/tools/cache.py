import typing as t
from collections import OrderedDict

__all__ = ("Cache",)


class Cache:

    __slots__ = ("cache", "maxsize")

    def __init__(self, maxsize=50) -> None:

        self.maxsize = maxsize
        self.cache: OrderedDict = OrderedDict()

    def get(self, key: t.Any) -> t.Any:
        return self.cache.get(key, None)

    def put(self, key: t.Any, value: t.Any) -> None:
        if len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def delete(self, key: t.Any) -> None:
        if key in self.cache:
            del self.cache[key]

    def clear(self) -> None:
        self.cache.clear()

    def __len__(self) -> int:
        return len(self.cache)

    def __contains__(self, key: t.Any) -> bool:
        return key in self.cache

    def __getitem__(self, key: t.Any) -> t.Any:
        return self.cache[key]

    def __delitem__(self, key: t.Any) -> None:
        if key in self.cache:
            del self.cache[key]
        else:
            raise KeyError(key) from None

    def __repr__(self) -> t.Any:
        return str(self.cache)

    def __delattr__(self, name: t.Any) -> None:
        if name in self.__dict__:
            del self.__dict__[name]
        else:
            delattr(self.cache, name)

    def __copy__(self):
        return self.__class__(self.cache)

    def __reversed__(self):
        return reversed(self.cache)
