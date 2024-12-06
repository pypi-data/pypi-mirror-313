# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ...._models import BaseModel

__all__ = ["AdjacentListResponse", "AdjacentListResponseItem"]


class AdjacentListResponseItem(BaseModel):
    code: Optional[str] = None

    name: Optional[str] = None


AdjacentListResponse: TypeAlias = List[AdjacentListResponseItem]
