from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.audit_repository import AuditRepository


class AuditService:
    @staticmethod
    def record_user_action(
        db: Session,
        actor: User | None,
        action: str,
        description: str,
    ) -> None:
        actor_label = "SYSTEM"
        if actor is not None:
            actor_label = (
                f"{actor.full_name} "
                f"({actor.mobile_number}, {actor.role})"
            )

        AuditRepository.create(
            db=db,
            user=actor_label,
            action=action,
            description=description,
        )
