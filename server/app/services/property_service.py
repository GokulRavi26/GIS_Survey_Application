from sqlalchemy.orm import Session

from app.models.property import Property
from app.repositories.property_repository import PropertyRepository
from app.schemas.property import PropertyCreate, PropertySearchResponse, PropertyUpdate


class PropertyService:
    @staticmethod
    def search_properties(
        db: Session,
        assessment_number: str | None = None,
        owner_name: str | None = None,
        door_number: str | None = None,
        ward_name: str | None = None,
        street_name: str | None = None,
        survey_status: str | None = None,
        query: str | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> PropertySearchResponse:
        rows, total = PropertyRepository.search(
            db=db,
            assessment_number=assessment_number,
            owner_name=owner_name,
            door_number=door_number,
            ward_name=ward_name,
            street_name=street_name,
            survey_status=survey_status,
            query=query,
            offset=offset,
            limit=limit,
        )
        return PropertySearchResponse(
            items=rows,
            total=total,
            offset=offset,
            limit=limit,
        )

    @staticmethod
    def get_property(db: Session, property_id: int) -> Property:
        property_record = PropertyRepository.get_by_id(db, property_id)
        if property_record is None:
            raise ValueError("Property not found.")
        return property_record

    @staticmethod
    def create_property(db: Session, payload: PropertyCreate) -> Property:
        existing = PropertyRepository.get_by_assessment_number(
            db,
            payload.assessment_number,
        )
        if existing is not None:
            raise ValueError("A property with this assessment number already exists.")

        property_record = Property(**payload.model_dump())
        return PropertyRepository.create(db, property_record)

    @staticmethod
    def update_property(
        db: Session,
        property_id: int,
        payload: PropertyUpdate,
    ) -> Property:
        property_record = PropertyService.get_property(db, property_id)
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No property fields were provided for update.")

        for field, value in update_data.items():
            if isinstance(value, str):
                value = value.strip()
            setattr(property_record, field, value)

        return PropertyRepository.update(db, property_record)
