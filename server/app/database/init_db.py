from app.database.database import engine, SessionLocal
from app.database.base import Base

# Import all models
from app.models import *

from app.services.bootstrap_service import create_default_admin


def create_tables():

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        create_default_admin(db)
    finally:
        db.close()