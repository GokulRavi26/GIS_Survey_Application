"""Floor API endpoints (stubs)."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/floors")
def list_floors():
    return []
