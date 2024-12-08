"""Base manager implementation."""

from abc import ABC, abstractmethod
from typing import Any


class BaseManager(ABC):
    """Base class for managers."""

    def __init__(self) -> None:
        """Initialize manager."""
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize manager resources."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup manager resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    def _ensure_initialized(self) -> None:
        """Ensure manager is initialized.

        Raises:
            RuntimeError: If manager not initialized
        """
        if not self._initialized:
            raise RuntimeError("Manager not initialized")

    @abstractmethod
    async def _setup(self) -> None:
        """Setup manager resources."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown manager resources."""
        pass

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """Get manager statistics.

        Returns:
            Manager statistics
        """
        pass
