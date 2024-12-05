import requests
from typing import Union
import os
import json


class NotLoggedIn(Exception):
    pass


class ConfigurationError(Exception):
    pass


WORKDIR = os.path.expanduser("~/.mobicontrol")


class MobicontrolClient(requests.Session):
    def __init__(
        self, base_url: str, headers: Union[dict, None] = None, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.base_url = base_url

        if headers is not None:
            self.headers = headers

    def request(
        self, method: Union[str, bytes], url: Union[str, bytes], *args, **kwargs
    ) -> requests.Response:

        if self.base_url not in url:
            url = f"{self.base_url}/MobiControl/api{str(url)}"

        return super().request(method, url, *args, **kwargs)

    def to_json(self) -> dict:
        return {"base_url": self.base_url, "headers": dict(self.headers)}

    def save(self) -> None:
        with open(f"{WORKDIR}/store.json", "w") as file:
            file.write(json.dumps(self.to_json()))

    @classmethod
    def load(cls) -> "MobicontrolClient":
        if not os.path.exists(WORKDIR):
            os.makedirs(WORKDIR)

        if not os.path.exists(f"{WORKDIR}/store.json"):
            with open(f"{WORKDIR}/store.json", "x") as file:
                file.write(json.dumps({"base_url": None, "headers": {}}))

        try:
            with open(f"{WORKDIR}/store.json", "r") as file:
                state = json.loads(file.read())

                return cls(**state)
        except Exception:
            raise ConfigurationError("Could not load configuration")
