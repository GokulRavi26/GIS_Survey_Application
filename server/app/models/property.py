from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
)

from app.database.base import BaseModel


class Property(BaseModel):

    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)

    assessment_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    ward_name = Column(String(100))

    street_name = Column(String(150))

    owner_name = Column(String(200))

    door_number = Column(String(50))

    mobile_number = Column(String(20))

    half_year_tax = Column(Float, default=0)

    balance = Column(Float, default=0)

    survey_status = Column(
        String(30),
        default="Pending",
    )