"""Distributed cache implementation."""

import importlib.util
from typing import Any, Protocol, runtime_checkable

# Verificar disponibilidade do Redis
_redis_spec = importlib.util.find_spec("redis")
has_redis = bool(_redis_spec)


@runtime_checkable
class CacheBackend(Protocol):
    """Cache backend protocol."""

    def get(self, key: str) -> Any:
        ...

    def set(self, key: str, value: Any) -> None:
        ...


class DistributedCache:
    """Distributed cache implementation."""

    def __init__(self) -> None:
        """Initialize distributed cache."""
        if not has_redis:
            raise ImportError(
                "Redis is not installed. Please install it with `pip install redis`"
            )
        self._client: CacheBackend | None = None

    def get(self, key: str) -> Any:
        """Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value
        """
        if self._client is None:
            raise RuntimeError("Cache not initialized")
        return self._client.get(key)

    def set(self, key: str, value: Any) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        if self._client is None:
            raise RuntimeError("Cache not initialized")
        self._client.set(key, value)
