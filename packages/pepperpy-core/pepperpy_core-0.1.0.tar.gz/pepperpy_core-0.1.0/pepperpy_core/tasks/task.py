"""Task implementation."""

from collections.abc import Callable
from typing import Any
from uuid import uuid4


class Task:
    """Task implementation."""

    def __init__(self, name: str, func: Callable[..., Any], **kwargs: Any) -> None:
        """Initialize task.

        Args:
            name: Task name
            func: Task function
            **kwargs: Additional task arguments
        """
        self.id = uuid4()
        self.name = name
        self._func = func
        self._kwargs = kwargs
        self._cancelled = False
        self._result: Any = None
        self._error: Exception | None = None

    async def execute(self) -> Any:
        """Execute task.

        Returns:
            Task result

        Raises:
            Exception: If task execution fails
        """
        if self._cancelled:
            raise RuntimeError("Task was cancelled")

        try:
            self._result = self._func(**self._kwargs)
            return self._result
        except Exception as e:
            self._error = e
            raise

    async def cancel(self) -> None:
        """Cancel task."""
        self._cancelled = True

    @property
    def is_cancelled(self) -> bool:
        """Check if task is cancelled."""
        return self._cancelled

    @property
    def result(self) -> Any:
        """Get task result."""
        return self._result

    @property
    def error(self) -> Exception | None:
        """Get task error."""
        return self._error
