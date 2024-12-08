"""Base cache implementation."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from ..base import BaseConfigData

ConfigT = TypeVar("ConfigT", bound=BaseConfigData)


class BaseCache(Generic[ConfigT], ABC):
    """Base cache implementation."""

    def __init__(self, config: ConfigT) -> None:
        """Initialize cache.

        Args:
            config: Cache configuration
        """
        self.config = config
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if cache is initialized."""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize cache."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup cache resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    @abstractmethod
    async def _setup(self) -> None:
        """Setup cache resources."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown cache resources."""
        pass

    @abstractmethod
    async def get(self, key: str) -> Any:
        """Get value from cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete value from cache."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all values from cache."""
        pass
