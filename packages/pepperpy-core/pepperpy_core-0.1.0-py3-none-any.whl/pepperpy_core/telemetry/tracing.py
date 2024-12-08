"""Telemetry tracing module."""

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any

from ..exceptions import PepperpyError
from ..module import BaseModule
from .config import TelemetryConfig


class TracingError(PepperpyError):
    """Tracing specific error."""

    pass


@dataclass
class TraceSpan:
    """Trace span data."""

    name: str
    start_time: float = field(default_factory=perf_counter)
    end_time: float | None = None
    parent_id: str | None = None
    tags: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def duration(self) -> float | None:
        """Get span duration.

        Returns:
            Duration in seconds if span is complete, None otherwise
        """
        if self.end_time is None:
            return None
        return self.end_time - self.start_time


class TracingCollector(BaseModule[TelemetryConfig]):
    """Tracing collector implementation."""

    def __init__(self) -> None:
        """Initialize tracing collector."""
        config = TelemetryConfig(name="tracing-collector")
        super().__init__(config)
        self._spans: dict[str, TraceSpan] = {}
        self._active_spans: list[str] = []

    async def _setup(self) -> None:
        """Setup tracing collector."""
        self._spans.clear()
        self._active_spans.clear()

    async def _teardown(self) -> None:
        """Teardown tracing collector."""
        self._spans.clear()
        self._active_spans.clear()

    async def start_span(
        self,
        name: str,
        parent_id: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> str:
        """Start trace span.

        Args:
            name: Span name
            parent_id: Optional parent span ID
            tags: Optional span tags

        Returns:
            Span ID
        """
        if not self.is_initialized:
            await self.initialize()

        span_id = f"{name}_{len(self._spans)}"
        span = TraceSpan(
            name=name,
            parent_id=parent_id,
            tags=tags or {},
        )

        self._spans[span_id] = span
        self._active_spans.append(span_id)

        if len(self._spans) > self.config.buffer_size:
            # Remove oldest completed spans
            completed = [
                sid for sid, span in self._spans.items() if span.end_time is not None
            ]
            for sid in completed[: -self.config.buffer_size]:
                del self._spans[sid]

        return span_id

    async def end_span(self, span_id: str) -> None:
        """End trace span.

        Args:
            span_id: Span ID

        Raises:
            TracingError: If span not found
        """
        if not self.is_initialized:
            await self.initialize()

        span = self._spans.get(span_id)
        if span is None:
            raise TracingError(f"Span {span_id} not found")

        span.end_time = perf_counter()
        if span_id in self._active_spans:
            self._active_spans.remove(span_id)

    async def get_stats(self) -> dict[str, Any]:
        """Get tracing collector statistics.

        Returns:
            Tracing collector statistics
        """
        if not self.is_initialized:
            await self.initialize()

        completed_spans = sum(
            1 for span in self._spans.values() if span.end_time is not None
        )

        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "total_spans": len(self._spans),
            "active_spans": len(self._active_spans),
            "completed_spans": completed_spans,
            "buffer_size": self.config.buffer_size,
            "flush_interval": self.config.flush_interval,
        }
