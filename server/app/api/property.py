from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_database, require_roles
from app.models.user import User
from app.schemas.property import (
    PropertyCreate,
    PropertyResponse,
    PropertySearchResponse,
    PropertyUpdate,
)
from app.services.property_service import PropertyService
from app.utils.response import ApiResponse, success_response

router = APIRouter(prefix="/properties", tags=["Properties"])


@router.get("", response_model=ApiResponse[PropertySearchResponse])
def search_properties(
    assessment_number: str | None = None,
    owner_name: str | None = None,
    door_number: str | None = None,
    ward_name: str | None = None,
    street_name: str | None = None,
    survey_status: str | None = None,
    query: str | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR", "SURVEYOR")),
):
    result = PropertyService.search_properties(
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
    return success_response("Properties loaded successfully.", result)


@router.post(
    "",
    response_model=ApiResponse[PropertyResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_property(
    payload: PropertyCreate,
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR")),
):
    try:
        property_record = PropertyService.create_property(db, payload)
        return success_response("Property created successfully.", property_record)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{property_id}", response_model=ApiResponse[PropertyResponse])
def get_property(
    property_id: int,
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR", "SURVEYOR")),
):
    try:
        property_record = PropertyService.get_property(db, property_id)
        return success_response("Property loaded successfully.", property_record)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.put("/{property_id}", response_model=ApiResponse[PropertyResponse])
def update_property(
    property_id: int,
    payload: PropertyUpdate,
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR")),
):
    try:
        property_record = PropertyService.update_property(db, property_id, payload)
        return success_response("Property updated successfully.", property_record)
    except ValueError as exc:
        status_code = 404 if str(exc) == "Property not found." else 400
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc
