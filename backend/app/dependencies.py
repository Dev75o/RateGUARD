
import hashlib

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from .database import get_database


api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)


def get_db():
    return get_database()


def get_current_api_key(
    api_key: str = Depends(api_key_header),
    db=Depends(get_db)
):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required."
        )

    key_hash = hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()

    api_key_record = db.api_keys.find_one({
        "key_hash": key_hash,
        "is_active": True
    })

    if not api_key_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key."
        )

    return api_key_record
