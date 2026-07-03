from datetime import datetime
from typing import Literal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

RoleName = Literal["ADMIN", "SUPERVISOR", "SURVEYOR"]


def validate_mobile_number(value: str) -> str:
    cleaned_value = value.strip()
    if not cleaned_value.isdigit():
        raise ValueError("Mobile number must contain digits only.")
    if len(cleaned_value) != 10:
        raise ValueError("Mobile number must contain exactly 10 digits.")
    return cleaned_value


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    mobile_number: str = Field(..., min_length=10, max_length=10)
    password: str = Field(..., min_length=8)
    role: RoleName = "SURVEYOR"

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        cleaned_value = value.strip()
        if len(cleaned_value) < 3:
            raise ValueError("Full name must contain at least 3 characters.")
        return cleaned_value

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile(cls, value: str) -> str:
        return validate_mobile_number(value)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    mobile_number: Optional[str] = Field(default=None, min_length=10, max_length=10)
    role: Optional[RoleName] = None
    is_active: Optional[bool] = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned_value = value.strip()
        if len(cleaned_value) < 3:
            raise ValueError("Full name must contain at least 3 characters.")
        return cleaned_value

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_mobile_number(value)


class PasswordReset(BaseModel):
    new_password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    mobile_number: str
    role: RoleName
    is_active: bool
    created_at: datetime
    updated_at: datetime
