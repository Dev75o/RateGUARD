from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings
from .database import (
    connect_to_mongodb,
    close_mongodb_connection
)

from .routes.rate_limit_routes import router as rate_limit_router
from .routes.analytics_routes import router as analytics_router
from .routes.health_routes import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup
    connect_to_mongodb()

    yield

    # Application shutdown
    close_mongodb_connection()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)


# Register API routes
app.include_router(rate_limit_router)
app.include_router(analytics_router)
app.include_router(health_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to RateGuard API",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "running"
    }