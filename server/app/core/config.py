import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

DATABASE_DIR = BASE_DIR / "database"
UPLOAD_DIR = BASE_DIR / "uploads"
EXPORT_DIR = BASE_DIR / "exports"
LOG_DIR = BASE_DIR / "logs"
DATABASE_PATH = DATABASE_DIR / "survey.db"


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "GIS Survey Application")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    API_V1_PREFIX: str = os.getenv("API_V1_PREFIX", "/api/v1")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_PATH}")
    DATABASE_CONNECT_TIMEOUT_SECONDS: int = int(
        os.getenv("DATABASE_CONNECT_TIMEOUT_SECONDS", "30")
    )

    DEFAULT_ADMIN_NAME: str = os.getenv("DEFAULT_ADMIN_NAME", "Administrator")
    DEFAULT_ADMIN_MOBILE: str = os.getenv("DEFAULT_ADMIN_MOBILE", "9999999999")
    DEFAULT_ADMIN_PASSWORD: str = os.getenv(
        "DEFAULT_ADMIN_PASSWORD",
        "ChangeMe@123",
    )
    DEFAULT_ADMIN_ROLE: str = os.getenv("DEFAULT_ADMIN_ROLE", "ADMIN")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", str(LOG_DIR / "app.log"))

    BACKEND_CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "BACKEND_CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]

    def validate(self) -> None:
        if not self.SECRET_KEY:
            raise RuntimeError("SECRET_KEY must be configured in server/.env.")

        if self.ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
            raise RuntimeError(
                "ACCESS_TOKEN_EXPIRE_MINUTES must be greater than zero."
            )

    def ensure_storage_directories(self) -> None:
        for directory in (DATABASE_DIR, UPLOAD_DIR, EXPORT_DIR, LOG_DIR):
            directory.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_storage_directories()
settings.validate()
