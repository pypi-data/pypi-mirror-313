# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["GeoRetrieveParams"]


class GeoRetrieveParams(TypedDict, total=False):
    lat: Required[float]

    lng: Required[float]

    back: int
    """The number of days back to fetch hotspots."""

    dist: int
    """The search radius from the given position, in kilometers."""

    fmt: Literal["csv", "json"]
    """Fetch the records in CSV or JSON format."""
