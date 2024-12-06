"""HomeLINK Exceptions."""


class HomeLINKException(Exception):
    """Base class for all client exceptions."""


class ApiException(HomeLINKException):
    """Raised during problems talking to the API."""


class AuthException(ApiException):
    """Raised due to auth problems talking to API."""
