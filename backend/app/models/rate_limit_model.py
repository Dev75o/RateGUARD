
from datetime import datetime, timezone


def create_rate_limit_document(
    client_id: str,
    count: int = 0,
    window_start: int = 0
):
    """
    Create a MongoDB rate-limit document.
    """

    return {
        "client_id": client_id,
        "count": count,
        "window_start": window_start,
        "updated_at": int(
            datetime.now(timezone.utc).timestamp()
        )
    }
