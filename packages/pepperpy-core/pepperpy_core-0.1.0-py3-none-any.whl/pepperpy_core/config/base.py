"""Base configuration implementation."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from ..base import BaseConfigData

ConfigT = TypeVar("ConfigT", bound=BaseConfigData)


class BaseConfig(Generic[ConfigT], ABC):
    """Base configuration."""

    def __init__(self, config: ConfigT) -> None:
        """Initialize configuration.

        Args:
            config: Configuration data
        """
        self.config = config
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if configuration is initialized."""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize configuration."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup configuration resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    @abstractmethod
    async def _setup(self) -> None:
        """Setup configuration resources."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown configuration resources."""
        pass

    @abstractmethod
    async def load(self, path: str) -> None:
        """Load configuration from file."""
        pass

    @abstractmethod
    async def save(self, path: str) -> None:
        """Save configuration to file."""
        pass

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """Get configuration statistics."""
        pass
