"""Metrics exceptions."""

from ..exceptions import PepperpyError


class MetricError(PepperpyError):
    """Base metric error."""


class CollectorError(MetricError):
    """Metric collector error."""


class MetricValueError(MetricError):
    """Metric value error."""


__all__ = [
    "MetricError",
    "CollectorError",
    "MetricValueError",
]
