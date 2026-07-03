from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.database.base import Base

from app.core.config import settings

engine = create_engine(

    settings.DATABASE_URL,

    connect_args={"check_same_thread": False}

)

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)

