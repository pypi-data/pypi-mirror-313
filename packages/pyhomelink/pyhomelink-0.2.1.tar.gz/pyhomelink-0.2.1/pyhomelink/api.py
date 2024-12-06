"""API in support of HomeLINK."""

from datetime import date
from typing import List

from .alert import Alert
from .auth import AbstractAuth
from .const import ATTR_RESULTS, LOOKUPEVENTTYPE, HomeLINKEndpoint, HomeLINKReadingType
from .device import Device
from .insight import Insight
from .lookup import Lookup, LookupEventType
from .property import Property
from .reading import DeviceReading, PropertyReading
from .utils import check_status


class HomeLINKApi:
    """HomeLINK API"""

    def __init__(self, auth: AbstractAuth) -> None:
        """Initialise the api."""
        self.auth = auth

    async def async_get_properties(self) -> List[Property]:
        """Return the Properties."""
        resp = await self.auth.request("get", HomeLINKEndpoint.PROPERTIES)
        check_status(resp)
        return [
            Property(property_data, self.auth)
            for property_data in (await resp.json())[ATTR_RESULTS]
        ]

    async def async_get_property(self, propertyreference: str) -> Property:
        """Return the Properties."""
        resp = await self.auth.request(
            "get",
            HomeLINKEndpoint.PROPERTY.format(propertyreference=propertyreference),
        )
        check_status(resp)
        return Property(await resp.json(), self.auth)

    async def async_get_property_devices(self, propertyreference: str) -> List[Device]:
        """Return the Property Devices."""
        resp = await self.auth.request(
            "get",
            HomeLINKEndpoint.PROPERTY_DEVICES.format(
                propertyreference=propertyreference
            ),
        )
        check_status(resp)
        return [
            Device(device_data, self.auth)
            for device_data in (await resp.json())[ATTR_RESULTS]
        ]

    async def async_get_property_alerts(self, propertyreference: str) -> List[Alert]:
        """Return the Property Alerts."""
        resp = await self.auth.request(
            "get",
            HomeLINKEndpoint.PROPERTY_ALERTS.format(
                propertyreference=propertyreference
            ),
        )
        check_status(resp)
        return [Alert(alert_data) for alert_data in (await resp.json())[ATTR_RESULTS]]

    async def async_get_property_insights(
        self, propertyreference: str
    ) -> List[Insight]:
        """Return the Property Insightss."""
        resp = await self.auth.request(
            "get",
            HomeLINKEndpoint.PROPERTY_INSIGHTS.format(
                propertyreference=propertyreference
            ),
        )
        check_status(resp)
        return [
            Insight(insight_data) for insight_data in (await resp.json())[ATTR_RESULTS]
        ]

    async def async_get_property_readings(
        self, propertyreference: str, readingdate: date
    ) -> List[PropertyReading]:
        """Return the Property Readings."""
        resp = await self.auth.request(
            "get",
            HomeLINKEndpoint.PROPERTY_READINGS.format(
                propertyreference=propertyreference, date=readingdate
            ),
        )
        check_status(resp)
        return [
            PropertyReading(reading_data)
            for reading_data in await resp.json()
            if "type" in reading_data
        ]

    async def async_add_property_tags(
        self, propertyreference: str, tags: List[str]
    ) -> List[str]:
        """Add tags to a property."""
        resp = await self.auth.request(
            "put",
            HomeLINKEndpoint.PROPERTY_TAGS.format(propertyreference=propertyreference),
            json={"tagIds": tags},
        )
        check_status(resp)
        return await resp.json()

    async def async_delete_property_tags(
        self, propertyreference: str, tags: List[str]
    ) -> List[str]:
        """Delete tags from a property."""
        resp = await self.auth.request(
            "delete",
            HomeLINKEndpoint.PROPERTY_TAGS.format(propertyreference=propertyreference),
            json={"tagIds": tags},
        )
        check_status(resp)
        return await resp.json()

    async def async_get_devices(self) -> List[Device]:
        """Return the Properties."""
        resp = await self.auth.request("get", HomeLINKEndpoint.DEVICES)
        check_status(resp)
        return [
            Device(device_data, self.auth)
            for device_data in (await resp.json())[ATTR_RESULTS]
        ]

    async def async_get_device(self, serialnumber: str) -> Device:
        """Return the Properties."""
        resp = await self.auth.request(
            "get", HomeLINKEndpoint.DEVICE.format(serialnumber=serialnumber)
        )
        check_status(resp)
        return Device(await resp.json(), self.auth)

    async def async_get_device_alerts(self, serialnumber: str) -> List[Alert]:
        """Return the Device Alerts."""
        resp = await self.auth.request(
            "get",
            HomeLINKEndpoint.DEVICE_ALERTS.format(serialnumber=serialnumber),
        )
        check_status(resp)
        return [Alert(alert_data) for alert_data in (await resp.json())[ATTR_RESULTS]]

    async def async_get_device_readings(
        self,
        serialnumber: str,
        readingtype: HomeLINKReadingType,
        start: date | None = None,
        end: date | None = None,
    ) -> DeviceReading:
        """Return the Device Alerts."""
        url = HomeLINKEndpoint.DEVICE_READINGS.format(
            serialnumber=serialnumber,
            readingtype=readingtype,
        )
        if start or end:
            url = f"{url}?"
        if start:
            url = f"{url}start={start}"
        if start and end:
            url = f"{url}&"
        if end:
            url = f"{url}end={end}"
        resp = await self.auth.request(
            "get",
            url,
        )
        check_status(resp)
        return DeviceReading(await resp.json())

    async def async_get_insights(self) -> List[Insight]:
        """Return the Properties."""
        resp = await self.auth.request("get", HomeLINKEndpoint.INSIGHTS)
        check_status(resp)
        return [
            Insight(insight_data) for insight_data in (await resp.json())[ATTR_RESULTS]
        ]

    async def async_get_insight(self, insightid: str) -> Insight:
        """Return the Properties."""
        resp = await self.auth.request(
            "get", HomeLINKEndpoint.INSIGHT.format(insightid=insightid)
        )
        check_status(resp)
        return Insight(await resp.json())

    async def async_get_lookups(self, lookuptype: str) -> List:
        """Return the Lookups for lookuptype"""
        resp = await self.auth.request(
            "get", HomeLINKEndpoint.LOOKUPS.format(lookuptype=lookuptype)
        )
        check_status(resp)
        return [
            self._process_lookup(lookuptype, lookup_data)
            for lookup_data in await resp.json()
        ]

    async def async_get_lookup(self, lookuptype: str, lookupid: str):
        """Return the Lookups for lookuptype"""
        resp = await self.auth.request(
            "get",
            HomeLINKEndpoint.LOOKUP.format(lookuptype=lookuptype, lookupid=lookupid),
        )
        check_status(resp)
        return self._process_lookup(lookuptype, await resp.json())

    def _process_lookup(self, lookuptype: str, data: dict):
        return LookupEventType(data) if lookuptype == LOOKUPEVENTTYPE else Lookup(data)
