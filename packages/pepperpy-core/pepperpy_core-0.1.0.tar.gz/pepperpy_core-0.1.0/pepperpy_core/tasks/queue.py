"""Task queue implementation."""

from collections import deque
from dataclasses import dataclass
from typing import Any

from ..module import BaseModule
from .base import TaskConfig


@dataclass
class TaskQueue(BaseModule[TaskConfig]):
    """Task queue implementation."""

    def __init__(self) -> None:
        """Initialize task queue."""
        config = TaskConfig(name="task-queue")
        super().__init__(config)
        self._queue: deque[Any] = deque()

    async def _setup(self) -> None:
        """Setup task queue."""
        self._queue.clear()

    async def _teardown(self) -> None:
        """Teardown task queue."""
        self._queue.clear()

    async def push(self, task: Any) -> None:
        """Push task to queue.

        Args:
            task: Task to push
        """
        if not self.is_initialized:
            await self.initialize()
        self._queue.append(task)

    async def pop(self) -> Any | None:
        """Pop task from queue.

        Returns:
            Task if queue not empty, None otherwise
        """
        if not self.is_initialized:
            await self.initialize()
        return self._queue.popleft() if self._queue else None

    async def get_stats(self) -> dict[str, Any]:
        """Get queue statistics.

        Returns:
            Queue statistics
        """
        if not self.is_initialized:
            await self.initialize()

        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "queue_size": len(self._queue),
        }
