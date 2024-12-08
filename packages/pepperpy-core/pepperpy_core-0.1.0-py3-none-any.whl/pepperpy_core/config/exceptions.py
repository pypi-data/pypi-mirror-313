"""Configuration-related exceptions."""

from ..exceptions import PepperpyError


class ConfigError(PepperpyError):
    """Base configuration error."""


class ConfigLoadError(ConfigError):
    """Configuration loading error."""


class ConfigValidationError(ConfigError):
    """Configuration validation error."""


class ConfigNotFoundError(ConfigError):
    """Configuration not found error."""


__all__ = [
    "ConfigError",
    "ConfigLoadError",
    "ConfigValidationError",
    "ConfigNotFoundError",
]
