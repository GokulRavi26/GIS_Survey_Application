from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    Text,
)

from app.database.base import BaseModel


class Survey(BaseModel):

    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True)

    property_id = Column(
        Integer,
        ForeignKey("properties.id"),
    )

    latitude = Column(Float)

    longitude = Column(Float)

    remarks = Column(Text)

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
    )