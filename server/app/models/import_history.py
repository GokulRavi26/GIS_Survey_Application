from sqlalchemy import Column, Integer, String, Text

from app.database.base import BaseModel


class ImportHistory(BaseModel):
    __tablename__ = "import_history"

    id = Column(Integer, primary_key=True)
    file_name = Column(String(255), nullable=False)
    imported_by = Column(Integer, nullable=True, index=True)
    total_rows = Column(Integer, nullable=False, default=0)
    inserted_rows = Column(Integer, nullable=False, default=0)
    updated_rows = Column(Integer, nullable=False, default=0)
    skipped_rows = Column(Integer, nullable=False, default=0)
    failed_rows = Column(Integer, nullable=False, default=0)
    status = Column(String(30), nullable=False, default="COMPLETED")
    report = Column(Text, nullable=True)
