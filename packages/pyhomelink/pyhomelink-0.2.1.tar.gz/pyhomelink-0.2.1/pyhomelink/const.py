"""Constants."""
from enum import StrEnum

ATTR_RESULTS = "results"

AUTH_URL = "https://auth.live.homelync.io/oauth2?client={0}&secret={1}"
BASE_URL = "https://frontier.live.homelync.io/v1/"

HTTP_OK = 200

LOOKUPEVENTTYPE = "eventType"
MODELTYPE_ENVIRONMENT = "ENV"
MODELTYPE_CO2 = "CO2"


class HomeLINKEndpoint(StrEnum):
    """HomeLINK Endpoints."""

    PROPERTIES = "property"
    PROPERTY = "property/{propertyreference}"
    PROPERTY_DEVICES = "property/{propertyreference}/devices"
    PROPERTY_ALERTS = "property/{propertyreference}/alerts"
    PROPERTY_INSIGHTS = "property/{propertyreference}/insights"
    PROPERTY_READINGS = "property/{propertyreference}/readings?date={date}"
    PROPERTY_TAGS = "property/{propertyreference}/tags"
    DEVICES = "device"
    DEVICE = "device/{serialnumber}"
    DEVICE_ALERTS = "device/{serialnumber}/alerts"
    DEVICE_READINGS = "device/{serialnumber}/readings/{readingtype}"
    INSIGHTS = "insight"
    INSIGHT = "insight/{insightid}"
    LOOKUPS = "lookup/{lookuptype}"
    LOOKUP = "lookup/{lookuptype}/{lookupid}"


class HomeLINKReadingType(StrEnum):
    """HomeLINK Endpoints."""

    CO2 = "environment-co2-indoor"
    HUMIDITY = "environment-humidity-indoor"
    TEMPERATURE = "environment-temperature-indoor"
