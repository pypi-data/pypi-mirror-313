# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["Top100RetrieveParams"]


class Top100RetrieveParams(TypedDict, total=False):
    region_code: Required[Annotated[str, PropertyInfo(alias="regionCode")]]

    y: Required[int]

    m: Required[int]

    max_results: Annotated[int, PropertyInfo(alias="maxResults")]
    """Only fetch this number of contributors."""

    ranked_by: Annotated[Literal["spp", "cl"], PropertyInfo(alias="rankedBy")]
    """Order by number of complete checklists (cl) or by number of species seen (spp)."""
