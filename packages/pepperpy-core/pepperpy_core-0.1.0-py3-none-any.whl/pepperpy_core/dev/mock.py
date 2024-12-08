"""Mock utilities for development."""

from collections.abc import Callable
from typing import Any, cast

from ..types import JsonDict, JsonValue


class MockResponse:
    """Mock HTTP response."""

    def __init__(
        self,
        status: int = 200,
        data: str | bytes | dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize mock response.

        Args:
            status: HTTP status code
            data: Response data
            headers: Response headers
        """
        self.status = status
        self.data = data or {}
        self.headers = headers or {}

    async def json(self) -> JsonDict:
        """Get JSON response data."""
        if isinstance(self.data, str | bytes):
            import json

            return cast(JsonDict, json.loads(self.data))
        return cast(JsonDict, self.data)

    async def text(self) -> str:
        """Get text response data."""
        if isinstance(self.data, bytes):
            return self.data.decode()
        if isinstance(self.data, dict):
            import json

            return json.dumps(self.data)
        return str(self.data)


def mock_response(
    status: int = 200,
    data: str | bytes | dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> Callable[..., MockResponse]:
    """Create mock response factory."""

    def factory(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(status, data, headers)

    return factory


def generate_mock_data() -> dict[str, JsonValue]:
    """Generate mock data."""
    mock_data = {
        "id": "123",
        "name": "test",
        "value": 42,
        "enabled": True,
        "metadata": {"key": "value"},
    }
    return cast(dict[str, JsonValue], mock_data)
