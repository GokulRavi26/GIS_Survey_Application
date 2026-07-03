from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_mobile(db: Session, mobile: str):

    return db.query(User).filter(
        User.mobile_number == mobile
    ).first()


def create_user(db: Session, user):

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def get_all_users(db: Session):

    return db.query(User).all()