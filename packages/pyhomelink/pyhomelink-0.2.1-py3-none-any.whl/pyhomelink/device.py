"""Python module for accessing HomeLINK Device."""

from datetime import date, datetime
from typing import List

from .alert import Alert
from .auth import AbstractAuth
from .const import (
    ATTR_RESULTS,
    MODELTYPE_CO2,
    MODELTYPE_ENVIRONMENT,
    HomeLINKReadingType,
)
from .reading import DeviceReading
from .utils import check_status, parse_date


class Metadata:
    """Metadata for property."""

    def __init__(self, raw_data: dict) -> None:
        """Initialise Metadata"""
        self._raw_data = raw_data

    @property
    def signalstrength(self) -> str:
        """Return the signalstrength of the Device"""
        return self._raw_data["signalStrength"]

    @property
    def lastseendate(self) -> datetime:
        """Return the lastseendate of the Device"""
        return parse_date(self._raw_data["lastSeenDate"])

    @property
    def connectivitytype(self) -> str:
        """Return the connectivitytype of the Device"""
        return self._raw_data["connectivityType"]


class Status:
    """Status for property."""

    def __init__(self, raw_data: dict) -> None:
        """Initialise Status"""
        self._raw_data = raw_data

    @property
    def operationalstatus(self) -> str:
        """Return the operationalstatus of the Device"""
        return self._raw_data["operationalStatus"]

    @property
    def lasttesteddate(self) -> datetime:
        """Return the lasttesteddate of the Device"""
        return parse_date(self._raw_data["lastTestedDate"])

    @property
    def datacollectionstatus(self) -> str:
        """Return the datacollectionstatus of the Device"""
        return self._raw_data["dataCollectionStatus"]


class Readings:
    """Reading URLs for device"""

    def __init__(self, raw_data: dict) -> None:
        """Initialise _Rel."""
        self._raw_data = raw_data

    @property
    def temperaturereadings(self) -> str:
        """Return the temperature readings url of the Device"""
        return self._raw_data["temperatureReadings"]

    @property
    def humidityreadings(self) -> str:
        """Return the humidity readings url of the Device"""
        return self._raw_data["humidityReadings"]


class ReadingsCO2(Readings):
    """CO2 Reading URLs for device"""

    @property
    def co2readings(self) -> str:
        """Return the CO2 readings url of the Device"""
        return self._raw_data["co2Readings"]


class Rel:
    """Relative URLs for device."""

    def __init__(self, raw_data: dict, modeltype: str) -> None:
        """Initialise _Rel."""
        self._raw_data = raw_data
        self._modeltype = modeltype

    @property
    def self(self) -> str:
        """Return the self url of the Device"""
        return self._raw_data["_self"]

    @property
    def hl_property(self) -> str:
        """Return the property url of the Device"""
        return self._raw_data["property"]

    @property
    def alerts(self) -> str:
        """Return the alerts url of the Device"""
        return self._raw_data["alerts"]


class RelEnvironment(Rel):
    """Reading URLs for device."""

    @property
    def readings(self) -> Readings | ReadingsCO2:
        """Return the readings url of the Device"""
        if MODELTYPE_CO2 in self._modeltype:
            return ReadingsCO2(self._raw_data["readings"])
        return Readings(self._raw_data["readings"])


class Device:
    """Device is the instantiation of a HomeLINK Device"""

    def __init__(self, raw_data: dict, auth: AbstractAuth) -> None:
        """Initialize the property."""
        self._raw_data = raw_data
        self._auth = auth

    @property
    def serialnumber(self) -> str:
        """Return the serialnumber of the Device"""
        return self._raw_data["serialNumber"]

    @property
    def createdat(self) -> datetime:
        """Return the createdat of the Device"""
        return parse_date(self._raw_data["createdAt"])

    @property
    def updatedat(self) -> datetime:
        """Return the updatedate of the Device"""
        return parse_date(self._raw_data["updatedAt"])

    @property
    def model(self) -> str:
        """Return the model of the Device"""
        return self._raw_data["model"]

    @property
    def modeltype(self) -> str:
        """Return the modeltype of the Device"""
        return self._raw_data["modelType"]

    @property
    def location(self) -> str:
        """Return the location of the Device"""
        return self._raw_data["location"]

    @property
    def locationnickname(self) -> str:
        """Return the locationnickname of the Device"""
        return self._raw_data["locationNickname"]

    @property
    def manufacturer(self) -> str:
        """Return the manufacturer of the Device"""
        return self._raw_data["manufacturer"]

    @property
    def installationdate(self) -> datetime:
        """Return the installationdate of the Device"""
        return parse_date(self._raw_data["installationDate"])

    @property
    def installedby(self) -> str:
        """Return the installedby of the Device"""
        return self._raw_data["installedBy"]

    @property
    def replacedate(self) -> datetime:
        """Return the replacedate of the Device"""
        return parse_date(self._raw_data["replaceDate"])

    @property
    def metadata(self) -> Metadata:
        """Return the metadata of the Device"""
        return Metadata(self._raw_data["metadata"])

    @property
    def status(self) -> Status:
        """Return the tags of the Device"""
        return Status(self._raw_data["status"])

    @property
    def rel(self) -> Rel | RelEnvironment:
        """Return the tags of the Device"""
        if self.modeltype.startswith(MODELTYPE_ENVIRONMENT):
            return RelEnvironment(self._raw_data["_rel"], self.modeltype)
        return Rel(self._raw_data["_rel"], self.modeltype)

    async def async_get_alerts(self) -> List[Alert]:
        """Return the Alerts."""
        resp = await self._auth.request("get", f"{self.rel.alerts}")
        check_status(resp)
        return [Alert(alert_data) for alert_data in (await resp.json())[ATTR_RESULTS]]

    async def async_get_device_readings(
        self,
        readingtype: HomeLINKReadingType,
        start: date | None = None,
        end: date | None = None,
    ) -> DeviceReading:
        """Return the Device Readings."""
        if readingtype == HomeLINKReadingType.CO2:
            url = self.rel.readings.co2readings  # type: ignore[attr-defined]
        elif readingtype == HomeLINKReadingType.HUMIDITY:
            url = self.rel.readings.humidityreadings  # type: ignore[attr-defined]
        elif readingtype == HomeLINKReadingType.TEMPERATURE:
            url = self.rel.readings.temperaturereadings  # type: ignore[attr-defined]

        if start or end:
            url = f"{url}?"
        if start:
            url = f"{url}start={start}"
            if end:
                url = f"{url}&"
        if end:
            url = f"{url}end={end}"
        resp = await self._auth.request("get", url)

        check_status(resp)
        return DeviceReading(await resp.json())
