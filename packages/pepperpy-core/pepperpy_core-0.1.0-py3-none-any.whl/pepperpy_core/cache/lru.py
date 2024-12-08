"""LRU cache implementation"""

from collections import OrderedDict
from typing import Generic, TypeVar

from .exceptions import CacheError

KT = TypeVar("KT")
VT = TypeVar("VT")


class LRUCache(Generic[KT, VT]):
    """LRU (Least Recently Used) cache implementation"""

    def __init__(self, capacity: int):
        """
        Initialize LRU cache

        Args:
            capacity: Maximum number of items to store

        """
        self.capacity = capacity
        self._cache: OrderedDict[KT, VT] = OrderedDict()

    def get(self, key: KT) -> VT | None:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Optional[VT]: Cached value if exists

        """
        try:
            if key not in self._cache:
                return None
            value = self._cache.pop(key)
            self._cache[key] = value
            return value
        except Exception as e:
            raise CacheError(f"Failed to get value: {e!s}", cause=e)

    def put(self, key: KT, value: VT) -> None:
        """
        Put value in cache

        Args:
            key: Cache key
            value: Value to cache

        """
        try:
            if key in self._cache:
                self._cache.pop(key)
            elif len(self._cache) >= self.capacity:
                self._cache.popitem(last=False)
            self._cache[key] = value
        except Exception as e:
            raise CacheError(f"Failed to put value: {e!s}", cause=e)

    def remove(self, key: KT) -> None:
        """
        Remove value from cache

        Args:
            key: Cache key

        """
        try:
            if key in self._cache:
                self._cache.pop(key)
        except Exception as e:
            raise CacheError(f"Failed to remove value: {e!s}", cause=e)

    def clear(self) -> None:
        """Clear all values from cache"""
        try:
            self._cache.clear()
        except Exception as e:
            raise CacheError(f"Failed to clear cache: {e!s}", cause=e)

    @property
    def size(self) -> int:
        """Get current cache size"""
        return len(self._cache)

    def __contains__(self, key: KT) -> bool:
        """Check if key exists in cache"""
        return key in self._cache

    def __len__(self) -> int:
        """Get current cache size"""
        return len(self._cache)
