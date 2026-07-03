from sqlalchemy.orm import Session

from app.models.import_history import ImportHistory


class ImportHistoryRepository:
    @staticmethod
    def create(db: Session, import_history: ImportHistory) -> ImportHistory:
        db.add(import_history)
        db.commit()
        db.refresh(import_history)
        return import_history

    @staticmethod
    def list_recent(db: Session, limit: int = 25) -> list[ImportHistory]:
        return (
            db.query(ImportHistory)
            .order_by(ImportHistory.created_at.desc())
            .limit(limit)
            .all()
        )
