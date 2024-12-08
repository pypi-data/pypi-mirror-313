"""Base type definitions."""

from typing import Any

JsonValue = str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]
JsonDict = dict[str, Any]


class BaseConfigData:
    """Base configuration data."""

    def __init__(self, name: str) -> None:
        """Initialize configuration data.

        Args:
            name: Configuration name
        """
        self.name = name
