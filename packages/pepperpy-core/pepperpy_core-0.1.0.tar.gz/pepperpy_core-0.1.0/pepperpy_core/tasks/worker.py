"""Task worker implementation."""

from typing import Any

from ..module import BaseModule
from .base import TaskConfig


class TaskWorker(BaseModule[TaskConfig]):
    """Task worker implementation."""

    def __init__(self) -> None:
        """Initialize task worker."""
        config = TaskConfig(name="task-worker")
        super().__init__(config)
        self._active: bool = False

    async def _setup(self) -> None:
        """Setup task worker."""
        self._active = False

    async def _teardown(self) -> None:
        """Teardown task worker."""
        self._active = False

    async def start(self) -> None:
        """Start worker."""
        if not self.is_initialized:
            await self.initialize()
        self._active = True

    async def stop(self) -> None:
        """Stop worker."""
        if not self.is_initialized:
            await self.initialize()
        self._active = False

    async def get_stats(self) -> dict[str, Any]:
        """Get worker statistics.

        Returns:
            Worker statistics
        """
        if not self.is_initialized:
            await self.initialize()

        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "active": self._active,
        }
