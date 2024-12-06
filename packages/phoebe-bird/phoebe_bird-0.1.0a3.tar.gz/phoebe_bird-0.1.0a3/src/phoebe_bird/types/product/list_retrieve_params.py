# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ListRetrieveParams"]


class ListRetrieveParams(TypedDict, total=False):
    max_results: Annotated[int, PropertyInfo(alias="maxResults")]
    """Only fetch this number of checklists."""
