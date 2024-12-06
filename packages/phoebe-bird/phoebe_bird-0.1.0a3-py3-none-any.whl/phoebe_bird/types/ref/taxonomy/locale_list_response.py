# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["LocaleListResponse", "LocaleListResponseItem"]


class LocaleListResponseItem(BaseModel):
    code: Optional[str] = None

    last_updated: Optional[str] = FieldInfo(alias="lastUpdated", default=None)

    name: Optional[str] = None


LocaleListResponse: TypeAlias = List[LocaleListResponseItem]
