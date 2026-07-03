from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class GalleryCreate(BaseModel):
    survey_id: int = Field(..., gt=0)
    image_path: str = Field(..., min_length=1, max_length=300)
    image_type: str = Field(..., min_length=1, max_length=50)


class GalleryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    survey_id: int
    image_path: str
    image_type: str
    created_at: datetime
    updated_at: datetime
