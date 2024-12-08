"""Database configuration"""

from dataclasses import dataclass, field
from typing import Any, ClassVar, cast

from ..base import ModuleConfig
from ..types import JsonDict


@dataclass
class DBConfig(ModuleConfig):
    """Database configuration"""

    name: str = "db"
    host: str = "localhost"
    port: int = 5432
    database: str = "pepperpy"
    user: str = "postgres"
    password: str = ""
    metadata: JsonDict = field(default_factory=dict)
    _instance: ClassVar[Any] = None

    @classmethod
    def get_default(cls) -> "DBConfig":
        """Get default configuration instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cast(DBConfig, cls._instance)
