from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)

from app.database.base import BaseModel


class Gallery(BaseModel):

    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True)

    survey_id = Column(
        Integer,
        ForeignKey("surveys.id"),
    )

    image_path = Column(String(300))

    image_type = Column(String(50))