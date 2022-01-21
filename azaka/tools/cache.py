from __future__ import annotations

import typing as t
from collections import OrderedDict

__all__ = ("Cache",)


class Cache:

    """
    A [dict][]-like object that is used for caching.

    Warning:
        This class is not meant to be instantiated by the user.
    """

    __slots__ = ("cache", "maxsize")

    def __init__(self, maxsize=50) -> None:
        """
        Cache constructor.

        Args:
            maxsize: The maximum size of the cache.

        Attributes:
            cache (OrderedDict): An [collections.OrderedDict][] instance.
        """

        self.maxsize = maxsize
        self.cache: OrderedDict = OrderedDict()

    def get(self, key: t.Any) -> t.Any:
        """
        get(key) -> value

        Returns:
            Either returns the value of key or None if not found.
        """
        return self.cache.get(key, None)

    def put(self, key: t.Any, value: t.Any) -> None:
        """
        put(key, value) -> None

        Adds a key-value pair to the cache. If the maximum size of the cache is reached,
        the oldest item is removed.
        """
        if len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def delete(self, key: t.Any) -> None:
        """
        delete(key) -> None

        Deletes a key-value pair from the cache.
        """
        if key in self.cache:
            del self.cache[key]

    def clear(self) -> None:
        """
        clear() -> None

        Clears the cache.
        """
        self.cache.clear()

    def __len__(self) -> int:
        """
        Returns:
            The number of items in the cache.
        """
        return len(self.cache)

    def __contains__(self, key: t.Any) -> bool:
        """
        Returns:
            Whether the cache contains the key.
        """
        return key in self.cache

    def __getitem__(self, key: t.Any) -> t.Any:
        """
        Args:
            key: The key to get the value of.

        Returns:
            The value of the key.
        """
        return self.cache[key]

    def __delitem__(self, key: t.Any) -> None:
        """
        Args:
            key: The key-value to delete.

        Deletes a key-value pair from the cache.
        """
        if key in self.cache:
            del self.cache[key]
        else:
            raise KeyError(key) from None

    def __repr__(self) -> t.Any:
        """
        Returns:
            [dict][] representation of the cache.
        """
        return str(self.cache)

    def __copy__(self) -> Cache:
        """
        Creates a shallow copy of the cache.
        """
        return self.__class__(self.cache)
