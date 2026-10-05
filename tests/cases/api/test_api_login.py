from base.base_case import AuthCase


class LoginApiTest(AuthCase):
    def test_api_login(self):
        "[Api][Login] API 登入捷徑：token 寫進 sessionStorage 後直接進 /devices"
        self.assert_url_contains("/devices")
        self.assert_element_present("//*[text()='Log out']")
