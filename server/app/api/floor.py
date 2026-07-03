from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_database, require_roles
from app.models.user import User
from app.schemas.floor import FloorCreate, FloorResponse
from app.services.floor_service import FloorService
from app.utils.response import ApiResponse, success_response

router = APIRouter(prefix="/floors", tags=["Floors"])


@router.get("/survey/{survey_id}", response_model=ApiResponse[list[FloorResponse]])
def list_floors(
    survey_id: int,
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR", "SURVEYOR")),
):
    try:
        floors = FloorService.list_floors(db, survey_id)
        return success_response("Floors loaded successfully.", floors)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post(
    "/survey/{survey_id}",
    response_model=ApiResponse[FloorResponse],
    status_code=status.HTTP_201_CREATED,
)
def add_floor(
    survey_id: int,
    payload: FloorCreate,
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR", "SURVEYOR")),
):
    try:
        floor = FloorService.add_floor(db, survey_id, payload)
        return success_response("Floor added successfully.", floor)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/{floor_id}", response_model=ApiResponse[None])
def delete_floor(
    floor_id: int,
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR")),
):
    try:
        FloorService.delete_floor(db, floor_id)
        return success_response("Floor deleted successfully.")
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
