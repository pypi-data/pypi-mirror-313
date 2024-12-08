"""Health check module."""

from dataclasses import dataclass, field
from typing import Any

from ..module import BaseModule
from .config import TelemetryConfig


@dataclass
class HealthStatus:
    """Health status data."""

    name: str
    status: str
    message: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


class HealthChecker(BaseModule[TelemetryConfig]):
    """Health checker implementation."""

    def __init__(self) -> None:
        """Initialize health checker."""
        config = TelemetryConfig(name="health-checker")
        super().__init__(config)
        self._checks: dict[str, HealthStatus] = {}

    async def _setup(self) -> None:
        """Setup health checker."""
        self._checks.clear()

    async def _teardown(self) -> None:
        """Teardown health checker."""
        self._checks.clear()

    async def register_check(self, check: HealthStatus) -> None:
        """Register health check.

        Args:
            check: Health check status
        """
        if not self.is_initialized:
            await self.initialize()
        self._checks[check.name] = check

    async def get_check(self, name: str) -> HealthStatus | None:
        """Get health check status.

        Args:
            name: Check name

        Returns:
            Health check status if found, None otherwise
        """
        if not self.is_initialized:
            await self.initialize()
        return self._checks.get(name)

    async def get_stats(self) -> dict[str, Any]:
        """Get health checker statistics.

        Returns:
            Health checker statistics
        """
        if not self.is_initialized:
            await self.initialize()

        healthy_count = sum(
            1 for check in self._checks.values() if check.status == "healthy"
        )

        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "total_checks": len(self._checks),
            "healthy_checks": healthy_count,
            "unhealthy_checks": len(self._checks) - healthy_count,
            "check_names": list(self._checks.keys()),
        }
