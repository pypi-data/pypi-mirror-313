"""Telemetry metrics module."""

from dataclasses import dataclass, field
from typing import Any

from ..exceptions import PepperpyError
from ..module import BaseModule
from .config import TelemetryConfig


class MetricsError(PepperpyError):
    """Metrics specific error."""

    pass


@dataclass
class MetricData:
    """Metric data."""

    name: str
    value: float
    tags: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class MetricsCollector(BaseModule[TelemetryConfig]):
    """Metrics collector implementation."""

    def __init__(self) -> None:
        """Initialize metrics collector."""
        config = TelemetryConfig(name="metrics-collector")
        super().__init__(config)
        self._metrics: dict[str, list[MetricData]] = {}

    async def _setup(self) -> None:
        """Setup metrics collector."""
        self._metrics.clear()

    async def _teardown(self) -> None:
        """Teardown metrics collector."""
        self._metrics.clear()

    async def collect(
        self, name: str, value: float, tags: dict[str, str] | None = None
    ) -> None:
        """Collect metric.

        Args:
            name: Metric name
            value: Metric value
            tags: Optional metric tags
        """
        if not self.is_initialized:
            await self.initialize()

        if name not in self._metrics:
            self._metrics[name] = []

        metric = MetricData(
            name=name,
            value=value,
            tags=tags or {},
        )

        metrics = self._metrics[name]
        metrics.append(metric)

        if len(metrics) > self.config.buffer_size:
            self._metrics[name] = metrics[-self.config.buffer_size :]

    async def get_stats(self) -> dict[str, Any]:
        """Get metrics collector statistics.

        Returns:
            Metrics collector statistics
        """
        if not self.is_initialized:
            await self.initialize()

        total_metrics = sum(len(metrics) for metrics in self._metrics.values())

        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "total_metrics": total_metrics,
            "metric_names": list(self._metrics.keys()),
            "buffer_size": self.config.buffer_size,
            "flush_interval": self.config.flush_interval,
        }
