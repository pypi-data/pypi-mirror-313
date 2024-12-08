"""Network exceptions."""

from ..exceptions import PepperpyError


class NetworkError(PepperpyError):
    """Base network error."""


class ConnectionError(NetworkError):
    """Connection error."""


class RequestError(NetworkError):
    """Request error."""


class ResponseError(NetworkError):
    """Response error."""


class TimeoutError(NetworkError):
    """Timeout error."""


class SSLError(NetworkError):
    """SSL error."""


class ProxyError(NetworkError):
    """Proxy error."""


class DNSError(NetworkError):
    """DNS resolution error."""


__all__ = [
    "NetworkError",
    "ConnectionError",
    "RequestError",
    "ResponseError",
    "TimeoutError",
    "SSLError",
    "ProxyError",
    "DNSError",
]
