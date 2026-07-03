from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password
from app.core.config import settings


def create_default_admin(db: Session):

    # Check whether the admin already exists
    admin = (
        db.query(User)
        .filter(User.mobile_number == settings.DEFAULT_ADMIN_MOBILE)
        .first()
    )

    if admin:
        print("Default admin already exists.")
        return

    # Create default admin
    admin = User(
        full_name=settings.DEFAULT_ADMIN_NAME,
        mobile_number=settings.DEFAULT_ADMIN_MOBILE,
        password=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
        role=settings.DEFAULT_ADMIN_ROLE,
        is_active=True,
    )

    db.add(admin)
    db.commit()

    print("Default admin created successfully.")