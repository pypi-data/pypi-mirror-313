"""Network configuration"""

from dataclasses import dataclass, field

from ..base import BaseData
from ..types import JsonDict


@dataclass
class NetworkConfig(BaseData):
    """Network configuration"""

    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    verify_ssl: bool = True
    metadata: JsonDict = field(default_factory=dict)

    def validate(self) -> None:
        """Validate configuration."""
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("Max retries must be non-negative")
        if self.retry_delay < 0:
            raise ValueError("Retry delay must be non-negative")
