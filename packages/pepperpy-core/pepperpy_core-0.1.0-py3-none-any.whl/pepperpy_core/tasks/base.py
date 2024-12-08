"""Base task implementation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData
from ..module import BaseModule


@dataclass
class TaskConfig(BaseConfigData):
    """Task configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    enabled: bool = True
    max_retries: int = 3
    timeout: float = 60.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate configuration."""
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.timeout <= 0:
            raise ValueError("timeout must be greater than 0")


class BaseTask(BaseModule[TaskConfig], ABC):
    """Base task implementation."""

    def __init__(self) -> None:
        """Initialize task."""
        config = TaskConfig(name="base-task")
        super().__init__(config)
        self._result: Any = None

    async def _setup(self) -> None:
        """Setup task resources."""
        self._result = None

    async def _teardown(self) -> None:
        """Teardown task resources."""
        self._result = None

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute task.

        Args:
            *args: Task arguments
            **kwargs: Task keyword arguments

        Returns:
            Task result
        """
        pass

    async def get_stats(self) -> dict[str, Any]:
        """Get task statistics.

        Returns:
            Task statistics
        """
        if not self.is_initialized:
            await self.initialize()

        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "max_retries": self.config.max_retries,
            "timeout": self.config.timeout,
            "has_result": self._result is not None,
        }
