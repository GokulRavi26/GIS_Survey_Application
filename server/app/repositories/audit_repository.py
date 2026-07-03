from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditRepository:
    @staticmethod
    def create(
        db: Session,
        user: str,
        action: str,
        description: str,
    ) -> AuditLog:
        audit_log = AuditLog(
            user=user,
            action=action,
            description=description,
        )
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        return audit_log
