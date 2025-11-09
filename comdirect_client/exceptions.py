"""Custom exceptions for the Comdirect API client."""


class ComdirectAPIError(Exception):
    """Base exception for all Comdirect API errors."""

    pass


class AuthenticationError(ComdirectAPIError):
    """Raised when authentication fails."""

    pass


class TANTimeoutError(ComdirectAPIError):
    """Raised when TAN approval times out."""

    pass


class SessionActivationError(ComdirectAPIError):
    """Raised when session activation fails."""

    pass


class TokenExpiredError(ComdirectAPIError):
    """Raised when the access token has expired."""

    pass


class NetworkTimeoutError(ComdirectAPIError):
    """Raised when a network request times out."""

    pass


class AccountNotFoundError(ComdirectAPIError):
    """Raised when an account is not found."""

    pass


class ValidationError(ComdirectAPIError):
    """Raised when API returns 422 Unprocessable Entity (validation error)."""

    pass


class ServerError(ComdirectAPIError):
    """Raised when API returns 500 Internal Server Error."""

    pass
