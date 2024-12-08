"""Base metrics implementation."""

from dataclasses import dataclass, field
from typing import Any

from ..module import BaseModule, ModuleConfig


@dataclass
class MetricsConfig(ModuleConfig):
    """Metrics configuration."""

    # Required fields (herdado de ModuleConfig)
    name: str

    # Optional fields
    enabled: bool = True
    interval: float = 60.0  # Collection interval in seconds
    buffer_size: int = 1000  # Maximum number of metrics to buffer
    metadata: dict[str, Any] = field(default_factory=dict)


class MetricsCollector(BaseModule[MetricsConfig]):
    """Base metrics collector implementation."""

    def __init__(self, config: MetricsConfig | None = None) -> None:
        """Initialize metrics collector.

        Args:
            config: Metrics configuration
        """
        super().__init__(config or MetricsConfig(name="metrics-collector"))
        self._metrics: dict[str, Any] = {}
        self._count: int = 0

    async def _setup(self) -> None:
        """Setup metrics collector."""
        self._metrics.clear()
        self._count = 0

    async def _teardown(self) -> None:
        """Cleanup metrics collector."""
        self._metrics.clear()
        self._count = 0

    async def collect(
        self, name: str, value: Any, tags: dict[str, str] | None = None
    ) -> None:
        """Collect metric.

        Args:
            name: Metric name
            value: Metric value
            tags: Optional metric tags
        """
        if not self.is_initialized:
            await self.initialize()

        if not self.config.enabled:
            return

        self._metrics[name] = {
            "value": value,
            "tags": tags or {},
            "timestamp": self._count,
        }
        self._count += 1

        # Buffer management
        if len(self._metrics) > self.config.buffer_size:
            # Remove oldest metrics
            sorted_metrics = sorted(
                self._metrics.items(), key=lambda x: x[1]["timestamp"]
            )
            for name, _ in sorted_metrics[: -self.config.buffer_size]:
                del self._metrics[name]

    async def get_stats(self) -> dict[str, Any]:
        """Get metrics statistics.

        Returns:
            Metrics statistics
        """
        if not self.is_initialized:
            await self.initialize()

        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "interval": self.config.interval,
            "buffer_size": self.config.buffer_size,
            "metrics_count": len(self._metrics),
            "total_collected": self._count,
        }
