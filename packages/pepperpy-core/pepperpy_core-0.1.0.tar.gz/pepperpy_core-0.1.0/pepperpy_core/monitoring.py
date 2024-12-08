"""Monitoring utilities."""

from typing import Protocol, TypeVar


# Define protocol for prometheus types
class CounterProtocol(Protocol):
    def inc(self, amount: float = 1.0) -> None:
        ...

    def labels(self, **kwargs: str) -> "CounterProtocol":
        ...


class HistogramProtocol(Protocol):
    def observe(self, amount: float) -> None:
        ...

    def labels(self, **kwargs: str) -> "HistogramProtocol":
        ...


# Type variables for prometheus types
C = TypeVar("C", bound=CounterProtocol)
H = TypeVar("H", bound=HistogramProtocol)

# Try importing prometheus
try:
    from prometheus_client import (
        Counter as PromCounter,
        Histogram as PromHistogram,
        start_http_server as prom_start_server,
    )

    prometheus_available = True
except ImportError:
    prometheus_available = False
    PromCounter = None  # type: ignore
    PromHistogram = None  # type: ignore
    prom_start_server = None  # type: ignore

# Type aliases
Counter = type[CounterProtocol] if prometheus_available else None
Histogram = type[HistogramProtocol] if prometheus_available else None

# Component initialization time histogram
COMPONENT_INIT_TIME: HistogramProtocol | None = (
    PromHistogram(
        "component_init_time_seconds",
        "Time spent initializing components",
        ["component_name"],
    )
    if prometheus_available and PromHistogram
    else None
)

# Component cleanup time histogram
COMPONENT_CLEANUP_TIME: HistogramProtocol | None = (
    PromHistogram(
        "component_cleanup_time_seconds",
        "Time spent cleaning up components",
        ["component_name"],
    )
    if prometheus_available and PromHistogram
    else None
)

# Render time histogram
RENDER_TIME: HistogramProtocol | None = (
    PromHistogram("render_time_seconds", "Time spent rendering", ["template_name"])
    if prometheus_available and PromHistogram
    else None
)

# Error counter
ERROR_COUNT: CounterProtocol | None = (
    PromCounter("error_count", "Number of errors", ["error_type"])
    if prometheus_available and PromCounter
    else None
)


def start_metrics_server(port: int = 8000) -> None:
    """Start metrics server.

    Args:
        port: Server port
    """
    if prometheus_available and prom_start_server:
        prom_start_server(port)


def record_error(error_type: str) -> None:
    """Record error.

    Args:
        error_type: Type of error
    """
    if ERROR_COUNT:
        ERROR_COUNT.labels(error_type=error_type).inc()
