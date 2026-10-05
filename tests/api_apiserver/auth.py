import requests

from config import Config


class Auth:
    """Log in through the API once and keep the token on a requests.Session.

    Tests reuse `auth.request` (already carries the Bearer header) for any API call,
    and AuthCase puts `auth.access_token` into the browser's sessionStorage.
    """

    def __init__(
        self,
        username: str = Config.APP_USERNAME,
        password: str = Config.APP_PASSWORD,
    ):
        self.login_path = f"{Config.API_URL}/auth/login"
        self.logout_path = f"{Config.API_URL}/auth/logout"
        self.request = requests.Session()
        self.username = username
        self.password = password
        self._set_tokens()

    def _get_login_api_response(self) -> requests.Response:
        body = {"username": self.username, "password": self.password}
        return self.request.post(self.login_path, json=body)

    def _set_tokens(self) -> None:
        response = self._get_login_api_response()
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
        self.request.headers["Authorization"] = f"Bearer {self.access_token}"

    def logout(self) -> None:
        self.request.post(self.logout_path)
