"""Settings configuration."""

import importlib.util
import os
from pathlib import Path
from typing import Any

# Verificar disponibilidade do python-dotenv
_dotenv_spec = importlib.util.find_spec("dotenv")
has_dotenv = bool(_dotenv_spec)


class Settings:
    """Settings configuration."""

    def __init__(self, env_file: str | Path | None = None) -> None:
        """Initialize settings.

        Args:
            env_file: Path to .env file
        """
        self._env_file = env_file
        self._values: dict[str, Any] = {}
        self._initialized = False

    def load(self) -> None:
        """Load settings from environment."""
        if has_dotenv and self._env_file:
            try:
                from dotenv import load_dotenv

                load_dotenv(self._env_file)
            except ImportError:
                pass  # Ignorar erro se dotenv não estiver disponível

        # Carregar variáveis de ambiente
        for key, value in os.environ.items():
            self._values[key] = value

        self._initialized = True

    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value.

        Args:
            key: Setting key
            default: Default value if key not found

        Returns:
            Setting value
        """
        if not self._initialized:
            self.load()
        return self._values.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """Get setting value.

        Args:
            key: Setting key

        Returns:
            Setting value

        Raises:
            KeyError: If key not found
        """
        if not self._initialized:
            self.load()
        return self._values[key]
