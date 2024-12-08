"""Event system implementation."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from .exceptions import PepperpyError


class EventError(PepperpyError):
    """Event system error."""

    pass


@dataclass
class Event:
    """Event data."""

    name: str
    data: Any
    metadata: dict[str, Any] = field(default_factory=dict)


EventHandler = Callable[[Event], None]


class EventManager:
    """Event manager implementation."""

    def __init__(self) -> None:
        """Initialize event manager."""
        self._handlers: dict[str, list[EventHandler]] = {}
        self._initialized: bool = False

    def initialize(self) -> None:
        """Initialize event manager."""
        if self._initialized:
            return
        self._initialized = True

    def cleanup(self) -> None:
        """Cleanup event manager."""
        if not self._initialized:
            return
        self._handlers.clear()
        self._initialized = False

    def subscribe(self, event_name: str, handler: EventHandler | None = None) -> None:
        """Subscribe to event.

        Args:
            event_name: Event name
            handler: Event handler

        Raises:
            EventError: If event manager not initialized
        """
        if not self._initialized:
            raise EventError("Event manager not initialized")

        if event_name not in self._handlers:
            self._handlers[event_name] = []

        if handler:
            self._handlers[event_name].append(handler)

    def unsubscribe(self, event_name: str, handler: EventHandler | None = None) -> None:
        """Unsubscribe from event.

        Args:
            event_name: Event name
            handler: Event handler

        Raises:
            EventError: If event manager not initialized
        """
        if not self._initialized:
            raise EventError("Event manager not initialized")

        if event_name not in self._handlers:
            return

        if handler:
            self._handlers[event_name].remove(handler)
        else:
            self._handlers[event_name].clear()

    def emit(self, event: Event) -> None:
        """Emit event.

        Args:
            event: Event data

        Raises:
            EventError: If event manager not initialized
        """
        if not self._initialized:
            raise EventError("Event manager not initialized")

        if event.name not in self._handlers:
            return

        for handler in self._handlers[event.name]:
            try:
                handler(event)
            except Exception as e:
                raise EventError(f"Event handler failed: {e}", cause=e)
