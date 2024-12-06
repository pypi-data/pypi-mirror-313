# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["StatRetrieveResponse"]


class StatRetrieveResponse(BaseModel):
    num_checklists: Optional[int] = FieldInfo(alias="numChecklists", default=None)

    num_contributors: Optional[int] = FieldInfo(alias="numContributors", default=None)

    num_species: Optional[int] = FieldInfo(alias="numSpecies", default=None)
