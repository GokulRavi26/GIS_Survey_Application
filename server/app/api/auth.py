import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_token_payload
from app.core.dependencies import get_current_user
from app.schemas.auth import LoginRequest
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse
from app.utils.response import ApiResponse
from app.utils.response import success_response

from app.core.dependencies import get_database

from app.models.user import User
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

logger = logging.getLogger(__name__)


def build_token_response(user) -> ApiResponse[TokenResponse]:
    token = AuthService.create_login_token(user)

    return success_response(
        message="Login successful.",
        data={
            "access_token": token,
            "token_type": "bearer",
            "user": user,
        },
    )


def build_oauth_token_response(user) -> dict:
    token = AuthService.create_login_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user),
    }


def get_request_metadata(request: Request) -> tuple[str | None, str | None]:
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    return ip_address, user_agent


@router.post(
    "/login",
    response_model=ApiResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user with mobile number and password.",
)
def login(
    request: LoginRequest,
    http_request: Request,
    db: Session = Depends(get_database),
):
    user = AuthService.authenticate_user(
        db,
        request.mobile_number,
        request.password,
    )

    ip_address, user_agent = get_request_metadata(http_request)

    if not user:
        AuthService.record_login_attempt(
            db=db,
            mobile_number=request.mobile_number,
            success=False,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason="Invalid Mobile Number or Password",
        )
        logger.warning(
            "Failed login attempt for mobile number %s",
            request.mobile_number,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Mobile Number or Password",
        )

    AuthService.record_login_attempt(
        db=db,
        mobile_number=request.mobile_number,
        success=True,
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    return build_token_response(user)


@router.post(
    "/token",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="OAuth2-compatible login for Swagger Authorize.",
)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: Session = Depends(get_database),
):
    user = AuthService.authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    ip_address, user_agent = get_request_metadata(request)

    if not user:
        AuthService.record_login_attempt(
            db=db,
            mobile_number=form_data.username,
            success=False,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason="Invalid Mobile Number or Password",
        )
        logger.warning(
            "Failed Swagger login attempt for mobile number %s",
            form_data.username,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Mobile Number or Password",
        )

    AuthService.record_login_attempt(
        db=db,
        mobile_number=form_data.username,
        success=True,
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    return build_oauth_token_response(user)


@router.post(
    "/logout",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Logout current user and revoke the active JWT.",
)
def logout(
    payload: dict = Depends(get_current_token_payload),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    AuthService.revoke_token(
        db=db,
        payload=payload,
        user_id=current_user.id,
        reason="logout",
    )
    return success_response(message="Logged out successfully.")


@router.get(
    "/me",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get the currently authenticated user.",
)
def me(
    current_user: User = Depends(get_current_user),
):
    return success_response(
        message="Authenticated user loaded.",
        data=current_user,
    )
