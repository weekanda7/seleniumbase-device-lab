from base.base_case import AuthCase


class LoginApiTest(AuthCase):
    def test_api_login(self):
        "[API][Login] API login shortcut: write the token to sessionStorage, then go straight to /devices"
        self.assert_url_contains("/devices")
        self.assert_element_present("//*[text()='Log out']")
