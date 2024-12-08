"""Network types."""

from dataclasses import dataclass, field
from typing import Any, Protocol

from ..types import JsonDict


@dataclass
class NetworkRequest:
    """Network request."""

    url: str
    method: str = "GET"
    headers: dict[str, str] = field(default_factory=dict)
    params: dict[str, str] = field(default_factory=dict)
    data: Any | None = None
    timeout: float = 30.0
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class NetworkResponse:
    """Network response."""

    status: int
    data: Any
    headers: dict[str, str] = field(default_factory=dict)
    metadata: JsonDict = field(default_factory=dict)


class NetworkWebSocket(Protocol):
    """Network WebSocket protocol."""

    async def connect(self) -> None:
        """Connect to WebSocket."""
        ...

    async def send(self, data: Any) -> None:
        """Send data through WebSocket."""
        ...

    async def receive(self) -> Any:
        """Receive data from WebSocket."""
        ...

    async def close(self) -> None:
        """Close WebSocket connection."""
        ...
