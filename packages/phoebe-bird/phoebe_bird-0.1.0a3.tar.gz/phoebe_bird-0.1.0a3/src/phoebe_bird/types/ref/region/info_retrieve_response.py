# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["InfoRetrieveResponse", "Bounds"]


class Bounds(BaseModel):
    max_x: Optional[float] = FieldInfo(alias="maxX", default=None)

    max_y: Optional[float] = FieldInfo(alias="maxY", default=None)

    min_x: Optional[float] = FieldInfo(alias="minX", default=None)

    min_y: Optional[float] = FieldInfo(alias="minY", default=None)


class InfoRetrieveResponse(BaseModel):
    bounds: Optional[Bounds] = None

    result: Optional[str] = None
