# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["NotableListParams"]


class NotableListParams(TypedDict, total=False):
    back: int
    """The number of days back to fetch observations."""

    detail: Literal["simple", "full"]
    """Include a subset (simple), or all (full), of the fields available."""

    hotspot: bool
    """Only fetch observations from hotspots"""

    max_results: Annotated[int, PropertyInfo(alias="maxResults")]
    """Only fetch this number of observations"""

    r: List[str]
    """Fetch observations from up to 10 locations"""

    spp_locale: Annotated[str, PropertyInfo(alias="sppLocale")]
    """Use this language for species common names"""
