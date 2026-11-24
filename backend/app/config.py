import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = "RateGuard"
    PROJECT_VERSION = "1.0.0"
    PROJECT_DESCRIPTION = "MongoDB-Powered API Rate Limiting System"

    MONGODB_URI = os.getenv(
        "MONGODB_URI",
        "mongodb://127.0.0.1:27017/"
    )

    DATABASE_NAME = os.getenv(
        "DATABASE_NAME",
        "rateguard_db"
    )

    DEFAULT_RATE_LIMIT = int(
        os.getenv("DEFAULT_RATE_LIMIT", "10")
    )

    DEFAULT_WINDOW_SECONDS = int(
        os.getenv("DEFAULT_WINDOW_SECONDS", "60")
    )


settings = Settings()