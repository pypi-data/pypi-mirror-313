import logging

from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

SCOPES = ["https://www.googleapis.com/auth/drive"]
DEFAULT_SECRETS_PATH = "/etc/google/secrets.json"

logger = logging.getLogger(__name__)


class GoogleDriveClient:
    def __init__(self, secrets_path: str = DEFAULT_SECRETS_PATH):
        gauth = GoogleAuth()

        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            filename=secrets_path,
            scopes=SCOPES,
        )

        self.drive: GoogleDrive = GoogleDrive(gauth)

    @staticmethod
    def from_google_secrets_json(google_secrets_json: str) -> "GoogleDriveClient":
        secrets_path = "/tmp/secrets.json"

        with open(secrets_path, "w") as f:
            f.write(google_secrets_json)

        return GoogleDriveClient(
            secrets_path=secrets_path,
        )

    def download(self, file_id: str, path: str) -> None:
        file = self.drive.CreateFile({"id": file_id})
        file.GetContentFile(path)

        logger.info(f"Downloaded file {file_id} to {path}")
