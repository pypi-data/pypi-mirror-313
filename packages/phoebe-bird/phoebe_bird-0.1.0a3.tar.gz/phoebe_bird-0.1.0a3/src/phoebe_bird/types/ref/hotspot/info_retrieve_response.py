# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["InfoRetrieveResponse"]


class InfoRetrieveResponse(BaseModel):
    country_code: Optional[str] = FieldInfo(alias="countryCode", default=None)

    country_name: Optional[str] = FieldInfo(alias="countryName", default=None)

    hierarchical_name: Optional[str] = FieldInfo(alias="hierarchicalName", default=None)

    is_hotspot: Optional[bool] = FieldInfo(alias="isHotspot", default=None)

    lat: Optional[float] = None

    latitude: Optional[float] = None

    lng: Optional[float] = None

    loc_id: Optional[str] = FieldInfo(alias="locId", default=None)

    loc_name: Optional[str] = FieldInfo(alias="locName", default=None)

    longitude: Optional[float] = None

    name: Optional[str] = None

    subnational1_code: Optional[str] = FieldInfo(alias="subnational1Code", default=None)

    subnational1_name: Optional[str] = FieldInfo(alias="subnational1Name", default=None)
