import pytest

from base.base_case import AuthCase, uuid_name
from pages.device.device_form_page import DeviceFormPage

pytestmark = pytest.mark.ui


class AddDeviceTest(AuthCase):
    """F3 Add a device."""

    def tearDown(self):
        self.delete_created_devices()  # API delete first, then logout + driver quit
        super().tearDown()

    # TODO(Henry): test_add_device

    def test_duplicate_name(self):
        "[UI][Add device] 名稱重複：欄位顯示已存在，停在新增頁"  # 🤝 AI
        name = uuid_name("dup")
        res = self.device_api.create(name=name)  # arrange through the API: fast, no UI dependency
        assert res.status_code == 201, res.text
        self.created_ids.append(res.json()["id"])

        DeviceFormPage.create_device(self, name=name)

        DeviceFormPage.assert_name_error(self, f"Device name '{name}' already exists")
        self.assert_url_contains("/devices/new")
        assert len(self.device_api.list(q=name).json()) == 1  # nothing extra was saved
