"""Logging settings configuration."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData


@dataclass
class LoggingSettings(BaseConfigData):
    """Logging settings configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    enabled: bool = True
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handlers: dict[str, Any] = field(default_factory=dict)
    formatters: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate settings.

        Raises:
            ValueError: If handlers or formatters are invalid
        """
        # Validar que os handlers e formatters têm a estrutura correta
        for name, handler in self.handlers.items():
            if "class" not in handler:
                raise ValueError(f"Handler '{name}' must have a 'class' field")

        for name, formatter in self.formatters.items():
            if "format" not in formatter:
                raise ValueError(f"Formatter '{name}' must have a 'format' field")

    def get_config(self) -> dict[str, Any]:
        """Get logging configuration dictionary.

        Returns:
            Logging configuration
        """
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": self.formatters,
            "handlers": self.handlers,
            "loggers": {
                self.name: {
                    "level": self.level,
                    "handlers": list(self.handlers.keys()),
                    "propagate": True,
                }
            },
        }
