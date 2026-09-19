@'
import os
import json
import base64

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = [
    "https://www.googleapis.com/auth/drive"
]

FOLDER_ID = os.environ["GOOGLE_DRIVE_FOLDER_ID"]


def get_drive_service():
    client_json_b64 = os.environ[
        "GOOGLE_OAUTH_CLIENT_JSON_B64"
    ]

    refresh_token = os.environ[
        "GOOGLE_REFRESH_TOKEN"
    ]

    client_json = json.loads(
        base64.b64decode(client_json_b64).decode("utf-8")
    )

    if "installed" in client_json:
        client_config = client_json["installed"]
    elif "web" in client_json:
        client_config = client_json["web"]
    else:
        raise RuntimeError(
            "Unsupported Google OAuth client configuration."
        )

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri=client_config["token_uri"],
        client_id=client_config["client_id"],
        client_secret=client_config["client_secret"],
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
        f.write(
            "Google Drive OAuth connection test\n"
        )

    metadata = {
        "name": "google-drive-test.txt",
        "parents": [FOLDER_ID],
    }

    media = MediaFileUpload(
        test_file,
        mimetype="text/plain",
        resumable=True,
    )

    result = service.files().create(
        body=metadata,
        media_body=media,
        fields="id,name",
    ).execute()

    print(
        f"Uploaded successfully: {result['name']}"
    )
    print(
        f"File ID: {result['id']}"
    )


if __name__ == "__main__":
    main()
'@ | Set-Content -Path ".\scripts\backup.py" -Encoding UTF8