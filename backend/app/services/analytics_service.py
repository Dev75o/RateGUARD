
def get_client_analytics(db, client_id: str):
    """
    Retrieve request analytics for a specific client.
    """

    # Fetch all request logs belonging to this client
    logs = db.request_logs.find(
        {"client_id": client_id},
        {"_id": 0, "allowed": 1}
    )

    total_requests = 0
    allowed_requests = 0
    blocked_requests = 0

    for log in logs:
        total_requests += 1

        if log.get("allowed") is True:
            allowed_requests += 1
        else:
            blocked_requests += 1

    return {
        "total_requests": total_requests,
        "allowed_requests": allowed_requests,
        "blocked_requests": blocked_requests
    }
