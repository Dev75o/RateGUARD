
from fastapi import APIRouter, HTTPException, status

from ..database import get_database

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health_check():
    try:
        db = get_database()
        db.command("ping")

        return {
            "status": "healthy",
            "application": "RateGuard",
            "database": "connected"
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "application": "RateGuard",
                "database": "disconnected"
            }
        )
