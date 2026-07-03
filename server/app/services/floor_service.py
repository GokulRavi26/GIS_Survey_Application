from sqlalchemy.orm import Session

from app.models.floor import Floor
from app.repositories.floor_repository import FloorRepository
from app.repositories.survey_repository import SurveyRepository
from app.schemas.floor import FloorCreate


class FloorService:
    @staticmethod
    def list_floors(db: Session, survey_id: int) -> list[Floor]:
        survey = SurveyRepository.get_by_id(db, survey_id)
        if survey is None:
            raise ValueError("Survey not found.")
        return FloorRepository.list_by_survey(db, survey_id)

    @staticmethod
    def add_floor(db: Session, survey_id: int, payload: FloorCreate) -> Floor:
        survey = SurveyRepository.get_by_id(db, survey_id)
        if survey is None:
            raise ValueError("Survey not found.")
        return FloorRepository.create(
            db,
            Floor(survey_id=survey_id, **payload.model_dump()),
        )

    @staticmethod
    def delete_floor(db: Session, floor_id: int) -> None:
        floor = FloorRepository.get_by_id(db, floor_id)
        if floor is None:
            raise ValueError("Floor not found.")
        FloorRepository.delete(db, floor)
