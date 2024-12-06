# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ...._models import BaseModel

__all__ = ["ListListResponse", "ListListResponseItem"]


class ListListResponseItem(BaseModel):
    code: Optional[str] = None

    name: Optional[str] = None


ListListResponse: TypeAlias = List[ListListResponseItem]
