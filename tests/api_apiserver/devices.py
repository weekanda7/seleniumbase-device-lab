import requests

from api_apiserver.auth import Auth
from config import Config


class DeviceApi:
    """Thin wrapper over /api/devices. Returns the raw Response so API tests can assert status codes."""

    def __init__(self, auth: Auth):
        self.session = auth.request
        self.url = f"{Config.API_URL}/devices"
        self.created_ids: list[
            int
        ] = []  # filled by tests, emptied by the `api` fixture

    def create(
        self,
        name: str,
        type: str = "Router",
        status: str = "online",
        location: str = "",
    ) -> requests.Response:
        body = {"name": name, "type": type, "status": status, "location": location}
        return self.session.post(self.url, json=body)

    def get(self, device_id: int) -> requests.Response:
        return self.session.get(f"{self.url}/{device_id}")

    def list(
        self, q: str | None = None, status: str | None = None
    ) -> requests.Response:
        params = {k: v for k, v in {"q": q, "status": status}.items() if v is not None}
        return self.session.get(self.url, params=params)

    def delete(self, device_id: int) -> requests.Response:
        return self.session.delete(f"{self.url}/{device_id}")
