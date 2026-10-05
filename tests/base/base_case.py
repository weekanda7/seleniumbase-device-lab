"""Shared test bases (D2 T1 decision).

- Plain method overriding (hooks), no abc / abstract / template method: only 2 subclasses,
  inheritance stays <= 3 levels (BaseCase -> AuthCase -> the test class).
- Window size lives in pyproject `addopts` (--window-size), not in code.
- `created_ids` is cleaned by each test class's own tearDown: delete via API first,
  then call super().tearDown() (which logs out here).
"""

import uuid

from seleniumbase import BaseCase

from api_apiserver.auth import Auth
from api_apiserver.devices import DeviceApi
from config import Config

TOKEN_KEY = (
    "device-lab-token"  # frontend keeps the token in sessionStorage under this key
)


def uuid_name(prefix: str = "dev") -> str:
    """Unique device name so parallel workers (-n auto) never collide."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


class NoAuthCase(BaseCase):
    """Starts logged out on the app root (login page tests)."""

    def setUp(self, masterqa_mode=False):
        super().setUp()
        self.open(Config.BASE_URL)


class AuthCase(BaseCase):
    """Starts logged in via the API shortcut, already on /devices."""

    def setUp(self, masterqa_mode=False):
        super().setUp()
        self.created_ids: list[int] = []
        self.auth = Auth()
        self.device_api = DeviceApi(self.auth)
        # sessionStorage is per origin: open the origin first, then write the token.
        self.open(Config.BASE_URL)
        self.set_session_storage_item(TOKEN_KEY, self.auth.access_token)
        self.open(f"{Config.BASE_URL}/devices")

    def tearDown(self):
        self.auth.logout()
        super().tearDown()

    def delete_created_devices(self) -> None:
        """Call from the test class's tearDown, before super().tearDown()."""
        for device_id in self.created_ids:
            self.device_api.delete(device_id)
        self.created_ids.clear()
