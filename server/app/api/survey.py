"""Survey API endpoints (stubs)."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/surveys")
def list_surveys():
    return []
