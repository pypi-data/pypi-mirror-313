# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["RecentListParams"]


class RecentListParams(TypedDict, total=False):
    back: int
    """The number of days back to fetch observations."""

    cat: Literal["species", "slash", "issf", "spuh", "hybrid", "domestic", "form", "intergrade"]
    """Only fetch observations from these taxonomic categories"""

    hotspot: bool
    """Only fetch observations from hotspots"""

    include_provisional: Annotated[bool, PropertyInfo(alias="includeProvisional")]
    """Include observations which have not yet been reviewed"""

    max_results: Annotated[int, PropertyInfo(alias="maxResults")]
    """Only fetch this number of observations"""

    r: List[str]
    """Fetch observations from up to 10 locations"""

    spp_locale: Annotated[str, PropertyInfo(alias="sppLocale")]
    """Use this language for species common names"""
