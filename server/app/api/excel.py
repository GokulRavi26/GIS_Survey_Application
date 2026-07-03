"""Excel export/import API endpoints (stubs)."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/excel")
def excel_health():
    return {"excel": "ready"}
