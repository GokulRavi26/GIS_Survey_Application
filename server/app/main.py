from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.auth import router as auth_router

from app.core.config import settings
from app.database.init_db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting GIS Survey Backend...")
    create_tables()
    print("Database initialized successfully.")
    yield
    print("Stopping GIS Survey Backend...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "GIS Survey Backend Running",
        "version": settings.APP_VERSION,
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy",
        "database": "Connected",
    }