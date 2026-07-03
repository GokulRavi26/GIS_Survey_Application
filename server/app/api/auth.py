from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest
from app.schemas.auth import TokenResponse

from app.core.dependencies import get_database

from app.core.security import create_access_token

from app.services.auth_service import authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=TokenResponse)
def login(

    request: LoginRequest,

    db: Session = Depends(get_database),

):

    user = authenticate_user(

        db,

        request.mobile_number,

        request.password,

    )

    if not user:

        raise HTTPException(

            status_code=401,

            detail="Invalid Mobile Number or Password",

        )

    token = create_access_token(

        {

            "sub": str(user.id),

            "role": user.role,

        }

    )

    return {

        "access_token": token,

        "token_type": "bearer",

    }