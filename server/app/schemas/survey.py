from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.floor import FloorCreate, FloorResponse
from app.schemas.gallery import GalleryResponse


class SurveyBase(BaseModel):
    property_id: int = Field(..., gt=0)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    remarks: str | None = Field(default=None, max_length=5000)


class SurveyCreate(SurveyBase):
    floors: list[FloorCreate] = Field(default_factory=list)


class SurveyUpdate(BaseModel):
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    remarks: str | None = Field(default=None, max_length=5000)
    floors: list[FloorCreate] | None = None


class SurveyResponse(SurveyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    floors: list[FloorResponse] = Field(default_factory=list)
    gallery: list[GalleryResponse] = Field(default_factory=list)


class SurveyListResponse(BaseModel):
    items: list[SurveyResponse]
    total: int
    offset: int
    limit: int
