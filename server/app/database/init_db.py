import logging

from app.database.database import engine, SessionLocal
from app.database.base import Base

from app.models import *

from app.services.bootstrap_service import create_default_admin

logger = logging.getLogger(__name__)


def create_tables() -> None:
    logger.info("Creating database tables when missing.")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        create_default_admin(db)
    finally:
        db.close()
