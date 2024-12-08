"""JSON type definitions."""

# Type aliases for JSON data
JsonValue = str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]
JsonDict = dict[str, JsonValue]

__all__ = ["JsonValue", "JsonDict"]
