# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["HistoricListParams"]


class HistoricListParams(TypedDict, total=False):
    region_code: Required[Annotated[str, PropertyInfo(alias="regionCode")]]

    y: Required[int]

    m: Required[int]

    cat: Literal["species", "slash", "issf", "spuh", "hybrid", "domestic", "form", "intergrade"]
    """Only fetch observations from these taxonomic categories"""

    detail: Literal["simple", "full"]
    """Include a subset (simple), or all (full), of the fields available."""

    hotspot: bool
    """Only fetch observations from hotspots"""

    include_provisional: Annotated[bool, PropertyInfo(alias="includeProvisional")]
    """Include observations which have not yet been reviewed."""

    max_results: Annotated[int, PropertyInfo(alias="maxResults")]
    """Only fetch this number of observations"""

    r: List[str]
    """Fetch observations from up to 50 locations"""

    rank: Literal["mrec", "create"]
    """Include latest observation of the day, or the first added"""

    spp_locale: Annotated[str, PropertyInfo(alias="sppLocale")]
    """Use this language for species common names"""
