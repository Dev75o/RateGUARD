
import secrets

from backend.app.config import settings
from backend.app.models.user_model import create_api_key_document
from pymongo import MongoClient


def main():
    client = MongoClient(
        settings.MONGODB_URI,
        serverSelectionTimeoutMS=5000
    )

    try:
        client.admin.command("ping")

        db = client[settings.DATABASE_NAME]

        api_key = secrets.token_urlsafe(32)

        api_key_document = create_api_key_document(
            client_id="demo-client",
            api_key=api_key,
            client_name="RateGuard Demo Client"
        )

        db.api_keys.insert_one(api_key_document)

        print("\nAPI KEY CREATED SUCCESSFULLY")
        print("--------------------------------")
        print("Client ID: demo-client")
        print("API Key:", api_key)
        print("--------------------------------")
        print("Save this key. It will not be stored in plaintext.")

    finally:
        client.close()


if __name__ == "__main__":
    main()
