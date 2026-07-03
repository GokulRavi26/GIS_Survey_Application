from sqlalchemy.orm import Session

from app.models.survey import Survey


class SurveyRepository:
    @staticmethod
    def get_by_id(db: Session, survey_id: int) -> Survey | None:
        return db.query(Survey).filter(Survey.id == survey_id).first()

    @staticmethod
    def list_by_property(db: Session, property_id: int) -> list[Survey]:
        return (
            db.query(Survey)
            .filter(Survey.property_id == property_id)
            .order_by(Survey.created_at.desc())
            .all()
        )

    @staticmethod
    def list_all(db: Session, offset: int = 0, limit: int = 50) -> tuple[list[Survey], int]:
        statement = db.query(Survey)
        total = statement.count()
        rows = statement.order_by(Survey.created_at.desc()).offset(offset).limit(limit).all()
        return rows, total

    @staticmethod
    def create(db: Session, survey: Survey) -> Survey:
        db.add(survey)
        db.commit()
        db.refresh(survey)
        return survey

    @staticmethod
    def update(db: Session, survey: Survey) -> Survey:
        db.commit()
        db.refresh(survey)
        return survey
