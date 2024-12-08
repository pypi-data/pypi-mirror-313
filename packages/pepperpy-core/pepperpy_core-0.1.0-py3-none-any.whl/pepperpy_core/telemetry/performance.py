"""Performance monitoring module."""

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any

from ..exceptions import PepperpyError
from ..module import BaseModule
from .config import TelemetryConfig


class PerformanceError(PepperpyError):
    """Performance specific error."""

    pass


@dataclass
class PerformanceMetric:
    """Performance metric data."""

    name: str
    value: float
    unit: str
    timestamp: float = field(default_factory=perf_counter)
    metadata: dict[str, Any] = field(default_factory=dict)


class PerformanceMonitor(BaseModule[TelemetryConfig]):
    """Performance monitor implementation."""

    def __init__(self) -> None:
        """Initialize performance monitor."""
        config = TelemetryConfig(name="performance-monitor")
        super().__init__(config)
        self._metrics: list[PerformanceMetric] = []

    async def _setup(self) -> None:
        """Setup performance monitor."""
        self._metrics.clear()

    async def _teardown(self) -> None:
        """Teardown performance monitor."""
        self._metrics.clear()

    async def record_metric(
        self, name: str, value: float, unit: str, metadata: dict[str, Any] | None = None
    ) -> None:
        """Record performance metric.

        Args:
            name: Metric name
            value: Metric value
            unit: Metric unit
            metadata: Optional metric metadata
        """
        if not self.is_initialized:
            await self.initialize()

        if len(self._metrics) >= self.config.buffer_size:
            self._metrics.pop(0)

        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            metadata=metadata or {},
        )
        self._metrics.append(metric)

    async def get_stats(self) -> dict[str, Any]:
        """Get performance monitor statistics.

        Returns:
            Performance monitor statistics
        """
        if not self.is_initialized:
            await self.initialize()

        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "total_samples": len(self._metrics),
            "buffer_size": self.config.buffer_size,
            "flush_interval": self.config.flush_interval,
            "metric_names": {m.name for m in self._metrics},
        }
