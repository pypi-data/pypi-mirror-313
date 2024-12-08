"""Pipeline type definitions."""

from typing import Any, Protocol, TypeVar

T = TypeVar("T")


class PipelineData(Protocol):
    """Pipeline data protocol."""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        ...
