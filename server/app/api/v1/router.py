from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.excel import router as excel_router
from app.api.floor import router as floor_router
from app.api.gallery import router as gallery_router
from app.api.property import router as property_router
from app.api.reports import router as reports_router
from app.api.survey import router as survey_router
from app.api.users import router as users_router
from app.api.v1.health import router as health_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(excel_router)
api_router.include_router(property_router)
api_router.include_router(survey_router)
api_router.include_router(floor_router)
api_router.include_router(gallery_router)
api_router.include_router(reports_router)
api_router.include_router(health_router)
