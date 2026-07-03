from datetime import datetime, timedelta, timezone
import re
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def validate_password(password: str) -> None:
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain one uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain one lowercase letter.")

    if not re.search(r"\d", password):
        raise ValueError("Password must contain one number.")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain one special character.")


def create_access_token(data: dict) -> str:
    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = data.copy()
    to_encode.update(
        {
            "iat": issued_at,
            "exp": expires_at,
            "jti": uuid4().hex,
            "typ": "access",
        }
    )

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        return None

    if payload.get("typ") != "access":
        return None

    return payload


def get_token_expiry(payload: dict) -> datetime:
    expires_at = payload.get("exp")
    if expires_at is None:
        raise ValueError("Token expiry is missing.")

    return datetime.fromtimestamp(int(expires_at), tz=timezone.utc)
