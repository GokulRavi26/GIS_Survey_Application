from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Base directory (server/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Storage directories
DATABASE_DIR = BASE_DIR / "database"
UPLOAD_DIR = BASE_DIR / "uploads"
EXPORT_DIR = BASE_DIR / "exports"

# Create directories if they don't exist
DATABASE_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)

# SQLite database path
DATABASE_PATH = DATABASE_DIR / "survey.db"


class Settings:

    # ===========================
    # Application
    # ===========================
    APP_NAME = os.getenv(
        "APP_NAME",
        "GIS Survey Application"
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    # ===========================
    # Security
    # ===========================
    SECRET_KEY = os.getenv("SECRET_KEY")

    ALGORITHM = os.getenv(
        "ALGORITHM",
        "HS256"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    )

    # ===========================
    # Database
    # ===========================
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

    # ===========================
    # Default Admin
    # ===========================
    DEFAULT_ADMIN_NAME = os.getenv(
        "DEFAULT_ADMIN_NAME",
        "Administrator"
    )

    DEFAULT_ADMIN_MOBILE = os.getenv(
        "DEFAULT_ADMIN_MOBILE",
        "638698277"
    )

    DEFAULT_ADMIN_PASSWORD = os.getenv(
        "DEFAULT_ADMIN_PASSWORD",
        "Imikod@321"
    )

    DEFAULT_ADMIN_ROLE = os.getenv(
        "DEFAULT_ADMIN_ROLE",
        "ADMIN"
    )


settings = Settings()