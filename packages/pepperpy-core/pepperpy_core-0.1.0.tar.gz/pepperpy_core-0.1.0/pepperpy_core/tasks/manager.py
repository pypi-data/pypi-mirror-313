"""Task manager module."""

from collections.abc import Callable
from typing import Any

from ..base import BaseModule
from .config import TaskConfig
from .task import Task


class TaskManager(BaseModule[TaskConfig]):
    """Task manager implementation."""

    def __init__(self) -> None:
        """Initialize task manager."""
        config = TaskConfig(name="task_manager")
        super().__init__(config)
        self._tasks: dict[str, Task] = {}

    async def _setup(self) -> None:
        """Setup task manager."""
        self._tasks.clear()

    async def _teardown(self) -> None:
        """Teardown task manager."""
        for task in self._tasks.values():
            await task.cancel()
        self._tasks.clear()

    async def get_stats(self) -> dict[str, Any]:
        """Get task manager statistics."""
        self._ensure_initialized()
        return {
            "total_tasks": len(self._tasks),
            "task_names": list(self._tasks.keys()),
            "active_tasks": sum(1 for t in self._tasks.values() if not t.is_cancelled),
        }

    async def create_task(
        self, name: str, func: Callable[..., Any], **kwargs: Any
    ) -> Task:
        """Create a new task.

        Args:
            name: Task name
            func: Task function
            **kwargs: Additional task arguments

        Returns:
            Created task
        """
        self._ensure_initialized()
        task = Task(name=name, func=func, **kwargs)
        self._tasks[task.name] = task
        return task
