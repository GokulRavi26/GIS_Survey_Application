from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)

from app.database.base import BaseModel


class User(BaseModel):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    full_name = Column(String(100), nullable=False)

    mobile_number = Column(
        String(10),
        nullable=False,
        unique=True,
        index=True,
    )

    password = Column(String(255), nullable=False)

    role = Column(
        String(20),
        nullable=False,
        default="SURVEYOR",
    )

    is_active = Column(
        Boolean,
        default=True,
    )