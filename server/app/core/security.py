from datetime import datetime, timedelta
import re

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash plain password.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify password.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def validate_password(password: str):
    """
    Password Policy

    Minimum 8 characters
    1 Uppercase
    1 Lowercase
    1 Number
    1 Special Character
    """

    if len(password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters."
        )

    if not re.search(r"[A-Z]", password):
        raise ValueError(
            "Password must contain one uppercase letter."
        )

    if not re.search(r"[a-z]", password):
        raise ValueError(
            "Password must contain one lowercase letter."
        )

    if not re.search(r"\d", password):
        raise ValueError(
            "Password must contain one number."
        )

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError(
            "Password must contain one special character."
        )


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {"exp": expire}
    )

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        return payload

    except JWTError:

        return None