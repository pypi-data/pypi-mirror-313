"""package exceptions for t-office-365."""
from .exceptions import (
    UnexpectedError,
    ServiceUnavailableError,
    AssetLockedError,
    AssetNotFoundError,
    BadRequestError,
    AuthenticationGraphError,
    InvalidJSONError,
)

__all__ = [
    "UnexpectedError",
    "ServiceUnavailableError",
    "AssetLockedError",
    "AssetNotFoundError",
    "BadRequestError",
    "AuthenticationGraphError",
    "InvalidJSONError",
]
