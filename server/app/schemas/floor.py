from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FloorBase(BaseModel):
    floor_name: str = Field(..., min_length=1, max_length=50)
    usage: str | None = Field(default=None, max_length=100)
    construction_type: str | None = Field(default=None, max_length=100)
    area: float = Field(default=0, ge=0)
    tax: float = Field(default=0, ge=0)

    @field_validator("floor_name", "usage", "construction_type", mode="before")
    @classmethod
    def clean_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = str(value).strip()
        return cleaned or None


class FloorCreate(FloorBase):
    """Payload for adding floor information to a survey."""


class FloorResponse(FloorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    survey_id: int
    created_at: datetime
    updated_at: datetime
