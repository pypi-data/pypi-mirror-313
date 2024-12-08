"""Security-related exceptions"""


class SecurityError(Exception):
    """Base security error"""


class AuthError(SecurityError):
    """Authentication error"""


class PermissionError(SecurityError):
    """Permission error"""


class TokenError(SecurityError):
    """Token error"""


class CryptoError(SecurityError):
    """Cryptography error"""
