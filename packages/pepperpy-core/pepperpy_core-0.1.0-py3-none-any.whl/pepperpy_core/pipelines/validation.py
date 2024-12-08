"""Pipeline validation utilities."""

from .base import PipelineConfig


def validate_config(config: PipelineConfig) -> None:
    """Validate pipeline configuration.

    Args:
        config: Pipeline configuration to validate

    Raises:
        ValueError: If configuration is invalid
    """
    if not config.name:
        raise ValueError("Pipeline name is required")
