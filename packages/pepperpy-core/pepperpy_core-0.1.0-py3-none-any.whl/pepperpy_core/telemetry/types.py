"""Telemetry types."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any

from pepperpy_core.base.types import JsonDict


class TelemetryLevel(Enum):
    """Telemetry level types."""

    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


@dataclass
class TelemetryEvent:
    """Telemetry event data."""

    name: str
    level: TelemetryLevel
    timestamp: datetime = field(default_factory=datetime.now)
    data: str | dict[str, Any] = field(default_factory=dict)
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class TelemetryMetric:
    """Telemetry metric data."""

    name: str
    value: int | float
    unit: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class TelemetryTrace:
    """Telemetry trace data."""

    name: str
    duration: float
    start_time: datetime
    end_time: datetime
    parent_id: str | None = None
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class TelemetrySpan:
    """Telemetry span data."""

    name: str
    trace_id: str
    parent_id: str | None = None
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    metadata: JsonDict = field(default_factory=dict)

    @property
    def duration(self) -> float | None:
        """Get span duration in seconds."""
        if not self.end_time:
            return None
        return (self.end_time - self.start_time).total_seconds()
