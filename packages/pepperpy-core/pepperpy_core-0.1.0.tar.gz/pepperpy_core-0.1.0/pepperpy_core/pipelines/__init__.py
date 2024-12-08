"""Pipeline module."""

from typing import TypeVar

from .base import Pipeline, PipelineStep
from .manager import PipelineManager

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")

__all__ = [
    "Pipeline",
    "PipelineStep",
    "PipelineManager",
    "InputT",
    "OutputT",
]
