from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_database, require_roles
from app.models.user import User
from app.schemas.gallery import GalleryResponse
from app.services.gallery_service import GalleryService
from app.utils.response import ApiResponse, success_response

router = APIRouter(prefix="/gallery", tags=["Gallery"])


@router.get("/survey/{survey_id}", response_model=ApiResponse[list[GalleryResponse]])
def list_images(
    survey_id: int,
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR", "SURVEYOR")),
):
    try:
        images = GalleryService.list_images(db, survey_id)
        return success_response("Gallery loaded successfully.", images)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post(
    "/survey/{survey_id}",
    response_model=ApiResponse[GalleryResponse],
    status_code=status.HTTP_201_CREATED,
)
def upload_image(
    survey_id: int,
    image_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR", "SURVEYOR")),
):
    try:
        image = GalleryService.upload_image(db, survey_id, image_type, file)
        return success_response("Image uploaded successfully.", image)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/{image_id}", response_model=ApiResponse[None])
def delete_image(
    image_id: int,
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR", "SURVEYOR")),
):
    try:
        GalleryService.delete_image(db, image_id)
        return success_response("Image deleted successfully.")
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
