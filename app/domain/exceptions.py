"""Domain exceptions."""


class MovieAPIError(Exception):
    """Base exception for movie API errors."""

    pass


class MovieAPIConnectionError(MovieAPIError):
    """Raised when there are connection issues with the movie API."""

    pass


class MovieAPIResponseError(MovieAPIError):
    """Raised when the movie API returns an error response."""

    pass
