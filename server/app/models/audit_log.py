from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)

from app.database.base import BaseModel


class AuditLog(BaseModel):

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)

    user = Column(String(100))

    action = Column(String(100))

    description = Column(Text)