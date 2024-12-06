"""Python module for accessing HomeLINK Reading."""

from datetime import datetime

from .utils import parse_date


class Rel:
    """Relative URLs for reading."""

    def __init__(self, raw_data):
        """Initialise _Rel."""
        self._raw_data = raw_data

    @property
    def hl_property(self) -> str:
        """Return the property url of the Reading"""
        return self._raw_data["property"]

    @property
    def device(self) -> str:
        """Return the device url of the Reading"""
        return self._raw_data["device"]


class Value:
    """Value for reading."""

    def __init__(self, raw_data):
        """Initialise _Rel."""
        self._raw_data = raw_data

    @property
    def value(self) -> str:
        """Return the value of the Reading"""
        return self._raw_data["value"]

    @property
    def serialnumber(self) -> str:
        """Return the serialNumber of the Reading"""
        return self._raw_data["serialNumber"]

    @property
    def readingtypeid(self) -> str:
        """Return the readingTypeId of the Reading"""
        return self._raw_data["readingTypeId"]

    @property
    def statusid(self) -> str:
        """Return the statusId of the Reading"""
        return self._raw_data["statusId"]

    @property
    def readingdate(self) -> datetime:
        """Return the readingDate of the Reading"""
        return parse_date(self._raw_data["readingDate"])


class Device:
    """Device is the instantiation of a device reading."""

    def __init__(self, raw_data: dict):
        """Initialize the property."""
        self._raw_data = raw_data

    @property
    def count(self) -> int:
        """Return the count of the Reading device values"""
        return self._raw_data["count"]

    @property
    def serialnumber(self) -> str:
        """Return the serial number of the Reading device"""
        return self._raw_data["serialNumber"]

    @property
    def rel(self) -> Rel:
        """Return the urls of the Reading device"""
        return Rel(self._raw_data["_rel"])

    @property
    def values(self) -> list[Value]:
        """Return the values of the Reading"""
        return [Value(value) for value in self._raw_data["values"]]


class PropertyReading:
    """Reading is the instantiation of a HomeLINK Reading"""

    def __init__(self, raw_data: dict) -> None:
        """Initialize the property."""
        self._raw_data = raw_data

    @property
    def unit(self) -> str:
        """Return the unit of the Reading"""
        return self._raw_data["unit"]

    @property
    def type(self) -> str:
        """Return the type of the Reading"""
        return self._raw_data["type"]

    @property
    def dataavailability(self) -> int:
        """Return the dataAvailability of the Reading"""
        return self._raw_data["dataAvailability"]

    @property
    def devices(self) -> list[Device]:
        """Return the devices of the Reading"""
        return [Device(device) for device in self._raw_data["devices"]]


class DeviceReading:
    """Reading is the instantiation of a HomeLINK Reading"""

    def __init__(self, raw_data: dict) -> None:
        """Initialize the property."""
        self._raw_data = raw_data

    @property
    def unit(self) -> str:
        """Return the unit of the Reading"""
        return self._raw_data["unit"]

    @property
    def count(self) -> int:
        """Return the count of the Reading values"""
        return self._raw_data["count"]

    @property
    def type(self) -> str:
        """Return the type of the Reading"""
        return self._raw_data["type"]

    @property
    def dataavailability(self) -> int:
        """Return the dataAvailability of the Reading"""
        return self._raw_data["dataAvailability"]

    @property
    def rel(self) -> Rel:
        """Return the urls of the Reading"""
        return Rel(self._raw_data["_rel"])

    @property
    def values(self) -> list[Value]:
        """Return the values of the Reading"""
        return [Value(value) for value in self._raw_data["values"]]
