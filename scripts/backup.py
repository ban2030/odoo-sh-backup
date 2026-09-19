import os
import json
import base64

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]


def load_client_json():
    value = os.environ.get("GOOGLE_OAUTH_CLIENT_JSON_B64", "").strip()

    if not value:
        raise RuntimeError(
            "GOOGLE_OAUTH_CLIENT_JSON_B64 is missing or empty."
        )

    try:
        decoded = base64.b64decode(value).decode("utf-8")
        data = json.loads(decoded)
    except Exception:
        try:
            data = json.loads(value)
        except Exception as exc:
            raise RuntimeError(
                "GOOGLE_OAUTH_CLIENT_JSON_B64 is not valid OAuth JSON."
            ) from exc

    if "installed" in data:
        return data["installed"]

    if "web" in data:
        return data["web"]

    raise RuntimeError(
        "Google OAuth client JSON does not contain "
        "either 'installed' or 'web' section."
    )


def get_drive_service():
    client_config = load_client_json()

    refresh_token = os.environ.get(
        "GOOGLE_REFRESH_TOKEN",
        "",
    ).strip()

    if not refresh_token:
        raise RuntimeError(
            "GOOGLE_REFRESH_TOKEN is missing or empty."
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

    folder_id = os.environ.get(
        "GOOGLE_DRIVE_FOLDER_ID",
        "",
    ).strip()

    if not folder_id:
        raise RuntimeError(
            "GOOGLE_DRIVE_FOLDER_ID is missing or empty."
        )

    os.makedirs("test", exist_ok=True)

    test_file = "test/google-drive-test.txt"

    with open(test_file, "w", encoding="utf-8") as f:
        f.write(
            "Google Drive OAuth connection test\n"
        )

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

    print(
        f"Uploaded successfully: {result['name']}"
    )
    print(
        f"File ID: {result['id']}"
    )


if __name__ == "__main__":
    main()
