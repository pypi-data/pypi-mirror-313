# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["VersionListResponse", "VersionListResponseItem"]


class VersionListResponseItem(BaseModel):
    authority_ver: Optional[float] = FieldInfo(alias="authorityVer", default=None)

    latest: Optional[bool] = None


VersionListResponse: TypeAlias = List[VersionListResponseItem]
