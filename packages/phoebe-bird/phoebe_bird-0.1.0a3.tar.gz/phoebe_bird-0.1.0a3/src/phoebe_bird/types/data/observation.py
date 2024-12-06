# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["Observation"]


class Observation(BaseModel):
    id: Optional[int] = None

    com_name: Optional[str] = FieldInfo(alias="comName", default=None)

    firstname: Optional[str] = None

    how_many: Optional[int] = FieldInfo(alias="howMany", default=None)

    lastname: Optional[str] = None

    lat: Optional[float] = None

    lng: Optional[float] = None

    location_private: Optional[bool] = FieldInfo(alias="locationPrivate", default=None)

    loc_id: Optional[str] = FieldInfo(alias="locId", default=None)

    loc_name: Optional[str] = FieldInfo(alias="locName", default=None)

    obs_dt: Optional[str] = FieldInfo(alias="obsDt", default=None)

    obs_reviewed: Optional[bool] = FieldInfo(alias="obsReviewed", default=None)

    obs_valid: Optional[bool] = FieldInfo(alias="obsValid", default=None)

    sci_name: Optional[str] = FieldInfo(alias="sciName", default=None)

    species_code: Optional[str] = FieldInfo(alias="speciesCode", default=None)

    sub_id: Optional[str] = FieldInfo(alias="subId", default=None)
