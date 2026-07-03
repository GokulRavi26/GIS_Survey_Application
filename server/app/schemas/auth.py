from pydantic import BaseModel, Field, field_validator

from app.schemas.user import UserResponse
from app.schemas.user import validate_mobile_number


class LoginRequest(BaseModel):
    mobile_number: str = Field(..., min_length=10, max_length=10)
    password: str = Field(..., min_length=1)

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile(cls, value: str) -> str:
        return validate_mobile_number(value)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class LogoutResponse(BaseModel):
    message: str
