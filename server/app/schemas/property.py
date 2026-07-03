from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

SurveyStatus = Literal["Pending", "In Progress", "Completed"]


class PropertyBase(BaseModel):
    assessment_number: str = Field(..., min_length=1, max_length=50)
    ward_name: str | None = Field(default=None, max_length=100)
    street_name: str | None = Field(default=None, max_length=150)
    owner_name: str | None = Field(default=None, max_length=200)
    door_number: str | None = Field(default=None, max_length=50)
    mobile_number: str | None = Field(default=None, max_length=20)
    half_year_tax: float = Field(default=0, ge=0)
    balance: float = Field(default=0, ge=0)
    survey_status: SurveyStatus = "Pending"

    @field_validator(
        "assessment_number",
        "ward_name",
        "street_name",
        "owner_name",
        "door_number",
        "mobile_number",
        mode="before",
    )
    @classmethod
    def clean_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = str(value).strip()
        return cleaned or None


class PropertyCreate(PropertyBase):
    """Payload for creating a property register record."""


class PropertyUpdate(BaseModel):
    ward_name: str | None = Field(default=None, max_length=100)
    street_name: str | None = Field(default=None, max_length=150)
    owner_name: str | None = Field(default=None, max_length=200)
    door_number: str | None = Field(default=None, max_length=50)
    mobile_number: str | None = Field(default=None, max_length=20)
    half_year_tax: float | None = Field(default=None, ge=0)
    balance: float | None = Field(default=None, ge=0)
    survey_status: SurveyStatus | None = None


class PropertyResponse(PropertyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class PropertySearchResponse(BaseModel):
    items: list[PropertyResponse]
    total: int
    offset: int
    limit: int
