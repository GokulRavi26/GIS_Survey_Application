import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_database
from app.core.dependencies import require_roles
from app.models.user import User
from app.schemas.user import PasswordReset
from app.schemas.user import UserCreate
from app.schemas.user import UserResponse
from app.schemas.user import UserUpdate
from app.services.user_service import UserService
from app.utils.response import ApiResponse
from app.utils.response import success_response

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

logger = logging.getLogger(__name__)


@router.get(
    "",
    response_model=ApiResponse[list[UserResponse]],
    summary="List all users.",
)
def list_users(
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR")),
):
    users = UserService.list_users(db)
    return success_response(
        message="Users loaded successfully.",
        data=users,
    )


@router.post(
    "",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user.",
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_roles("ADMIN")),
):
    try:
        user = UserService.create_user(db, payload, current_user)
        return success_response(
            message="User created successfully.",
            data=user,
        )
    except ValueError as exc:
        logger.warning("User creation failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
    summary="Get a user by id.",
)
def get_user(
    user_id: int,
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR")),
):
    try:
        user = UserService.get_user(db, user_id)
        return success_response(
            message="User loaded successfully.",
            data=user,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
    summary="Update a user.",
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_roles("ADMIN")),
):
    try:
        user = UserService.update_user(db, user_id, payload, current_user)
        return success_response(
            message="User updated successfully.",
            data=user,
        )
    except ValueError as exc:
        status_code = (
            status.HTTP_404_NOT_FOUND
            if str(exc) == "User not found."
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(
            status_code=status_code,
            detail=str(exc),
        ) from exc


@router.post(
    "/{user_id}/reset-password",
    response_model=ApiResponse[UserResponse],
    summary="Reset a user's password.",
)
def reset_password(
    user_id: int,
    payload: PasswordReset,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_roles("ADMIN")),
):
    try:
        user = UserService.reset_password(
            db,
            user_id,
            payload.new_password,
            current_user,
        )
        return success_response(
            message="Password reset successfully.",
            data=user,
        )
    except ValueError as exc:
        status_code = (
            status.HTTP_404_NOT_FOUND
            if str(exc) == "User not found."
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(
            status_code=status_code,
            detail=str(exc),
        ) from exc


@router.post(
    "/{user_id}/activate",
    response_model=ApiResponse[UserResponse],
    summary="Activate a user.",
)
def activate_user(
    user_id: int,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_roles("ADMIN")),
):
    try:
        user = UserService.activate_user(db, user_id, current_user)
        return success_response(
            message="User activated successfully.",
            data=user,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "/{user_id}/deactivate",
    response_model=ApiResponse[UserResponse],
    summary="Deactivate a user.",
)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_roles("ADMIN")),
):
    try:
        user = UserService.deactivate_user(
            db,
            user_id,
            current_user.id,
            current_user,
        )
        return success_response(
            message="User deactivated successfully.",
            data=user,
        )
    except ValueError as exc:
        status_code = (
            status.HTTP_404_NOT_FOUND
            if str(exc) == "User not found."
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(
            status_code=status_code,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{user_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete a user.",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_roles("ADMIN")),
):
    try:
        UserService.delete_user(db, user_id, current_user.id, current_user)
    except ValueError as exc:
        status_code = (
            status.HTTP_404_NOT_FOUND
            if str(exc) == "User not found."
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(
            status_code=status_code,
            detail=str(exc),
        ) from exc

    return success_response(message="User deleted successfully.")
