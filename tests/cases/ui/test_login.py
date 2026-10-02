from seleniumbase import BaseCase

from config import Config
from pages.login.login_page import LoginPage


class LoginTest(BaseCase):
    def setUp(self, masterqa_mode=False):
        super().setUp()
        self.open_url("http://localhost:8080/")

    def tearDown(self):
        super().tearDown()

    def test_login(self):
        "[Login] 輸入 admin 帳密，並按下 Log button，登入成功"
        LoginPage.login(self, Config.APP_USERNAME, Config.APP_PASSWORD)
        self.assert_element_present("//*[text()='Log out']")
