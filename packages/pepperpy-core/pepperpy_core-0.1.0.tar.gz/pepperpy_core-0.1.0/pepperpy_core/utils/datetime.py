"""Datetime utilities"""

from datetime import UTC, datetime


def utc_now() -> datetime:
    """Get current UTC datetime"""
    return datetime.now(UTC)
