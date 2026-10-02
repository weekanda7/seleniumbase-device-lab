from seleniumbase import BaseCase

from config import Config
from pages.common.elements import ERROR_ALERT, tid

TOKEN_KEY = "device-lab-token"  # sessionStorage key used by frontend/src/api.ts


class LoginPage:
    url = f"{Config.BASE_URL}/login"

    page_title = tid("page-title")
    username_field = tid("username-field")
    username_input = tid("username-input")
    password_field = tid("password-field")
    password_input = tid("password-input")
    login_button = tid("login-button")
    error_alert = ERROR_ALERT

    @staticmethod
    def open(sb: BaseCase) -> None:
        sb.open(LoginPage.url)
        sb.wait_for_element_visible(LoginPage.login_button)

    @staticmethod
    def login(sb: BaseCase, username: str, password: str) -> None:
        """Fill the form and submit. Does not assert the result (use for success and failure)."""
        sb.type(LoginPage.username_input, username)
        sb.type(LoginPage.password_input, password)
        sb.click(LoginPage.login_button)

    @staticmethod
    def login_as_default_user(sb: BaseCase) -> None:
        """UI login with the .env account, then wait until the device list is shown."""
        LoginPage.open(sb)
        LoginPage.login(sb, Config.APP_USERNAME, Config.APP_PASSWORD)
        sb.assert_url_contains("/devices")

    @staticmethod
    def login_by_token(
        sb: BaseCase, token: str, landing_path: str = "/devices"
    ) -> None:
        """Skip the login form: put an API token into sessionStorage.

        Storage belongs to an origin, so open a page on :8080 first, then write it.
        """
        sb.open(LoginPage.url)
        sb.set_session_storage_item(TOKEN_KEY, token)
        sb.open(f"{Config.BASE_URL}{landing_path}")
        sb.assert_url_contains(landing_path)

    @staticmethod
    def assert_login_error(
        sb: BaseCase, text: str = "Invalid username or password"
    ) -> None:
        sb.assert_text(text, LoginPage.error_alert)
        sb.assert_url_contains("/login")
