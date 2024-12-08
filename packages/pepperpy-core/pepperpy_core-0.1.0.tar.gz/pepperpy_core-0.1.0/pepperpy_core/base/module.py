"""Base module implementation."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from .config import BaseConfigData

ConfigT = TypeVar("ConfigT", bound=BaseConfigData)


class BaseModule(ABC, Generic[ConfigT]):
    """Base module class."""

    def __init__(self, config: ConfigT) -> None:
        """Initialize module.

        Args:
            config: Module configuration
        """
        self.config = config
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize module."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup module resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    @abstractmethod
    async def _setup(self) -> None:
        """Setup module resources."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown module resources."""
        pass

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """Get module statistics.

        Returns:
            Module statistics

        Raises:
            RuntimeError: If module is not initialized
        """
        if not self._initialized:
            raise RuntimeError("Module not initialized")
        return {}

    @property
    def is_initialized(self) -> bool:
        """Check if module is initialized."""
        return self._initialized

    def _ensure_initialized(self) -> None:
        """Ensure module is initialized.

        Raises:
            RuntimeError: If module is not initialized
        """
        if not self._initialized:
            raise RuntimeError("Module not initialized")


class BaseManager(BaseModule[ConfigT], ABC):
    """Base manager implementation."""

    def __init__(self, config: ConfigT) -> None:
        """Initialize manager.

        Args:
            config: Manager configuration
        """
        super().__init__(config)
        self._items: dict[str, Any] = {}

    async def _setup(self) -> None:
        """Setup manager resources."""
        self._items.clear()

    async def _teardown(self) -> None:
        """Teardown manager resources."""
        self._items.clear()

    async def get_stats(self) -> dict[str, Any]:
        """Get manager statistics.

        Returns:
            Manager statistics
        """
        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "items_count": len(self._items),
            "item_names": list(self._items.keys()),
        }


class InitializableModule(BaseModule[ConfigT], ABC):
    """Initializable module implementation."""

    def _ensure_initialized(self) -> None:
        """Ensure module is initialized."""
        if not self.is_initialized:
            raise RuntimeError("Module not initialized")
