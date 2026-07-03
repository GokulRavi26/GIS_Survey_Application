from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import BASE_DIR
from app.models.gallery import Gallery
from app.repositories.gallery_repository import GalleryRepository
from app.repositories.survey_repository import SurveyRepository
from app.services.upload_service import UploadService


class GalleryService:
    @staticmethod
    def list_images(db: Session, survey_id: int) -> list[Gallery]:
        survey = SurveyRepository.get_by_id(db, survey_id)
        if survey is None:
            raise ValueError("Survey not found.")
        return GalleryRepository.list_by_survey(db, survey_id)

    @staticmethod
    def upload_image(
        db: Session,
        survey_id: int,
        image_type: str,
        file: UploadFile,
    ) -> Gallery:
        survey = SurveyRepository.get_by_id(db, survey_id)
        if survey is None:
            raise ValueError("Survey not found.")

        image_path = UploadService.save_image(file)
        gallery = Gallery(
            survey_id=survey_id,
            image_path=image_path,
            image_type=image_type.strip(),
        )
        return GalleryRepository.create(db, gallery)

    @staticmethod
    def delete_image(db: Session, image_id: int) -> None:
        gallery = GalleryRepository.get_by_id(db, image_id)
        if gallery is None:
            raise ValueError("Image not found.")

        stored_path = BASE_DIR / Path(gallery.image_path)
        if stored_path.exists() and stored_path.is_file():
            stored_path.unlink()

        GalleryRepository.delete(db, gallery)
