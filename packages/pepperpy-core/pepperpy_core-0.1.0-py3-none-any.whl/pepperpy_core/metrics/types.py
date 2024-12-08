"""Metrics types."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MetricsConfig:
    """Metrics configuration."""

    name: str = ""
    enabled: bool = True
    collection_interval: float = 60.0
    retention_period: float = 3600.0
    metadata: dict[str, Any] = field(default_factory=dict)
