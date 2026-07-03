from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_database, require_roles
from app.models.user import User
from app.schemas.excel import ImportHistoryResponse, ImportReport
from app.services.excel_service import ExcelService
from app.utils.response import ApiResponse, success_response

router = APIRouter(prefix="/excel", tags=["Excel"])


@router.post("/import", response_model=ApiResponse[ImportReport])
def import_excel(
    file: UploadFile = File(...),
    update_existing: bool = True,
    db: Session = Depends(get_database),
    current_user: User = Depends(require_roles("ADMIN")),
):
    try:
        report = ExcelService.import_properties(
            db=db,
            file=file,
            current_user=current_user,
            update_existing=update_existing,
        )
        return success_response("Excel import completed.", report)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/export")
def export_excel(
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR")),
):
    output_path = ExcelService.export_properties(db)
    return FileResponse(
        path=output_path,
        filename=output_path.name,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )


@router.get("/history", response_model=ApiResponse[list[ImportHistoryResponse]])
def import_history(
    db: Session = Depends(get_database),
    _: User = Depends(require_roles("ADMIN", "SUPERVISOR")),
):
    history = ExcelService.list_import_history(db)
    return success_response("Import history loaded successfully.", history)
