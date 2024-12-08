"""Development mocks module."""

from typing import Generic, TypeVar

T = TypeVar("T")


class MockCollector(Generic[T]):
    """Mock data collector."""

    def __init__(self) -> None:
        """Initialize collector."""
        self._calls: list[T] = []

    def record(self, data: T) -> None:
        """Record mock data."""
        self._calls.append(data)

    def get_calls(self) -> list[T]:
        """Get recorded calls."""
        return self._calls

    def clear(self) -> None:
        """Clear recorded calls."""
        self._calls.clear()
