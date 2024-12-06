# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["Top100RetrieveResponse", "Top100RetrieveResponseItem"]


class Top100RetrieveResponseItem(BaseModel):
    num_complete_checklists: Optional[int] = FieldInfo(alias="numCompleteChecklists", default=None)

    num_species: Optional[int] = FieldInfo(alias="numSpecies", default=None)

    profile_handle: Optional[str] = FieldInfo(alias="profileHandle", default=None)

    row_num: Optional[int] = FieldInfo(alias="rowNum", default=None)

    user_display_name: Optional[str] = FieldInfo(alias="userDisplayName", default=None)

    user_id: Optional[str] = FieldInfo(alias="userId", default=None)


Top100RetrieveResponse: TypeAlias = List[Top100RetrieveResponseItem]
