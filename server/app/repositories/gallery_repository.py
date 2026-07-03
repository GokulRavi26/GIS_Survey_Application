from sqlalchemy.orm import Session

from app.models.gallery import Gallery


class GalleryRepository:
    @staticmethod
    def get_by_id(db: Session, image_id: int) -> Gallery | None:
        return db.query(Gallery).filter(Gallery.id == image_id).first()

    @staticmethod
    def list_by_survey(db: Session, survey_id: int) -> list[Gallery]:
        return (
            db.query(Gallery)
            .filter(Gallery.survey_id == survey_id)
            .order_by(Gallery.created_at.desc())
            .all()
        )

    @staticmethod
    def create(db: Session, gallery: Gallery) -> Gallery:
        db.add(gallery)
        db.commit()
        db.refresh(gallery)
        return gallery

    @staticmethod
    def delete(db: Session, gallery: Gallery) -> None:
        db.delete(gallery)
        db.commit()
