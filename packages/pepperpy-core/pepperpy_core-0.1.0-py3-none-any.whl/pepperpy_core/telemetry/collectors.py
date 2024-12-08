"""Telemetry collectors module."""

from typing import Any

from ..exceptions import PepperpyError
from ..module import BaseModule
from .config import TelemetryConfig


class TelemetryError(PepperpyError):
    """Telemetry specific error."""

    pass


class TelemetryCollector(BaseModule[TelemetryConfig]):
    """Telemetry collector implementation."""

    def __init__(self) -> None:
        """Initialize telemetry collector."""
        config = TelemetryConfig(name="telemetry-collector")
        super().__init__(config)
        self._metrics: list[dict[str, Any]] = []

    async def _setup(self) -> None:
        """Setup telemetry collector."""
        self._metrics.clear()

    async def _teardown(self) -> None:
        """Teardown telemetry collector."""
        await self.flush()
        self._metrics.clear()

    async def collect(self, metric: dict[str, Any]) -> None:
        """Collect metric.

        Args:
            metric: Metric data to collect
        """
        if not self.is_initialized:
            await self.initialize()
        if len(self._metrics) >= self.config.buffer_size:
            await self.flush()
        self._metrics.append(metric)

    async def flush(self) -> None:
        """Flush collected metrics."""
        if not self.is_initialized:
            await self.initialize()
        # Implementation for sending metrics to telemetry service would go here
        self._metrics.clear()

    async def get_stats(self) -> dict[str, Any]:
        """Get telemetry collector statistics.

        Returns:
            Telemetry collector statistics
        """
        if not self.is_initialized:
            await self.initialize()
        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "buffered_metrics": len(self._metrics),
            "buffer_size": self.config.buffer_size,
            "flush_interval": self.config.flush_interval,
        }
