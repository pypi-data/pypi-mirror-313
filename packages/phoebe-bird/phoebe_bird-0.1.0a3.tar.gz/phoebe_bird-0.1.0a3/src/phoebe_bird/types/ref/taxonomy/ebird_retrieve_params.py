# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["EbirdRetrieveParams"]


class EbirdRetrieveParams(TypedDict, total=False):
    cat: str
    """Only fetch records from these taxonomic categories."""

    fmt: Literal["csv", "json"]
    """Fetch the records in CSV or JSON format."""

    locale: str
    """Use this language for common names."""

    species: str
    """Only fetch records for these species."""

    version: str
    """Fetch a specific version of the taxonomy."""
