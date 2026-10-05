import pytest

from base.base_case import uuid_name
from db_client.device_db import DeviceDb

pytestmark = pytest.mark.db


class TestDevicesDb:
    """Write through the API, verify in Postgres (:5433): checks what was really persisted,
    not just what the API echoed back."""

    def test_created_device_is_persisted(self, api):
        "[DB][Add device] API 建立後，DB 欄位一致、有 created_at"  # 🤝 AI
        name = uuid_name("db")
        res = api.create(name=name, type="Switch", status="offline", location="  3F  ")
        assert res.status_code == 201, res.text
        device_id = res.json()["id"]
        api.created_ids.append(device_id)

        row = DeviceDb.find_by_id(device_id)
        assert row is not None
        assert row["name"] == name
        assert row["type"] == "Switch"
        assert row["status"] == "offline"
        assert row["location"] == "3F"  # API strips whitespace before saving
        assert row["created_at"] is not None

    def test_deleted_device_is_gone(self, api):
        "[DB][Delete device] API 刪除後，DB 查不到、GET 回 404"  # 🤝 AI
        name = uuid_name("db")
        res = api.create(name=name)
        assert res.status_code == 201, res.text
        device_id = res.json()["id"]
        api.created_ids.append(device_id)

        assert api.delete(device_id).status_code == 204

        assert DeviceDb.find_by_id(device_id) is None
        assert DeviceDb.count_by_name(name) == 0
        assert api.get(device_id).status_code == 404
