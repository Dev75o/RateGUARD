from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from .config import settings


client = None
database = None


def connect_to_mongodb():
    global client, database

    try:
        client = MongoClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000
        )

        # Verify that MongoDB is reachable
        client.admin.command("ping")

        database = client[settings.DATABASE_NAME]

        # Create indexes for efficient database operations
        database.rate_limits.create_index(
            "client_id",
            unique=True
        )

        database.api_keys.create_index(
            "key_hash",
            unique=True
        )

        database.request_logs.create_index(
            "timestamp"
        )

        print("Successfully connected to MongoDB.")

    except ServerSelectionTimeoutError as error:
        client = None
        database = None
        raise RuntimeError(
            "Could not connect to MongoDB. "
            "Check whether MongoDB is running."
        ) from error


def get_database():
    if database is None:
        raise RuntimeError("Database connection is not initialized.")

    return database


def close_mongodb_connection():
    global client, database

    if client is not None:
        client.close()
        client = None
        database = None

        print("MongoDB connection closed.")