import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = [
    "https://www.googleapis.com/auth/drive"
]

FOLDER_ID = os.environ["GOOGLE_DRIVE_FOLDER_ID"]

SERVICE_ACCOUNT_JSON = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]


def get_drive_service():
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(SERVICE_ACCOUNT_JSON),
        scopes=SCOPES,
    )

    return build(
        "drive",
        "v3",
        credentials=credentials,
    )


def main():
    service = get_drive_service()

    os.makedirs("test", exist_ok=True)

    test_file = "test/google-drive-test.txt"

    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Google Drive connection test\n")

    metadata = {
        "name": "google-drive-test.txt",
        "parents": [FOLDER_ID],
    }

    media = MediaFileUpload(
        test_file,
        mimetype="text/plain",
    )

    result = service.files().create(
        body=metadata,
        media_body=media,
        fields="id,name",
    ).execute()

    print(f"Uploaded successfully: {result['name']}")
    print(f"File ID: {result['id']}")


if __name__ == "__main__":
    main()
