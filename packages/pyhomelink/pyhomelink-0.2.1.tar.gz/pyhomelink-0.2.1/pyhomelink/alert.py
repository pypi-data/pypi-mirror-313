"""Python module for accessing HomeLINK Alert."""

from datetime import datetime

from .utils import parse_date


class Rel:
    """Relative URLs for property."""

    def __init__(self, raw_data) -> None:
        """Initialise _Rel."""
        self._raw_data = raw_data
        if "device" in self._raw_data:
            self.device = self._raw_data["device"]

        if "insight" in self._raw_data:
            self.insight = self._raw_data["insight"]

    @property
    def self(self) -> str:
        """Return the self url of the Alert"""
        return self._raw_data["_self"]

    @property
    def hl_property(self) -> str:
        """Return the property url of the Alert"""
        return self._raw_data["property"]


class Alert:
    """Alert is the instantiation of a HomeLINK Alert"""

    def __init__(self, raw_data: dict) -> None:
        """Initialize the property."""
        self._raw_data = raw_data

    @property
    def alertid(self) -> str:
        """Return the alertid of the Alert"""
        return self._raw_data["id"]

    @property
    def serialnumber(self) -> str:
        """Return the serialnumber of the Alert"""
        return self._raw_data["serialNumber"]

    @property
    def description(self) -> str:
        """Return the description of the Alert"""
        return self._raw_data["description"]

    @property
    def eventtype(self) -> str:
        """Return the eventtype of the Alert"""
        return self._raw_data["eventType"]

    @property
    def propertyreference(self) -> str:
        """Return the propertyreference of the Alert"""
        return self._raw_data["propertyReference"]

    @property
    def model(self) -> str:
        """Return the model of the Alert"""
        return self._raw_data["model"]

    @property
    def modeltype(self) -> str:
        """Return the modeltype of the Alert"""
        return self._raw_data["modelType"]

    @property
    def location(self) -> str:
        """Return the location of the Alert"""
        return self._raw_data["location"]

    @property
    def locationnickname(self) -> str:
        """Return the locationnickname of the Alert"""
        return self._raw_data["locationNickname"]

    @property
    def insightid(self) -> str:
        """Return the insightId of the Alert"""
        return self._raw_data["insightId"]

    @property
    def raiseddate(self) -> datetime:
        """Return the raisedDate of the Property"""
        return parse_date(self._raw_data["raisedDate"])  # type: ignore[return-value]

    @property
    def severity(self) -> str:
        """Return the severity of the Alert"""
        return self._raw_data["severity"]

    @property
    def category(self) -> str:
        """Return the category of the Alert"""
        return self._raw_data["category"]

    @property
    def hl_type(self) -> str:
        """Return the type of the Alert"""
        return self._raw_data["type"]

    @property
    def status(self) -> str:
        """Return the status of the Alert"""
        return self._raw_data["status"]

    @property
    def rel(self) -> Rel:
        """Return the tags of the Alert"""
        return Rel(self._raw_data["_rel"])
