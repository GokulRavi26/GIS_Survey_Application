from fastapi import APIRouter, status

from app.core.config import settings
from app.database.database import check_database_connection
from app.schemas.health import HealthResponse
from app.utils.response import ApiResponse
from app.utils.response import success_response

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=ApiResponse[HealthResponse],
    status_code=status.HTTP_200_OK,
    summary="Check API and database health.",
)
def health_check() -> ApiResponse[HealthResponse]:
    database_connected = check_database_connection()
    return success_response(
        message="Health check completed.",
        data=HealthResponse(
            status="healthy" if database_connected else "degraded",
            application=settings.APP_NAME,
            version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT,
            database="connected" if database_connected else "disconnected",
        ),
    )
