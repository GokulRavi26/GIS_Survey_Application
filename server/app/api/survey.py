from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_database, require_roles
from app.models.user import User
from app.schemas.survey import SurveyCreate, SurveyListResponse, SurveyResponse, SurveyUpdate
from app.services.survey_service import SurveyService
from app.utils.response import ApiResponse, success_response

router = APIRouter(prefix="/surveys", tags=["Surveys"])


@router.get("", response_model=ApiResponse[SurveyListResponse])
def list_surveys(
    property_id: int | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR", "SURVEYOR")),
):
    result = SurveyService.list_surveys(db, property_id, offset, limit)
    return success_response("Surveys loaded successfully.", result)


@router.post(
    "",
    response_model=ApiResponse[SurveyResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_survey(
    payload: SurveyCreate,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_roles("ADMIN", "SUPERVISOR", "SURVEYOR")),
):
    try:
        survey = SurveyService.create_survey(db, payload, current_user)
        return success_response("Survey submitted successfully.", survey)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{survey_id}", response_model=ApiResponse[SurveyResponse])
def get_survey(
    survey_id: int,
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR", "SURVEYOR")),
):
    try:
        survey = SurveyService.get_survey(db, survey_id)
        return success_response("Survey loaded successfully.", survey)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.put("/{survey_id}", response_model=ApiResponse[SurveyResponse])
def update_survey(
    survey_id: int,
    payload: SurveyUpdate,
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR", "SURVEYOR")),
):
    try:
        survey = SurveyService.update_survey(db, survey_id, payload)
        return success_response("Survey updated successfully.", survey)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
