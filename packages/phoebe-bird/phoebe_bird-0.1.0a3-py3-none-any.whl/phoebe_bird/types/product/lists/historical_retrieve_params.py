# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["HistoricalRetrieveParams"]


class HistoricalRetrieveParams(TypedDict, total=False):
    region_code: Required[Annotated[str, PropertyInfo(alias="regionCode")]]

    y: Required[int]

    m: Required[int]

    max_results: Annotated[int, PropertyInfo(alias="maxResults")]
    """Only fetch this number of checklists."""

    sort_key: Annotated[Literal["obs_dt", "creation_dt"], PropertyInfo(alias="sortKey")]
    """Order the results by the date of the checklist or by the date it was submitted."""
