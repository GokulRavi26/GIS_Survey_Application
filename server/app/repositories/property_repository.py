from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.property import Property


class PropertyRepository:
    @staticmethod
    def get_by_id(db: Session, property_id: int) -> Property | None:
        return db.query(Property).filter(Property.id == property_id).first()

    @staticmethod
    def get_by_assessment_number(
        db: Session,
        assessment_number: str,
    ) -> Property | None:
        return (
            db.query(Property)
            .filter(Property.assessment_number == assessment_number)
            .first()
        )

    @staticmethod
    def search(
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
    ) -> tuple[list[Property], int]:
        statement = db.query(Property)

        if assessment_number:
            statement = statement.filter(
                Property.assessment_number.ilike(f"%{assessment_number}%")
            )
        if owner_name:
            statement = statement.filter(Property.owner_name.ilike(f"%{owner_name}%"))
        if door_number:
            statement = statement.filter(Property.door_number.ilike(f"%{door_number}%"))
        if ward_name:
            statement = statement.filter(Property.ward_name.ilike(f"%{ward_name}%"))
        if street_name:
            statement = statement.filter(Property.street_name.ilike(f"%{street_name}%"))
        if survey_status:
            statement = statement.filter(Property.survey_status == survey_status)
        if query:
            value = f"%{query}%"
            statement = statement.filter(
                or_(
                    Property.assessment_number.ilike(value),
                    Property.owner_name.ilike(value),
                    Property.door_number.ilike(value),
                    Property.ward_name.ilike(value),
                    Property.street_name.ilike(value),
                )
            )

        total = statement.count()
        rows = (
            statement.order_by(Property.assessment_number.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return rows, total

    @staticmethod
    def create(db: Session, property_record: Property) -> Property:
        db.add(property_record)
        db.commit()
        db.refresh(property_record)
        return property_record

    @staticmethod
    def update(db: Session, property_record: Property) -> Property:
        db.commit()
        db.refresh(property_record)
        return property_record

    @staticmethod
    def set_status(
        db: Session,
        property_record: Property,
        survey_status: str,
    ) -> Property:
        property_record.survey_status = survey_status
        db.commit()
        db.refresh(property_record)
        return property_record
