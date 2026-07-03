from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.session import get_db


def get_database():

    db: Session = next(get_db())

    try:
        yield db

    finally:
        db.close()