# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["SpeciesGroupListResponse", "SpeciesGroupListResponseItem"]


class SpeciesGroupListResponseItem(BaseModel):
    group_name: Optional[str] = FieldInfo(alias="groupName", default=None)

    group_order: Optional[int] = FieldInfo(alias="groupOrder", default=None)

    taxon_order_bounds: Optional[List[List[float]]] = FieldInfo(alias="taxonOrderBounds", default=None)


SpeciesGroupListResponse: TypeAlias = List[SpeciesGroupListResponseItem]
