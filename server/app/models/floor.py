from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
)

from app.database.base import BaseModel


class Floor(BaseModel):

    __tablename__ = "floors"

    id = Column(Integer, primary_key=True)

    survey_id = Column(
        Integer,
        ForeignKey("surveys.id"),
    )

    floor_name = Column(String(50))

    usage = Column(String(100))

    construction_type = Column(String(100))

    area = Column(Float)

    tax = Column(Float)