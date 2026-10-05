import pytest

from base.base_case import AuthCase, uuid_name
from pages.common.toast import Toast
from pages.device.device_form_page import DeviceFormPage

pytestmark = pytest.mark.ui


class AddDeviceTest(AuthCase):
    """F3 Add a device."""

    def setUp(self, masterqa_mode=False):
        super().setUp()
        self.name = uuid_name("test")

    def tearDown(self):
        self.track_devices_named(
            self.name
        )  # UI-created device: find its id by name  # 🤝 AI
        self.delete_created_devices()  # API delete first, then logout + driver quit
        super().tearDown()

    def test_add_device_success(self):
        "[UI][Add device] 新增 Device 成功"
        DeviceFormPage.create_device(self, name=self.name)
        Toast.assert_success(self, f"Device {self.name} created")

    def test_duplicate_name(self):
        "[UI][Add device] 名稱重複：欄位顯示已存在，停在新增頁"  # 🤝 AI
        res = self.device_api.create(
            name=self.name
        )  # arrange through the API: fast, no UI dependency
        assert res.status_code == 201, res.text
        self.created_ids.append(res.json()["id"])

        DeviceFormPage.create_device(self, name=self.name)

        DeviceFormPage.assert_name_error(
            self, f"Device name '{self.name}' already exists"
        )
        self.assert_url_contains("/devices/new")
        assert (
            len(self.device_api.list(q=self.name).json()) == 1
        )  # nothing extra was saved
