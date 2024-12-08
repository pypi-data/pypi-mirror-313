"""Plugin type definitions."""

from dataclasses import dataclass, field
from typing import Any, Protocol, TypeVar

T = TypeVar("T")


class PluginProtocol(Protocol):
    """Plugin protocol definition."""

    async def initialize(self) -> None:
        """Initialize plugin."""
        ...

    async def cleanup(self) -> None:
        """Cleanup plugin."""
        ...

    async def execute(self, **kwargs: Any) -> Any:
        """Execute plugin functionality."""
        ...


@dataclass
class PluginMetadata:
    """Plugin metadata."""

    name: str
    version: str
    description: str = ""
    author: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
