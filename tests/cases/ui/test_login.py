from base.base_case import NoAuthCase
from config import Config
from pages.login.login_page import LoginPage


class LoginTest(NoAuthCase):
    def test_login(self):
        "[Login] Enter the admin credentials and press Log in: login succeeds"
        LoginPage.login(self, Config.APP_USERNAME, Config.APP_PASSWORD)
        self.assert_element_present("//*[text()='Log out']")
