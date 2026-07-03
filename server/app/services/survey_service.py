from sqlalchemy.orm import Session

from app.models.floor import Floor
from app.models.survey import Survey
from app.models.user import User
from app.repositories.floor_repository import FloorRepository
from app.repositories.gallery_repository import GalleryRepository
from app.repositories.property_repository import PropertyRepository
from app.repositories.survey_repository import SurveyRepository
from app.schemas.survey import SurveyCreate, SurveyListResponse, SurveyResponse, SurveyUpdate


class SurveyService:
    @staticmethod
    def list_surveys(
        db: Session,
        property_id: int | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> SurveyListResponse:
        if property_id is not None:
            rows = SurveyRepository.list_by_property(db, property_id)
            total = len(rows)
            rows = rows[offset : offset + limit]
        else:
            rows, total = SurveyRepository.list_all(db, offset, limit)

        return SurveyListResponse(
            items=[SurveyService._build_response(db, row) for row in rows],
            total=total,
            offset=offset,
            limit=limit,
        )

    @staticmethod
    def get_survey(db: Session, survey_id: int) -> SurveyResponse:
        survey = SurveyRepository.get_by_id(db, survey_id)
        if survey is None:
            raise ValueError("Survey not found.")
        return SurveyService._build_response(db, survey)

    @staticmethod
    def create_survey(
        db: Session,
        payload: SurveyCreate,
        current_user: User,
    ) -> SurveyResponse:
        property_record = PropertyRepository.get_by_id(db, payload.property_id)
        if property_record is None:
            raise ValueError("Property not found.")

        survey = Survey(
            property_id=payload.property_id,
            latitude=payload.latitude,
            longitude=payload.longitude,
            remarks=payload.remarks,
            created_by=current_user.id,
        )
        created_survey = SurveyRepository.create(db, survey)

        for floor_payload in payload.floors:
            FloorRepository.create(
                db,
                Floor(
                    survey_id=created_survey.id,
                    **floor_payload.model_dump(),
                ),
            )

        PropertyRepository.set_status(db, property_record, "Completed")
        return SurveyService._build_response(db, created_survey)

    @staticmethod
    def update_survey(
        db: Session,
        survey_id: int,
        payload: SurveyUpdate,
    ) -> SurveyResponse:
        survey = SurveyRepository.get_by_id(db, survey_id)
        if survey is None:
            raise ValueError("Survey not found.")

        update_data = payload.model_dump(exclude_unset=True)
        floors = update_data.pop("floors", None)

        for field, value in update_data.items():
            setattr(survey, field, value)
        SurveyRepository.update(db, survey)

        if floors is not None:
            FloorRepository.delete_by_survey(db, survey.id)
            for floor_payload in floors:
                FloorRepository.create(
                    db,
                    Floor(
                        survey_id=survey.id,
                        **floor_payload.model_dump(),
                    ),
                )

        property_record = PropertyRepository.get_by_id(db, survey.property_id)
        if property_record is not None:
            PropertyRepository.set_status(db, property_record, "Completed")

        return SurveyService._build_response(db, survey)

    @staticmethod
    def _build_response(db: Session, survey: Survey) -> SurveyResponse:
        floors = FloorRepository.list_by_survey(db, survey.id)
        gallery = GalleryRepository.list_by_survey(db, survey.id)
        return SurveyResponse.model_validate(
            {
                "id": survey.id,
                "property_id": survey.property_id,
                "latitude": survey.latitude,
                "longitude": survey.longitude,
                "remarks": survey.remarks,
                "created_by": survey.created_by,
                "created_at": survey.created_at,
                "updated_at": survey.updated_at,
                "floors": floors,
                "gallery": gallery,
            }
        )
