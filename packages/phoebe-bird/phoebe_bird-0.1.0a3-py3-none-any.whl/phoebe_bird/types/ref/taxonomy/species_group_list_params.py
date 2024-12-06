# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["SpeciesGroupListParams"]


class SpeciesGroupListParams(TypedDict, total=False):
    group_name_locale: Annotated[str, PropertyInfo(alias="groupNameLocale")]
    """Locale for species group names.

    English names are returned for any non-listed locale or any non-translated group
    name.
    """
