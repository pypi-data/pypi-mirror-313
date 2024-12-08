"""Validation configuration module."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData
from ..module import BaseModule


@dataclass
class ValidationConfig(BaseConfigData):
    """Validation configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    enabled: bool = True
    strict_mode: bool = False
    cache_size: int = 1000
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate configuration."""
        if self.cache_size < 0:
            raise ValueError("cache_size must be non-negative")


class ValidationConfigManager(BaseModule[ValidationConfig]):
    """Validation configuration manager implementation."""

    def __init__(self) -> None:
        """Initialize validation configuration manager."""
        config = ValidationConfig(name="validation-config")
        super().__init__(config)
        self._validators: dict[str, dict[str, Any]] = {}
        self._cache: dict[str, Any] = {}

    async def _setup(self) -> None:
        """Setup validation configuration manager."""
        self._validators.clear()
        self._cache.clear()

    async def _teardown(self) -> None:
        """Teardown validation configuration manager."""
        self._validators.clear()
        self._cache.clear()

    async def register_validator(
        self, name: str, validator_config: dict[str, Any]
    ) -> None:
        """Register validator configuration.

        Args:
            name: Validator name
            validator_config: Validator configuration
        """
        if not self.is_initialized:
            await self.initialize()

        self._validators[name] = validator_config

        # Limitar o tamanho do cache
        if len(self._cache) > self.config.cache_size:
            # Remover entradas mais antigas
            remove_count = len(self._cache) - self.config.cache_size
            for key in list(self._cache.keys())[:remove_count]:
                del self._cache[key]

    async def get_validator(self, name: str) -> dict[str, Any] | None:
        """Get validator configuration.

        Args:
            name: Validator name

        Returns:
            Validator configuration if found, None otherwise
        """
        if not self.is_initialized:
            await self.initialize()

        return self._validators.get(name)

    async def get_stats(self) -> dict[str, Any]:
        """Get validation configuration statistics.

        Returns:
            Validation configuration statistics
        """
        if not self.is_initialized:
            await self.initialize()

        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "strict_mode": self.config.strict_mode,
            "validators_count": len(self._validators),
            "cache_size": len(self._cache),
            "max_cache_size": self.config.cache_size,
            "validator_names": list(self._validators.keys()),
        }
