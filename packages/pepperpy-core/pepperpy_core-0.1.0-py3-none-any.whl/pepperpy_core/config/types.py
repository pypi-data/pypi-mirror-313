"""Configuration types module."""

from pydantic import BaseModel


class ConfigManagerConfig(BaseModel):
    """Configuration manager configuration."""

    name: str
    config_path: str
    enabled: bool = True


__all__ = ["ConfigManagerConfig"]
