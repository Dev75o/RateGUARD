
from fastapi import APIRouter, Depends

from ..dependencies import get_current_api_key
from ..database import get_database
from ..services.analytics_service import get_client_analytics

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/me")
def get_my_analytics(
    api_key_record: dict = Depends(get_current_api_key),
    db=Depends(get_database)
):
    analytics = get_client_analytics(
        db=db,
        client_id=api_key_record["client_id"]
    )

    return {
        "client_id": api_key_record["client_id"],
        "analytics": analytics
    }
