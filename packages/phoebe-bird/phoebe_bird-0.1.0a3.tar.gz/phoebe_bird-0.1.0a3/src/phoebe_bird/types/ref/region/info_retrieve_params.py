# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["InfoRetrieveParams"]


class InfoRetrieveParams(TypedDict, total=False):
    delim: str
    """The characters used to separate elements in the name."""

    region_name_format: Annotated[
        Literal["detailed", "detailednoqual", "full", "namequal", "nameonly", "revdetailed"],
        PropertyInfo(alias="regionNameFormat"),
    ]
    """Control how the name is displayed."""
