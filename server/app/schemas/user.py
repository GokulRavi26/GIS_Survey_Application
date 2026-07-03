from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):

    full_name: str = Field(..., min_length=3)

    mobile_number: str = Field(..., min_length=10, max_length=10)

    password: str

    role: str = "SURVEYOR"


class UserResponse(BaseModel):

    id: int

    full_name: str

    mobile_number: str

    role: str

    is_active: bool

    class Config:
        from_attributes = True