"""Python module for accessing HomeLINK Property."""

from datetime import datetime
from typing import List

from .alert import Alert
from .auth import AbstractAuth
from .const import ATTR_RESULTS, HomeLINKEndpoint
from .device import Device
from .insight import Insight
from .reading import PropertyReading
from .utils import check_status, parse_date


class Rel:
    """Relative URLs for property."""

    def __init__(self, raw_data: dict) -> None:
        """Initialise _Rel."""
        self._raw_data = raw_data

    @property
    def self(self) -> str:
        """Return the self url of the Property"""
        return self._raw_data["_self"]

    @property
    def devices(self) -> str:
        """Return the devices url of the Property"""
        return self._raw_data["devices"]

    @property
    def alerts(self) -> str:
        """Return the alerts url of the Property"""
        return self._raw_data["alerts"]

    @property
    def readings(self) -> str:
        """Return the readings url of the Property"""
        return self._raw_data["readings"]

    @property
    def insights(self) -> str:
        """Return the insights url of the Property"""
        return self._raw_data["insights"]


class Property:
    """Property is the instantiation of a HomeLINK Property"""

    def __init__(self, raw_data: dict, auth: AbstractAuth) -> None:
        """Initialize the property."""
        self._raw_data = raw_data
        self._auth = auth

    @property
    def reference(self) -> str:
        """Return the reference of the Property"""
        return self._raw_data["reference"]

    @property
    def createdate(self) -> datetime:
        """Return the createdat of the Property"""
        return parse_date(self._raw_data["createdAt"])

    @property
    def updatedat(self) -> datetime:
        """Return the updatedat of the Property"""
        return parse_date(self._raw_data["updatedAt"])

    @property
    def postcode(self) -> str:
        """Return the postcode of the Property"""
        return self._raw_data["postcode"]

    @property
    def latitude(self) -> str:
        """Return the latitude of the Property"""
        return self._raw_data["latitude"]

    @property
    def longitude(self) -> str:
        """Return the longitude of the Property"""
        return self._raw_data["longitude"]

    @property
    def address(self) -> str:
        """Return the address of the Property"""
        return self._raw_data["address"]

    @property
    def tags(self) -> list[str]:
        """Return the tags of the Property"""
        return self._raw_data["tags"]

    @property
    def rel(self) -> Rel:
        """Return the tags of the Property"""
        return Rel(self._raw_data["_rel"])

    async def async_get_devices(self) -> List[Device]:
        """Return the Devices."""
        resp = await self._auth.request("get", f"{self.rel.devices}")
        check_status(resp)
        return [
            Device(device_data, self._auth)
            for device_data in (await resp.json())[ATTR_RESULTS]
        ]

    async def async_get_insights(self) -> List[Insight]:
        """Return the Insights."""
        resp = await self._auth.request("get", f"{self.rel.insights}")
        check_status(resp)
        return [
            Insight(insight_data) for insight_data in (await resp.json())[ATTR_RESULTS]
        ]

    async def async_get_alerts(self) -> List[Alert]:
        """Return the Alerts."""
        resp = await self._auth.request("get", f"{self.rel.alerts}")
        check_status(resp)
        return [Alert(alert_data) for alert_data in (await resp.json())[ATTR_RESULTS]]

    async def async_get_readings(self, readingdate) -> List[PropertyReading]:
        """Return the Readings."""
        resp = await self._auth.request(
            "get", f"{self.rel.readings}?date={readingdate}"
        )
        check_status(resp)
        return [
            PropertyReading(reading_data)
            for reading_data in await resp.json()
            if "type" in reading_data
        ]

    async def async_add_tags(self, tags) -> List[str]:
        """Add tags to a property."""
        resp = await self._auth.request(
            "put",
            HomeLINKEndpoint.PROPERTY_TAGS.format(propertyreference=self.reference),
            json={"tagIds": tags},
        )
        check_status(resp)
        return await resp.json()

    async def async_delete_tags(self, tags) -> List[str]:
        """Delete tags from a property."""
        resp = await self._auth.request(
            "delete",
            HomeLINKEndpoint.PROPERTY_TAGS.format(propertyreference=self.reference),
            json={"tagIds": tags},
        )
        check_status(resp)
        return await resp.json()
