# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["RecentListParams"]


class RecentListParams(TypedDict, total=False):
    lat: Required[float]

    lng: Required[float]

    back: int
    """The number of days back to fetch observations."""

    cat: Literal["species", "slash", "issf", "spuh", "hybrid", "domestic", "form", "intergrade"]
    """Only fetch observations from these taxonomic categories"""

    dist: int
    """The search radius from the given position, in kilometers."""

    hotspot: bool
    """Only fetch observations from hotspots"""

    include_provisional: Annotated[bool, PropertyInfo(alias="includeProvisional")]
    """Include observations which have not yet been reviewed."""

    max_results: Annotated[int, PropertyInfo(alias="maxResults")]
    """Only fetch this number of observations"""

    sort: Literal["date", "species"]
    """Sort observations by taxonomy or by date, most recent first."""

    spp_locale: Annotated[str, PropertyInfo(alias="sppLocale")]
    """Use this language for species common names"""
