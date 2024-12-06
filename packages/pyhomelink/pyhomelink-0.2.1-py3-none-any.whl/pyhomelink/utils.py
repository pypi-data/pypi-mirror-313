"""HomeLINK utilities."""

from datetime import datetime

from dateutil import parser

from .exceptions import ApiException, AuthException


def check_status(resp) -> None:
    """Check status of the call."""
    if resp.status == 401:
        raise AuthException(f"Authorization failed: {resp.status}")
    if resp.status != 200:
        raise ApiException(f"Error request failed: {resp.status}, url: {resp.url}")


def parse_date(in_date) -> datetime:
    """Parse the date."""
    return parser.parse(in_date) if in_date else None  # type: ignore[return-value]
