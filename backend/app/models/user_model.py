
import hashlib
from datetime import datetime, timezone


def create_api_key_document(
    client_id: str,
    api_key: str,
    client_name: str
):
    """
    Create an API-key document for a RateGuard client.
    """

    key_hash = hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()

    return {
        "client_id": client_id,
        "client_name": client_name,
        "key_hash": key_hash,
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    }
