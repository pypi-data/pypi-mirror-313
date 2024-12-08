"""Type definitions module."""

from typing import Any, TypeVar

from .json import JsonDict, JsonValue
from .validation import ValidationResult

# Type variable for generic types
T = TypeVar("T")
U = TypeVar("U")

# Type alias for any callable
AnyCallable = Any  # TODO: Make this more specific

__all__ = [
    "AnyCallable",
    "JsonDict",
    "JsonValue",
    "T",
    "U",
    "ValidationResult",
]
