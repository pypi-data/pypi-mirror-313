"""Memory cache implementation."""

from typing import Any

from .exceptions import CacheError


class MemoryCache:
    """Simple in-memory cache implementation."""

    def __init__(self) -> None:
        """Initialize memory cache."""
        self._cache: dict[str, Any] = {}

    def get(self, key: str) -> Any | None:
        """Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value if found, None otherwise

        Raises:
            CacheError: If get operation fails
        """
        try:
            return self._cache.get(key)
        except Exception as e:
            raise CacheError(f"Failed to get value: {e}", cause=e)

    def set(self, key: str, value: Any, ttl: int | float | None = None) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds

        Raises:
            CacheError: If set operation fails
        """
        try:
            self._cache[key] = value
        except Exception as e:
            raise CacheError(f"Failed to set value: {e}", cause=e)
