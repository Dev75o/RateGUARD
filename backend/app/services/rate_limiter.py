
import time

from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from ..config import settings


def check_rate_limit(
    db,
    client_id: str,
    limit: int | None = None,
    window_seconds: int | None = None
):
    """
    Check whether a client is allowed to make an API request.

    Algorithm: Fixed Window Counter
    Storage: MongoDB
    Updates: Atomic MongoDB update pipeline
    """

    # Use configured defaults if custom values are not supplied
    limit = limit or settings.DEFAULT_RATE_LIMIT
    window_seconds = window_seconds or settings.DEFAULT_WINDOW_SECONDS

    if not client_id:
        raise ValueError("client_id cannot be empty.")

    if limit <= 0 or window_seconds <= 0:
        raise ValueError("Limit and window duration must be positive.")

    # Calculate the current fixed time window
    current_time = int(time.time())

    current_window_start = (
        current_time // window_seconds
    ) * window_seconds

    # Atomic update: reset expired counters or increment active ones
    update_pipeline = [
        {
            "$set": {
                "window_start": {
                    "$cond": [
                        {
                            "$lt": [
                                {"$ifNull": ["$window_start", 0]},
                                current_window_start
                            ]
                        },
                        current_window_start,
                        {"$ifNull": ["$window_start", current_window_start]}
                    ]
                },

                "count": {
                    "$cond": [
                        {
                            "$lt": [
                                {"$ifNull": ["$window_start", 0]},
                                current_window_start
                            ]
                        },
                        1,
                        {
                            "$cond": [
                                {
                                    "$eq": [
                                        "$window_start",
                                        current_window_start
                                    ]
                                },
                                {"$add": ["$count", 1]},
                                {"$ifNull": ["$count", 0]}
                            ]
                        }
                    ]
                },

                "updated_at": current_time
            }
        }
    ]

    collection = db.rate_limits

    try:
        record = collection.find_one_and_update(
            {"client_id": client_id},
            update_pipeline,
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

    except DuplicateKeyError:
        # Another request may have created the client's record
        # at the same time. Retry without upsert.
        record = collection.find_one_and_update(
            {"client_id": client_id},
            update_pipeline,
            upsert=False,
            return_document=ReturnDocument.AFTER
        )

        if record is None:
            raise RuntimeError(
                "Could not update the client's rate-limit record."
            )

    # Read the updated counter
    request_count = record["count"]

    window_end = record["window_start"] + window_seconds

    # Determine whether the request is permitted
    allowed = request_count <= limit

    remaining = max(0, limit - request_count)

    retry_after = (
        max(1, window_end - current_time)
        if not allowed
        else 0
    )


    result = {
        "client_id": client_id,
        "allowed": allowed,
        "algorithm": "Fixed Window Counter",
        "limit": limit,
        "window_seconds": window_seconds,
        "current_count": request_count,
        "remaining": remaining,
        "window_start": record["window_start"],
        "reset_at": window_end,
        "retry_after": retry_after
    }

    # Save every request attempt for analytics
    db.request_logs.insert_one({
        "client_id": client_id,
        "allowed": allowed,
        "timestamp": current_time
    })

    return result


