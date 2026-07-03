from datetime import datetime

from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.core.security import get_token_expiry
from app.core.security import verify_password
from app.models.user import User
from app.repositories.auth_repository import AuthRepository
from app.services.user_service import get_user_by_mobile


class AuthService:
    @staticmethod
    def authenticate_user(
        db: Session,
        mobile: str,
        password: str,
    ) -> User | None:
        user = get_user_by_mobile(db, mobile)

        if not user:
            return None

        if not user.is_active:
            return None

        if not verify_password(password, user.password):
            return None

        return user

    @staticmethod
    def create_login_token(user: User) -> str:
        return create_access_token(
            {
                "sub": str(user.id),
                "role": user.role,
                "mobile_number": user.mobile_number,
            }
        )

    @staticmethod
    def is_token_revoked(db: Session, jti: str) -> bool:
        return AuthRepository.get_revoked_token(db, jti) is not None

    @staticmethod
    def revoke_token(
        db: Session,
        payload: dict,
        user_id: int,
        reason: str = "logout",
    ) -> None:
        jti = payload.get("jti")
        if not jti:
            raise ValueError("Token id is missing.")

        expires_at = get_token_expiry(payload)
        AuthRepository.revoke_token(
            db=db,
            jti=jti,
            user_id=user_id,
            expires_at=expires_at,
            reason=reason,
        )

    @staticmethod
    def record_login_attempt(
        db: Session,
        mobile_number: str,
        success: bool,
        user_id: int | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        failure_reason: str | None = None,
    ) -> None:
        AuthRepository.create_login_history(
            db=db,
            mobile_number=mobile_number,
            success=success,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason=failure_reason,
        )


def authenticate_user(
    db: Session,
    mobile: str,
    password: str,
) -> User | None:
    return AuthService.authenticate_user(db, mobile, password)
