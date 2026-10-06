import os
import re

import pytest
import requests

from config import Config

pytestmark = pytest.mark.api

# Black-box: the test repo can't see the app's git, so check the shape of the value, not an exact one.
# A deploy pipeline that knows what it shipped can pin it: EXPECTED_VERSION=v0.1.0 pytest -m api
VERSION_RE = r"(v\d+\.\d+\.\d+(-\d+-g[0-9a-f]+)?|[0-9a-f]{7,40}|dev)(-dirty)?"
COMMIT_RE = r"[0-9a-f]{7,40}|unknown"


class TestVersionApi:
    def test_version_returns_valid_value(self):
        "[API][Version] /api/version 不用登入回 200，version / commit 是合法格式"  # 🤝 AI
        res = requests.get(f"{Config.API_URL}/version", timeout=10)
        assert res.status_code == 200, res.text
        body = res.json()
        assert re.fullmatch(VERSION_RE, body["version"]), body
        assert re.fullmatch(COMMIT_RE, body["commit"]), body

        expected = os.getenv("EXPECTED_VERSION")
        if expected:
            assert body["version"] == expected
