"""Telemetry configuration."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData


@dataclass
class TelemetryConfig(BaseConfigData):
    """Telemetry configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    enabled: bool = True
    buffer_size: int = 1000
    flush_interval: float = 60.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate configuration."""
        if self.buffer_size < 1:
            raise ValueError("buffer_size must be greater than 0")
        if self.flush_interval <= 0:
            raise ValueError("flush_interval must be greater than 0")

    def get_stats(self) -> dict[str, Any]:
        """Get configuration statistics."""
        return {
            "name": self.name,
            "enabled": self.enabled,
            "buffer_size": self.buffer_size,
            "flush_interval": self.flush_interval,
            "metadata": self.metadata,
        }


__all__ = ["TelemetryConfig"]
