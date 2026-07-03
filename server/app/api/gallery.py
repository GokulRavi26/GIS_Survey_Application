"""Gallery API endpoints (stubs)."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/gallery")
def list_gallery():
    return []
