"""State management module."""

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from .exceptions import PepperpyError

T = TypeVar("T")


@dataclass
class State(Generic[T]):
    """State container."""

    value: T
    metadata: dict[str, Any] = field(default_factory=dict)


class StateError(PepperpyError):
    """State error."""

    pass


class StateManager(Generic[T]):
    """State manager implementation."""

    def __init__(self) -> None:
        """Initialize state manager."""
        self._state: State[T] | None = None

    def get_state(self) -> State[T] | None:
        """Get current state."""
        return self._state

    def set_state(self, value: T, **metadata: Any) -> None:
        """Set current state."""
        self._state = State(value=value, metadata=metadata)
