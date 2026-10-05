import pytest

from base.base_case import uuid_name

pytestmark = pytest.mark.api


class TestDevicesApi:
    """F3 at the API layer. No browser: fast, and safe with -n auto (unique names)."""

    def test_create_device_returns_201(self, api):
        "[API][Add device] 建立裝置回 201，GET 回同一筆"  # 🤝 AI
        name = uuid_name("api")
        res = api.create(name=name, type="Sensor", status="offline", location="B1")
        assert res.status_code == 201, res.text
        body = res.json()
        api.created_ids.append(body["id"])
        assert {k: body[k] for k in ("name", "type", "status", "location")} == {
            "name": name,
            "type": "Sensor",
            "status": "offline",
            "location": "B1",
        }

        got = api.get(body["id"])
        assert got.status_code == 200
        assert got.json()["name"] == name

    def test_duplicate_name_returns_409(self, api):
        "[API][Add device] 名稱重複回 409，訊息帶名稱"  # 🤝 AI
        name = uuid_name("api")
        first = api.create(name=name)
        assert first.status_code == 201, first.text
        api.created_ids.append(first.json()["id"])

        second = api.create(name=name)
        assert second.status_code == 409
        assert second.json()["detail"] == f"Device name '{name}' already exists"
