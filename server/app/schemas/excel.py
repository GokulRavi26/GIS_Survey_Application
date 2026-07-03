from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ImportReport(BaseModel):
    total_rows: int
    inserted_rows: int
    updated_rows: int
    skipped_rows: int
    failed_rows: int
    errors: list[str]


class ImportHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_name: str
    imported_by: int | None
    total_rows: int
    inserted_rows: int
    updated_rows: int
    skipped_rows: int
    failed_rows: int
    status: str
    report: str | None
    created_at: datetime
    updated_at: datetime
