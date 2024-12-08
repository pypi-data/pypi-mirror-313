"""Pipeline manager module."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData, BaseManager


@dataclass
class PipelineConfig(BaseConfigData):
    """Pipeline configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str = "pipeline-manager"

    # Optional fields
    enabled: bool = True
    max_concurrent: int = 10
    timeout: float = 60.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate configuration."""
        if self.max_concurrent < 1:
            raise ValueError("max_concurrent must be greater than 0")
        if self.timeout <= 0:
            raise ValueError("timeout must be greater than 0")


class PipelineManager(BaseManager[PipelineConfig]):
    """Pipeline manager implementation."""

    def __init__(self) -> None:
        """Initialize pipeline manager."""
        config = PipelineConfig()
        super().__init__(config)
        self._active_pipelines: dict[str, Any] = {}

    async def _setup(self) -> None:
        """Setup pipeline manager."""
        await super()._setup()
        self._active_pipelines.clear()

    async def _teardown(self) -> None:
        """Teardown pipeline manager."""
        await super()._teardown()
        self._active_pipelines.clear()

    async def get_stats(self) -> dict[str, Any]:
        """Get pipeline manager statistics.

        Returns:
            Pipeline manager statistics
        """
        stats = await super().get_stats()
        stats.update(
            {
                "active_pipelines": len(self._active_pipelines),
                "max_concurrent": self.config.max_concurrent,
                "timeout": self.config.timeout,
            }
        )
        return stats
