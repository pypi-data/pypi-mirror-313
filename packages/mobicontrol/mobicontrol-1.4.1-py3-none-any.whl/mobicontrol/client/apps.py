from mobicontrol.client import MobicontrolClient
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import json

BOUNDARY = "mc_boundary"


def get_app(client: MobicontrolClient, app_id: str):
    response = client.get(f"/appManagement/android/apps//enterprise/{app_id}")

    if response.status_code != 200:
        raise Exception(f"Could not fetch app. Error code: {response.status_code}. {response.text}")

    return response.json()


def upload_app(client: MobicontrolClient, filename: str, file: bytes):
    message = MIMEMultipart("related", charset="utf-8")
    message.add_header("Content-Disposition", f"attachment; filename={filename}")

    # add metadata
    metadata = MIMEBase("application", "vnd.android.application.metadata+json")
    metadata.set_payload(json.dumps({"DeviceFamily": "AndroidPlus"}))
    del metadata["mime-version"]
    message.attach(metadata)

    # add file base 64 encoded
    binary_file = MIMEBase("application", "vnd.android.application")
    binary_file["Content-Type-Encoding"] = "base64"
    binary_file["Content-Disposition"] = f'attachment; filename="{filename}"'
    binary_file.set_payload(file)
    del binary_file["mime-version"]

    message.attach(binary_file)

    body = message.as_string().split("\n\n", 1)[1]
    body = body.replace("\n", "\r\n")

    headers = dict(message.items())

    response = client.post(
        "/appManagement/android/apps/enterprise/internal",
        headers={"Content-Type": headers["Content-Type"]},
        data=body.encode("utf-8"),
    )

    if response.status_code != 200:
        raise Exception(f"Upload failed with status code {response.status_code}. {response.text}.")

    data = response.json()

    if "ErrorCode" in data:
        raise Exception(f"Upload failed with message: {data['Message']}")

    return data
