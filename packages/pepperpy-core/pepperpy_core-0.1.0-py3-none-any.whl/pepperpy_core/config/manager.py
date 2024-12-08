"""Configuration manager module."""

import json
import os
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from .types import ConfigManagerConfig

T = TypeVar("T", bound=BaseModel)


class ConfigManager:
    """Configuration manager."""

    def __init__(self, config: ConfigManagerConfig) -> None:
        """Initialize configuration manager."""
        self.config = config
        self.__initialized = False

    async def initialize(self) -> None:
        """Initialize manager."""
        if self.__initialized:
            return
        await self._setup()
        self.__initialized = True

    async def cleanup(self) -> None:
        """Cleanup manager."""
        if not self.__initialized:
            return
        await self._teardown()
        self.__initialized = False

    async def is_ready(self) -> bool:
        """Check if manager is initialized."""
        return self.__initialized

    async def _setup(self) -> None:
        """Setup manager resources."""
        os.makedirs(self.config.config_path, exist_ok=True)

    async def _teardown(self) -> None:
        """Teardown manager resources."""
        pass

    async def get_config(self, name: str, config_type: type[T]) -> T:
        """Get configuration by name.

        Args:
            name: Configuration name
            config_type: Configuration type

        Returns:
            Configuration instance

        Raises:
            ValueError: If config file not found
        """
        config_path = Path(self.config.config_path) / f"{name}.json"
        if not config_path.exists():
            raise ValueError(f"Config file not found: {name}")

        config_text = config_path.read_text()
        config_data = json.loads(config_text)
        return config_type.model_validate(config_data)
