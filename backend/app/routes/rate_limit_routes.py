
from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_current_api_key
from ..database import get_database
from ..services.rate_limiter import check_rate_limit

router = APIRouter(
    prefix="/rate-limit",
    tags=["Rate Limiting"]
)


@router.post("/check")
def check_request(
    api_key_record: dict = Depends(get_current_api_key),
    db=Depends(get_database)
):
    result = check_rate_limit(
        db=db,
        client_id=api_key_record["client_id"]
    )

    headers = {
        "X-RateLimit-Limit": str(result["limit"]),
        "X-RateLimit-Remaining": str(result["remaining"]),
        "X-RateLimit-Reset": str(result["reset_at"])
    }

    if not result["allowed"]:
        headers["Retry-After"] = str(result["retry_after"])

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=result,
            headers=headers
        )

    return result
