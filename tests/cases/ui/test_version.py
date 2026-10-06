import pytest

from base.base_case import NoAuthCase
from pages.common.version_info import VersionInfo
from pages.login.login_page import LoginPage

pytestmark = pytest.mark.ui


class VersionTest(NoAuthCase):
    def test_web_and_api_versions_match(self):
        "[Version] 登入頁：Web 和 API 顯示同一個版本（前後端部署成同一版）"  # 🤝 AI
        LoginPage.open(self)
        web, api = VersionInfo.read(self)
        assert web == api, f"web {web} != api {api}"
        assert "…" not in api and "—" not in api, f"API version not loaded: {api}"
