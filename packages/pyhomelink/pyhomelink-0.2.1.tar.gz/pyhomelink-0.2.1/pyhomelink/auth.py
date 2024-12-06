"""HomeLINK Auth."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional

from aiohttp import ClientError, ClientResponse, ClientSession

from .const import BASE_URL

AUTHURL = "https://auth.live.homelync.io/oauth2"
AUTHORIZATION_HEADER = "Authorization"

_LOGGER = logging.getLogger(__name__)


class AbstractAuth(ABC):
    """Abstract class to make authenticated requests."""

    def __init__(
        self,
        websession: ClientSession,
    ) -> None:
        """Initialize the auth."""
        self._websession = websession

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def request(
        self, method: str, url_suffix: str, **kwargs: Optional[Mapping[str, Any]]
    ) -> ClientResponse:
        """Make a request."""
        try:
            access_token = await self.async_get_access_token()
        except ClientError as err:
            raise RuntimeError(f"Access token failure: {err}") from err
        headers = {
            AUTHORIZATION_HEADER: f"Bearer {access_token}",
            "accept": "application/json",
        }
        url = f"{BASE_URL}{url_suffix}"
        return await self._websession.request(
            method,
            url,
            **kwargs,  # type: ignore[arg-type]
            headers=headers,
        )

    async def async_get_token(
        self, url: str, **kwargs: Optional[Mapping[str, Any]]
    ) -> ClientResponse:
        """Make a request."""
        url = f"{AUTHURL}{url}"
        _LOGGER.debug(
            "request[%s]=%s %s",
            "get",
            "Auth get token",
            kwargs.get("params"),
        )
        return await self._websession.request("get", url, **kwargs)  # type: ignore[arg-type]
