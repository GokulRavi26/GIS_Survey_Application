from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate
from app.core.security import hash_password
from app.core.security import validate_password
from app.services.audit_service import AuditService


class UserService:
    VALID_ROLES = {"ADMIN", "SUPERVISOR", "SURVEYOR"}

    @staticmethod
    def list_users(db: Session) -> list[User]:
        return UserRepository.get_all(db)

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        user = UserRepository.get_by_id(db, user_id)
        if user is None:
            raise ValueError("User not found.")
        return user

    @staticmethod
    def get_user_by_mobile(db: Session, mobile_number: str) -> User | None:
        return UserRepository.get_by_mobile(db, mobile_number)

    @staticmethod
    def create_user(
        db: Session,
        payload: UserCreate,
        actor: User | None = None,
    ) -> User:
        UserService._validate_role(payload.role)
        validate_password(payload.password)

        existing_user = UserRepository.get_by_mobile(
            db,
            payload.mobile_number,
        )
        if existing_user is not None:
            raise ValueError("A user with this mobile number already exists.")

        user = User(
            full_name=payload.full_name.strip(),
            mobile_number=payload.mobile_number,
            password=hash_password(payload.password),
            role=payload.role,
            is_active=True,
        )
        created_user = UserRepository.create(db, user)
        AuditService.record_user_action(
            db=db,
            actor=actor,
            action="USER_CREATED",
            description=(
                f"Created user {created_user.full_name} "
                f"({created_user.mobile_number}) with role "
                f"{created_user.role}."
            ),
        )
        return created_user

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        payload: UserUpdate,
        actor: User | None = None,
    ) -> User:
        user = UserService.get_user(db, user_id)
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No user fields were provided for update.")

        if "role" in update_data:
            UserService._validate_role(update_data["role"])

        if "mobile_number" in update_data:
            existing_user = UserRepository.get_by_mobile(
                db,
                update_data["mobile_number"],
            )
            if existing_user is not None and existing_user.id != user.id:
                raise ValueError(
                    "A user with this mobile number already exists."
                )

        changes: list[str] = []
        for field, value in update_data.items():
            if isinstance(value, str):
                value = value.strip()
            old_value = getattr(user, field)
            if old_value != value:
                changes.append(f"{field}: {old_value} -> {value}")
            setattr(user, field, value)

        updated_user = UserRepository.update(db, user)
        AuditService.record_user_action(
            db=db,
            actor=actor,
            action="USER_UPDATED",
            description=(
                f"Updated user {updated_user.full_name} "
                f"({updated_user.mobile_number}). Changes: "
                f"{'; '.join(changes) if changes else 'No value changes'}."
            ),
        )
        return updated_user

    @staticmethod
    def reset_password(
        db: Session,
        user_id: int,
        new_password: str,
        actor: User | None = None,
    ) -> User:
        validate_password(new_password)
        user = UserService.get_user(db, user_id)
        user.password = hash_password(new_password)
        updated_user = UserRepository.update(db, user)
        AuditService.record_user_action(
            db=db,
            actor=actor,
            action="USER_PASSWORD_RESET",
            description=(
                f"Reset password for user {updated_user.full_name} "
                f"({updated_user.mobile_number})."
            ),
        )
        return updated_user

    @staticmethod
    def activate_user(
        db: Session,
        user_id: int,
        actor: User | None = None,
    ) -> User:
        user = UserService.get_user(db, user_id)
        user.is_active = True
        updated_user = UserRepository.update(db, user)
        AuditService.record_user_action(
            db=db,
            actor=actor,
            action="USER_ACTIVATED",
            description=(
                f"Activated user {updated_user.full_name} "
                f"({updated_user.mobile_number})."
            ),
        )
        return updated_user

    @staticmethod
    def deactivate_user(
        db: Session,
        user_id: int,
        current_user_id: int,
        actor: User | None = None,
    ) -> User:
        if user_id == current_user_id:
            raise ValueError("Current admin user cannot be deactivated.")

        user = UserService.get_user(db, user_id)
        user.is_active = False
        updated_user = UserRepository.update(db, user)
        AuditService.record_user_action(
            db=db,
            actor=actor,
            action="USER_DEACTIVATED",
            description=(
                f"Deactivated user {updated_user.full_name} "
                f"({updated_user.mobile_number})."
            ),
        )
        return updated_user

    @staticmethod
    def delete_user(
        db: Session,
        user_id: int,
        current_user_id: int,
        actor: User | None = None,
    ) -> None:
        if user_id == current_user_id:
            raise ValueError("Current admin user cannot be deleted.")

        user = UserService.get_user(db, user_id)
        deleted_user_label = f"{user.full_name} ({user.mobile_number})"
        try:
            UserRepository.delete(db, user)
        except IntegrityError as exc:
            db.rollback()
            raise ValueError(
                "User cannot be deleted because related history exists. "
                "Deactivate the user instead."
            ) from exc
        AuditService.record_user_action(
            db=db,
            actor=actor,
            action="USER_DELETED",
            description=f"Deleted user {deleted_user_label}.",
        )

    @staticmethod
    def _validate_role(role: str) -> None:
        if role not in UserService.VALID_ROLES:
            raise ValueError("Invalid user role.")


def get_user_by_mobile(db, mobile: str) -> User | None:
    return UserService.get_user_by_mobile(db, mobile)
