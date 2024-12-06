# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["Location", "GreaterRegion"]


class GreaterRegion(BaseModel):
    name: Optional[str] = None
    """Name of the greater region."""


class Location(BaseModel):
    city_name: str
    """Name of the city of the location."""

    country_iso2: str
    """Two-digit country abbreviation."""

    continent_name: Optional[str] = None
    """Name of the continent of the location."""

    country_iso3: Optional[str] = None
    """Three-digit country abbreviation."""

    country_name: Optional[str] = None
    """Name of the country for the location."""

    greater_regions: Optional[List[GreaterRegion]] = None
    """List of the greater regions encompassing the location."""

    house_number: Optional[str] = None
    """House number for the location."""

    latitude: Optional[float] = None
    """Latitude for the location."""

    location_type: Optional[str] = None
    """Indicates if the location is the HQ or location of business."""

    longitude: Optional[float] = None
    """Longitude for the location."""

    macro_region: Optional[str] = None
    """Macro region for the location."""

    micro_region: Optional[str] = None
    """Micro region for the location."""

    postal_code: Optional[str] = None
    """Postal code of location."""

    raw_address: Optional[str] = None
    """The location's full address."""

    region_iso: Optional[str] = None
    """Region abbreviation of the location."""

    region_name: Optional[str] = None
    """Name of the region for the location."""

    street: Optional[str] = None
    """Street name of the location."""
