from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_database, require_roles
from app.models.user import User
from app.schemas.report import ReportsResponse
from app.services.report_service import ReportService
from app.utils.response import ApiResponse, success_response

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("", response_model=ApiResponse[ReportsResponse])
def get_reports(
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR")),
):
    reports = ReportService.get_reports(db)
    return success_response("Reports loaded successfully.", reports)
