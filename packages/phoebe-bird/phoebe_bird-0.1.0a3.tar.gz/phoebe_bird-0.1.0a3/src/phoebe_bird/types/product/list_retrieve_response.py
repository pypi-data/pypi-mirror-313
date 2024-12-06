# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "ListRetrieveResponse",
    "ListRetrieveResponseItem",
    "ListRetrieveResponseItemLoc",
    "ListRetrieveResponseItemOb",
    "ListRetrieveResponseItemObObsAux",
]


class ListRetrieveResponseItemLoc(BaseModel):
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


class ListRetrieveResponseItemObObsAux(BaseModel):
    aux_code: Optional[str] = FieldInfo(alias="auxCode", default=None)

    entry_method_code: Optional[str] = FieldInfo(alias="entryMethodCode", default=None)

    field_name: Optional[str] = FieldInfo(alias="fieldName", default=None)

    obs_id: Optional[str] = FieldInfo(alias="obsId", default=None)

    species_code: Optional[str] = FieldInfo(alias="speciesCode", default=None)

    sub_id: Optional[str] = FieldInfo(alias="subId", default=None)

    value: Optional[str] = None


class ListRetrieveResponseItemOb(BaseModel):
    obs_aux: Optional[List[ListRetrieveResponseItemObObsAux]] = FieldInfo(alias="obsAux", default=None)

    obs_dt: Optional[str] = FieldInfo(alias="obsDt", default=None)

    obs_id: Optional[str] = FieldInfo(alias="obsId", default=None)

    species_code: Optional[str] = FieldInfo(alias="speciesCode", default=None)


class ListRetrieveResponseItem(BaseModel):
    all_obs_reported: Optional[bool] = FieldInfo(alias="allObsReported", default=None)

    checklist_id: Optional[str] = FieldInfo(alias="checklistId", default=None)

    creation_dt: Optional[str] = FieldInfo(alias="creationDt", default=None)

    duration_hrs: Optional[float] = FieldInfo(alias="durationHrs", default=None)

    iso_obs_date: Optional[str] = FieldInfo(alias="isoObsDate", default=None)

    last_edited_dt: Optional[str] = FieldInfo(alias="lastEditedDt", default=None)

    loc: Optional[ListRetrieveResponseItemLoc] = None

    loc_id: Optional[str] = FieldInfo(alias="locId", default=None)

    num_observers: Optional[int] = FieldInfo(alias="numObservers", default=None)

    num_species: Optional[int] = FieldInfo(alias="numSpecies", default=None)

    obs: Optional[List[ListRetrieveResponseItemOb]] = None

    obs_dt: Optional[str] = FieldInfo(alias="obsDt", default=None)

    obs_time: Optional[str] = FieldInfo(alias="obsTime", default=None)

    obs_time_valid: Optional[bool] = FieldInfo(alias="obsTimeValid", default=None)

    proj_id: Optional[str] = FieldInfo(alias="projId", default=None)

    protocol_id: Optional[str] = FieldInfo(alias="protocolId", default=None)

    sub_id: Optional[str] = FieldInfo(alias="subId", default=None)

    submission_method_code: Optional[str] = FieldInfo(alias="submissionMethodCode", default=None)

    subnational1_code: Optional[str] = FieldInfo(alias="subnational1Code", default=None)

    user_display_name: Optional[str] = FieldInfo(alias="userDisplayName", default=None)


ListRetrieveResponse: TypeAlias = List[ListRetrieveResponseItem]
