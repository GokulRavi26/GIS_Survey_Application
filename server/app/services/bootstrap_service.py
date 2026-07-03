import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.user_service import UserService

logger = logging.getLogger(__name__)


def create_default_admin(db: Session):
    admin = UserRepository.get_by_mobile(
        db,
        settings.DEFAULT_ADMIN_MOBILE,
    )

    if admin:
        logger.info("Default admin already exists.")
        return

    admin_payload = UserCreate(
        full_name=settings.DEFAULT_ADMIN_NAME,
        mobile_number=settings.DEFAULT_ADMIN_MOBILE,
        password=settings.DEFAULT_ADMIN_PASSWORD,
        role=settings.DEFAULT_ADMIN_ROLE,
    )

    UserService.create_user(db, admin_payload)
    logger.info("Default admin created successfully.")
