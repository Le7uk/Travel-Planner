from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PlaceCreate(BaseModel):
    external_id: int


class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    visited: Optional[bool] = None


class PlaceResponse(BaseModel):
    id: int
    project_id: int
    external_id: int
    title: str
    artist: Optional[str]
    image_url: Optional[str]
    notes: Optional[str]
    visited: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
