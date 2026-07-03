from datetime import datetime

from sqlalchemy.orm import Session

from app.models.auth import LoginHistory
from app.models.auth import RevokedToken


class AuthRepository:
    @staticmethod
    def get_revoked_token(db: Session, jti: str) -> RevokedToken | None:
        return (
            db.query(RevokedToken)
            .filter(RevokedToken.jti == jti)
            .first()
        )

    @staticmethod
    def revoke_token(
        db: Session,
        jti: str,
        user_id: int,
        expires_at: datetime,
        reason: str = "logout",
    ) -> RevokedToken:
        existing_token = AuthRepository.get_revoked_token(db, jti)
        if existing_token is not None:
            return existing_token

        revoked_token = RevokedToken(
            jti=jti,
            user_id=user_id,
            expires_at=expires_at,
            reason=reason,
        )
        db.add(revoked_token)
        db.commit()
        db.refresh(revoked_token)
        return revoked_token

    @staticmethod
    def create_login_history(
        db: Session,
        mobile_number: str,
        success: bool,
        user_id: int | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        failure_reason: str | None = None,
    ) -> LoginHistory:
        login_history = LoginHistory(
            user_id=user_id,
            mobile_number=mobile_number,
            success=success,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason=failure_reason,
        )
        db.add(login_history)
        db.commit()
        db.refresh(login_history)
        return login_history
