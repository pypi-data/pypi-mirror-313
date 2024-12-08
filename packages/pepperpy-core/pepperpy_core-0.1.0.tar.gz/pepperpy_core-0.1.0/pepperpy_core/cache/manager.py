"""Cache management module."""

from dataclasses import dataclass, field
from typing import Any

from ..module import BaseModule, ModuleConfig


@dataclass
class CacheManagerConfig(ModuleConfig):
    """Cache manager configuration."""

    # Required fields (herdado de ModuleConfig)
    name: str

    # Optional fields
    max_size: int = 1000
    ttl: float = 60.0  # Time to live in seconds
    metadata: dict[str, Any] = field(default_factory=dict)


class CacheManager(BaseModule[CacheManagerConfig]):
    """Cache manager implementation."""

    def __init__(self, config: CacheManagerConfig | None = None) -> None:
        """Initialize cache manager.

        Args:
            config: Cache manager configuration
        """
        super().__init__(config or CacheManagerConfig(name="cache-manager"))
        self._cache: dict[str, Any] = {}

    async def _setup(self) -> None:
        """Setup cache manager."""
        self._cache.clear()

    async def _teardown(self) -> None:
        """Cleanup cache manager."""
        self._cache.clear()

    async def get(self, key: str) -> Any:
        """Get cache entry.

        Args:
            key: Cache key

        Returns:
            Cache entry if found, None otherwise
        """
        if not self.is_initialized:
            await self.initialize()
        return self._cache.get(key)

    async def set(self, key: str, value: Any) -> None:
        """Set cache entry.

        Args:
            key: Cache key
            value: Cache value
        """
        if not self.is_initialized:
            await self.initialize()
        self._cache[key] = value

    async def delete(self, key: str) -> None:
        """Delete cache entry.

        Args:
            key: Cache key
        """
        if not self.is_initialized:
            await self.initialize()
        self._cache.pop(key, None)

    async def clear(self) -> None:
        """Clear all cache entries."""
        if not self.is_initialized:
            await self.initialize()
        self._cache.clear()

    async def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            Cache statistics
        """
        if not self.is_initialized:
            await self.initialize()
        return {
            "size": len(self._cache),
            "max_size": self.config.max_size,
            "ttl": self.config.ttl,
        }
