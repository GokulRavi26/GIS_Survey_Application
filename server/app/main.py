from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.database.database import check_database_connection
from app.database.init_db import create_tables
from app.utils.response import error_response
from app.utils.response import success_response

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting GIS Survey Backend...")
    create_tables()
    logger.info("Database initialized successfully.")
    yield
    logger.info("Stopping GIS Survey Backend...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for the GIS Survey Application.",
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    content = error_response(
        message=str(exc.detail),
        errors=None,
    ).model_dump(mode="json")
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    content = error_response(
        message="Request validation failed.",
        errors=exc.errors(),
    ).model_dump(mode="json")
    return JSONResponse(
        status_code=422,
        content=content,
    )


def swagger_authorize_script() -> str:
    return """
    <script>
      (function () {
        function customizeAuthorizeModal() {
          const modal = document.querySelector(".dialog-ux");
          if (!modal) return;

          modal.querySelectorAll("label").forEach((label) => {
            const text = label.textContent.trim().toLowerCase();
            if (text.includes("username")) {
              label.childNodes.forEach((node) => {
                if (node.nodeType === Node.TEXT_NODE) {
                  node.textContent = node.textContent.replace(
                    /username/i,
                    "Mobile number"
                  );
                }
              });
            }

            if (text.includes("client_id") || text.includes("client_secret")) {
              const wrapper = label.closest(".wrapper") || label.parentElement;
              if (wrapper) wrapper.style.display = "none";
            }
          });

          modal.querySelectorAll("input").forEach((input) => {
            if (input.name === "username") {
              input.placeholder = "Mobile number";
              input.inputMode = "numeric";
              input.autocomplete = "username";
            }

            if (input.name === "client_id" || input.name === "client_secret") {
              const wrapper = input.closest(".wrapper") || input.parentElement;
              if (wrapper) wrapper.style.display = "none";
            }
          });
        }

        const observer = new MutationObserver(customizeAuthorizeModal);
        observer.observe(document.body, { childList: true, subtree: true });
        window.addEventListener("load", customizeAuthorizeModal);
      })();
    </script>
    """


@app.get("/docs", include_in_schema=False)
def swagger_ui_html() -> HTMLResponse:
    response = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{settings.APP_NAME} - Swagger UI",
    )
    html = response.body.decode("utf-8").replace(
        "</body>",
        f"{swagger_authorize_script()}</body>",
    )
    return HTMLResponse(html)


@app.get("/redoc", include_in_schema=False)
def redoc_html() -> HTMLResponse:
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{settings.APP_NAME} - ReDoc",
    )


@app.get("/")
def root():
    return success_response(
        message="GIS Survey Backend Running",
        data={"version": settings.APP_VERSION},
    )


@app.get("/health")
def health():
    database_connected = check_database_connection()
    return success_response(
        message="Health check completed.",
        data={
            "status": "healthy" if database_connected else "degraded",
            "database": "connected" if database_connected else "disconnected",
        },
    )
