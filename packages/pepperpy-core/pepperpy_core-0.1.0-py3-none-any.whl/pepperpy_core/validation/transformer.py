"""Validation transformer module."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from ..base import BaseConfigData
from ..module import BaseModule

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


@dataclass
class TransformerConfig(BaseConfigData):
    """Transformer configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    enabled: bool = True
    strict_mode: bool = False
    cache_size: int = 1000
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate configuration."""
        if self.cache_size < 0:
            raise ValueError("cache_size must be non-negative")


@dataclass
class TransformRule(Generic[InputT, OutputT]):
    """Transform rule."""

    name: str
    transform_fn: Callable[[InputT], OutputT]
    input_type: type[InputT]
    output_type: type[OutputT]
    metadata: dict[str, Any] = field(default_factory=dict)


class ValidationTransformer(BaseModule[TransformerConfig]):
    """Validation transformer implementation."""

    def __init__(self) -> None:
        """Initialize validation transformer."""
        config = TransformerConfig(name="validation-transformer")
        super().__init__(config)
        self._rules: dict[str, TransformRule[Any, Any]] = {}
        self._cache: dict[str, Any] = {}

    async def _setup(self) -> None:
        """Setup validation transformer."""
        self._rules.clear()
        self._cache.clear()

    async def _teardown(self) -> None:
        """Teardown validation transformer."""
        self._rules.clear()
        self._cache.clear()

    async def register_rule(self, rule: TransformRule[InputT, OutputT]) -> None:
        """Register transform rule.

        Args:
            rule: Transform rule
        """
        if not self.is_initialized:
            await self.initialize()

        self._rules[rule.name] = rule

        # Limitar o tamanho do cache
        if len(self._cache) > self.config.cache_size:
            # Remover entradas mais antigas
            remove_count = len(self._cache) - self.config.cache_size
            for key in list(self._cache.keys())[:remove_count]:
                del self._cache[key]

    async def transform(self, name: str, value: Any) -> Any:
        """Transform value using registered rule.

        Args:
            name: Rule name
            value: Value to transform

        Returns:
            Transformed value

        Raises:
            ValueError: If rule not found or type mismatch
        """
        if not self.is_initialized:
            await self.initialize()

        rule = self._rules.get(name)
        if rule is None:
            raise ValueError(f"Transform rule {name} not found")

        if not isinstance(value, rule.input_type):
            raise ValueError(
                f"Value type {type(value)} does not match rule input type {rule.input_type}"
            )

        cache_key = f"{name}:{value}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        result = rule.transform_fn(value)
        if not isinstance(result, rule.output_type):
            msg = (
                f"Transform result type {type(result)} does not match rule output type "
                f"{rule.output_type}"
            )
            raise ValueError(msg)

        self._cache[cache_key] = result
        return result

    async def get_stats(self) -> dict[str, Any]:
        """Get transformer statistics.

        Returns:
            Transformer statistics
        """
        if not self.is_initialized:
            await self.initialize()

        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "strict_mode": self.config.strict_mode,
            "rules_count": len(self._rules),
            "cache_size": len(self._cache),
            "max_cache_size": self.config.cache_size,
            "rule_names": list(self._rules.keys()),
        }
