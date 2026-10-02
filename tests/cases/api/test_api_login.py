from seleniumbase import BaseCase

from api_apiserver.auth import Auth


class LoginApiTest(BaseCase):
    def setUp(self, masterqa_mode=False):
        super().setUp()
        self.open_url("http://localhost:8080/")

    def tearDown(self):
        super().tearDown()

    def test_api_login(self):
        "[Api][Login] 登入成功"
        self.auth = Auth()
        self.set_session_storage_item("device-lab-token", self.auth.access_token)
        self.open_url("http://localhost:8080/devices")
        self.assert_element_present("//*[text()='Log out']")
