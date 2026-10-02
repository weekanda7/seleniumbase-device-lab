import requests

from config import Config


class Auth:
    def __init__(
        self,
        username: str = Config.APP_USERNAME,
        password: str = Config.APP_PASSWORD,
    ):
        self.base_url = "http://localhost:8080"
        self.login_path = f"{self.base_url}/api/auth/login"
        self.request = requests.session()
        self.request.headers["authorization"] = None
        self.username = username
        self.password = password
        self._set_tokens()

    def _get_login_api_response(self):
        body = {"username": self.username, "password": self.password}
        return self.request.post(self.login_path, json=body, verify=False)

    def _set_tokens(self):
        response = self._get_login_api_response()
        response.raise_for_status()
        _access_res = response.json()
        self.access_token = _access_res["access_token"]
        self.request.headers["authorization"] = f"Bearer {self.access_token}"

    def logout(self):
        self.request.post(f"{self.base_url}/api/auth/logout", verify=True)
