"""Base classes for pipeline implementation."""

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from ..config.config import Config

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")
StepInputT = TypeVar("StepInputT")
StepOutputT = TypeVar("StepOutputT")


@dataclass
class PipelineConfig(Config):
    """Pipeline configuration."""

    name: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineResult(Generic[OutputT]):
    """Result of pipeline execution."""

    output: OutputT
    metadata: dict[str, Any] = field(default_factory=dict)


class PipelineStep(Generic[StepInputT, StepOutputT]):
    """Base class for pipeline steps."""

    async def execute(self, input_data: StepInputT) -> StepOutputT:
        """Execute pipeline step.

        Args:
            input_data: Input data to process

        Returns:
            Processed output data
        """
        raise NotImplementedError


class Pipeline(Generic[InputT, OutputT]):
    """Base pipeline implementation."""

    def __init__(self, config: PipelineConfig) -> None:
        """Initialize pipeline.

        Args:
            config: Pipeline configuration
        """
        self.config = config
        self._steps: list[PipelineStep[Any, Any]] = []

    def add_step(self, step: PipelineStep[Any, Any]) -> None:
        """Add step to pipeline.

        Args:
            step: Pipeline step to add
        """
        self._steps.append(step)

    async def execute(self, input_data: InputT) -> PipelineResult[OutputT]:
        """Execute pipeline.

        Args:
            input_data: Input data to process

        Returns:
            Pipeline execution result
        """
        current_data: Any = input_data

        for step in self._steps:
            current_data = await step.execute(current_data)

        return PipelineResult[OutputT](
            output=current_data, metadata={"steps": len(self._steps)}
        )
