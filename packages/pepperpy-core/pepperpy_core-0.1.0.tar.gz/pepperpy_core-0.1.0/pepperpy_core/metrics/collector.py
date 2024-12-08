"""Metrics collector implementation."""

from typing import Any

from .base import MetricsCollector, MetricsConfig


class SimpleMetricsCollector(MetricsCollector):
    """Simple metrics collector implementation."""

    def __init__(self) -> None:
        """Initialize collector."""
        super().__init__(MetricsConfig(name="simple-metrics"))

    async def _setup(self) -> None:
        """Setup collector."""
        await super()._setup()

    async def _teardown(self) -> None:
        """Teardown collector."""
        await super()._teardown()

    async def get_stats(self) -> dict[str, Any]:
        """Get collector statistics."""
        return await super().get_stats()
