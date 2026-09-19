import os
import json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]


def get_drive_service():
    client_json = json.loads(os.environ["GOOGLE_OAUTH_CLIENT_JSON_B64"])

    credentials = Credentials(
        token=None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        token_uri=client_json["web"]["token_uri"],
        client_id=client_json["web"]["client_id"],
        client_secret=client_json["web"]["client_secret"],
        scopes=SCOPES,
    )

    return build(
        "drive",
        "v3",
        credentials=credentials,
    )


def main():
    service = get_drive_service()

    folder_id = os.environ["GOOGLE_DRIVE_FOLDER_ID"]

    os.makedirs("test", exist_ok=True)

    test_file = "test/google-drive-test.txt"

    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Google Drive connection test\n")

    metadata = {
        "name": "google-drive-test.txt",
        "parents": [folder_id],
    }

    media = MediaFileUpload(
        test_file,
        mimetype="text/plain",
        resumable=True,
    )

    result = (
        service.files()
        .create(
            body=metadata,
            media_body=media,
            fields="id,name",
        )
        .execute()
    )

    print(f"Uploaded successfully: {result['name']}")
    print(f"File ID: {result['id']}")


if __name__ == "__main__":
    main()
