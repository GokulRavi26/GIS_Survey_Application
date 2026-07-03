from sqlalchemy.orm import Session

from app.models.floor import Floor


class FloorRepository:
    @staticmethod
    def get_by_id(db: Session, floor_id: int) -> Floor | None:
        return db.query(Floor).filter(Floor.id == floor_id).first()

    @staticmethod
    def list_by_survey(db: Session, survey_id: int) -> list[Floor]:
        return (
            db.query(Floor)
            .filter(Floor.survey_id == survey_id)
            .order_by(Floor.id.asc())
            .all()
        )

    @staticmethod
    def create(db: Session, floor: Floor) -> Floor:
        db.add(floor)
        db.commit()
        db.refresh(floor)
        return floor

    @staticmethod
    def delete_by_survey(db: Session, survey_id: int) -> None:
        db.query(Floor).filter(Floor.survey_id == survey_id).delete()
        db.commit()

    @staticmethod
    def delete(db: Session, floor: Floor) -> None:
        db.delete(floor)
        db.commit()
