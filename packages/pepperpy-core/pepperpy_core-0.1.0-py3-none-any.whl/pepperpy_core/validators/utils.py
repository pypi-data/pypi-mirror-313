"""Validation utilities."""

from collections.abc import Sequence
from typing import Any

from .base import BaseValidator


async def validate_many(value: Any, validators: Sequence[BaseValidator]) -> bool:
    """Run multiple validations.

    Args:
        value: Value to validate
        validators: Validators to run

    Returns:
        True if all validations pass, False otherwise
    """
    for validator in validators:
        if not await validator.validate(value):
            return False
    return True
