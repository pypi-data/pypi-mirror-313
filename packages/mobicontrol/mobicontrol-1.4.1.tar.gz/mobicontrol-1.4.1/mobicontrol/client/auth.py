import requests
from mobicontrol.client import MobicontrolClient


def authenticate(
    client: MobicontrolClient,
    client_id: str,
    client_secret: str,
    username: str,
    password: str,
) -> None:
    auth = requests.models.HTTPBasicAuth(client_id, client_secret)

    response = client.post(
        "/token",
        auth=auth,
        data={"grant_type": "password", "username": username, "password": password},
    )

    if response.status_code != 200:
        raise Exception("Could not authenticate")

    client.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
