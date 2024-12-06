"""Custom exceptions for the t-office-365."""


class TOffice365Exception(Exception):
    """Business Exception."""


class AuthenticationGraphError(TOffice365Exception):
    """Authentication to OfficeAccount Graph Exception."""


class AssetLockedError(TOffice365Exception):
    """Asset locked Exception."""


class BadRequestError(TOffice365Exception):
    """Bad request error."""


class AssetNotFoundError(TOffice365Exception):
    """Asset not found error."""


class UnexpectedError(TOffice365Exception):
    """Unexpected error."""


class ServiceUnavailableError(TOffice365Exception):
    """Service Unavailable error."""


class InvalidJSONError(Exception):
    """Custom exception for invalid JSON responses."""

    pass
