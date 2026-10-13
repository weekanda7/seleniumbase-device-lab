import pytest

from base.base_case import NoAuthCase
from pages.common.version_info import VersionInfo
from pages.login.login_page import LoginPage

pytestmark = pytest.mark.ui


class VersionTest(NoAuthCase):
    def test_web_and_api_versions_match(self):
        "[Version] Login page: Web and API show the same version (frontend and backend deployed together)"
        LoginPage.open(self)
        web, api = VersionInfo.read(self)
        assert web == api, f"web {web} != api {api}"
        assert "…" not in api and "—" not in api, f"API version not loaded: {api}"
