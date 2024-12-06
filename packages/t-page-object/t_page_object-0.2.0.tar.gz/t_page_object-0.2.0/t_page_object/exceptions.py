"""Module to hold all custom exceptions for the package."""


class NoVerificationElement(Exception):
    """Raised when no verification element is set for the page."""

    pass


class BadRequestError(Exception):
    """Exception for a bad request in t_requests."""

    pass


class NoURL(Exception):
    """Raised when no URL is set for the page."""

    pass
