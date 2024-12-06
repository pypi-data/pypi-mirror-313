"""Python module for accessing HomeLINK Lookup."""


class Lookup:
    """Lookup is the instantiation of a HomeLINK Lookup"""

    def __init__(self, raw_data: dict) -> None:
        """Initialize the property."""
        self._raw_data = raw_data

    @property
    def lookupid(self) -> str:
        """Return the id of the Lookup"""
        return self._raw_data["id"]

    @property
    def code(self) -> str:
        """Return the codet of the Lookup"""
        return self._raw_data["code"]

    @property
    def name(self) -> str:
        """Return the name of the Lookup"""
        return self._raw_data["name"]

    @property
    def description(self) -> str:
        """Return the description of the Lookup"""
        return self._raw_data["description"]

    @property
    def active(self) -> bool:
        """Return the active of the Lookup"""
        return self._raw_data["active"]


class LookupEventType(Lookup):
    """LookupEventType is the instantiation of a HomeLINK EventType Lookup"""

    @property
    def eventcategoryid(self) -> str:
        """Return the category of the Lookup"""
        return self._raw_data["eventCategoryId"]

    @property
    def severityid(self) -> str:
        """Return the severity of the Lookup"""
        return self._raw_data["severityId"]
