"""Registry manager implementation."""

from dataclasses import dataclass, field
from typing import Any

from ..module import BaseModule
from .config import RegistryConfig


@dataclass
class RegistryEntry:
    """Registry entry."""

    key: str
    value: Any
    metadata: dict[str, Any] = field(default_factory=dict)


class RegistryManager(BaseModule[RegistryConfig]):
    """Registry manager implementation."""

    def __init__(self) -> None:
        """Initialize registry manager."""
        config = RegistryConfig(name="registry-manager")
        super().__init__(config)
        self._registry: dict[str, RegistryEntry] = {}

    async def _setup(self) -> None:
        """Setup registry manager."""
        self._registry.clear()

    async def _teardown(self) -> None:
        """Teardown registry manager."""
        self._registry.clear()

    async def register(self, entry: RegistryEntry) -> None:
        """Register entry.

        Args:
            entry: Registry entry
        """
        if not self.is_initialized:
            await self.initialize()
        self._registry[entry.key] = entry

    async def unregister(self, key: str) -> None:
        """Unregister entry.

        Args:
            key: Entry key
        """
        if not self.is_initialized:
            await self.initialize()
        self._registry.pop(key, None)

    async def get(self, key: str) -> Any | None:
        """Get registry value.

        Args:
            key: Entry key

        Returns:
            Entry value if found, None otherwise
        """
        if not self.is_initialized:
            await self.initialize()
        entry = self._registry.get(key)
        return entry.value if entry else None

    async def get_stats(self) -> dict[str, Any]:
        """Get registry statistics.

        Returns:
            Registry statistics
        """
        if not self.is_initialized:
            await self.initialize()
        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "entries_count": len(self._registry),
            "keys": list(self._registry.keys()),
        }
