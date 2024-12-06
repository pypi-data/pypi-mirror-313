"""Python module for accessing HomeLINK Insight."""

from datetime import datetime

from .utils import parse_date


class Rel:
    """Relative URLs for property."""

    def __init__(self, raw_data):
        """Initialise _Rel."""
        self._raw_data = raw_data

    @property
    def self(self) -> str:
        """Return the self url of the Insight"""
        return self._raw_data["_self"]

    @property
    def hl_property(self) -> str:
        """Return the property url of the Insight"""
        return self._raw_data["property"]


class Insight:
    """Insight is the instantiation of a HomeLINK Insight"""

    def __init__(self, raw_data: dict) -> None:
        """Initialize the property."""
        self._raw_data = raw_data

    @property
    def insightid(self) -> str:
        """Return the serialnumber of the Insight"""
        return self._raw_data["id"]

    @property
    def hl_type(self) -> str:
        """Return the type of the Insight"""
        return self._raw_data["type"]

    @property
    def risklevel(self) -> str:
        """Return the risk level of the Insight"""
        return self._raw_data["riskLevel"]

    @property
    def value(self) -> int:
        """Return the value of the Insight"""
        return self._raw_data["value"]

    @property
    def appliesto(self) -> str:
        """Return the applies to of the Insight"""
        return self._raw_data["appliesTo"]

    @property
    def propertyreference(self) -> str:
        """Return the propertyreference of the Insight"""
        return self._raw_data["propertyReference"]

    @property
    def location(self) -> str:
        """Return the location of the Insight"""
        return self._raw_data.get("location", None)

    @property
    def calculatedat(self) -> datetime | None:
        """Return the datetime of the Insight calculation"""
        return parse_date(self._raw_data.get("calculatedAt", None))

    @property
    def rel(self) -> Rel:
        """Return the tags of the Insight"""
        return Rel(self._raw_data["_rel"])
