from sqlalchemy.orm import Session

from app.models.user import User

from app.services.user_service import get_user_by_mobile

from app.core.security import verify_password


def authenticate_user(

    db: Session,

    mobile: str,

    password: str,

):

    user = get_user_by_mobile(db, mobile)

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user