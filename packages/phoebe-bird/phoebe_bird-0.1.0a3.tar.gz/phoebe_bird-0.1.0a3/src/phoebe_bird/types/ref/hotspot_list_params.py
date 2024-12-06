# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["HotspotListParams"]


class HotspotListParams(TypedDict, total=False):
    back: int
    """The number of days back to fetch hotspots."""

    fmt: Literal["csv", "json"]
    """Fetch the records in CSV or JSON format."""
