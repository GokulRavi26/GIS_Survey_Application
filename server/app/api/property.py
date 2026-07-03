"""Property API endpoints (stubs)."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/properties")
def list_properties():
    return []
