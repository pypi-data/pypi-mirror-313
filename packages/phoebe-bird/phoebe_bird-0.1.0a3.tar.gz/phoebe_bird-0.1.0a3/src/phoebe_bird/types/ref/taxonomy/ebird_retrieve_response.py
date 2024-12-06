# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["EbirdRetrieveResponse", "EbirdRetrieveResponseItem"]


class EbirdRetrieveResponseItem(BaseModel):
    banding_codes: Optional[List[str]] = FieldInfo(alias="bandingCodes", default=None)

    category: Optional[str] = None

    com_name: Optional[str] = FieldInfo(alias="comName", default=None)

    com_name_codes: Optional[List[str]] = FieldInfo(alias="comNameCodes", default=None)

    family_code: Optional[str] = FieldInfo(alias="familyCode", default=None)

    family_com_name: Optional[str] = FieldInfo(alias="familyComName", default=None)

    family_sci_name: Optional[str] = FieldInfo(alias="familySciName", default=None)

    order: Optional[str] = None

    sci_name: Optional[str] = FieldInfo(alias="sciName", default=None)

    sci_name_codes: Optional[List[str]] = FieldInfo(alias="sciNameCodes", default=None)

    species_code: Optional[str] = FieldInfo(alias="speciesCode", default=None)

    taxon_order: Optional[int] = FieldInfo(alias="taxonOrder", default=None)


EbirdRetrieveResponse: TypeAlias = List[EbirdRetrieveResponseItem]
