import pytest

from base.base_case import AuthCase, uuid_name
from pages.common.toast import Toast
from pages.device.device_detail_page import DeviceDetailPage

pytestmark = pytest.mark.ui


class DeviceDetailTest(AuthCase):
    """Device detail page (/devices/{id}) + F5 delete from the detail page.  # 🤝 AI
    Each test arranges its own device through the API, so it never depends on seed data."""

    def tearDown(self):
        self.delete_created_devices()  # API delete first (404 is fine if the test deleted it)
        super().tearDown()

    def _create(self, **fields) -> dict:
        """Arrange through the API: fast, no UI dependency. Returns the created device."""
        res = self.device_api.create(**fields)
        assert res.status_code == 201, res.text
        device = res.json()
        self.created_ids.append(device["id"])
        return device

    def test_show_device_info(self):
        "[UI][Device detail] 詳細頁顯示裝置的名稱、類型、狀態、位置（deferred asserts）"  # 🤝 AI
        name = uuid_name("dt")
        device = self._create(name=name, type="Switch", status="offline", location="B2")

        DeviceDetailPage.open(self, device["id"])

        self.deferred_assert_exact_text(name, DeviceDetailPage.page_title)
        self.deferred_assert_exact_text(name, DeviceDetailPage.breadcrumb_name)
        self.deferred_assert_exact_text("Switch", DeviceDetailPage.type)
        self.deferred_assert_element(DeviceDetailPage.status_offline)
        self.deferred_assert_exact_text("B2", DeviceDetailPage.location)
        self.process_deferred_asserts()  # required: without it every deferred failure is silently dropped

    def test_back_to_the_list(self):
        "[UI][Device detail] 返回按鈕回到裝置列表"  # 🤝 AI
        device = self._create(name=uuid_name("dt"))

        DeviceDetailPage.open(self, device["id"])
        DeviceDetailPage.back_to_list(self)  # asserts the URL is /devices

    def test_open_edit_from_the_detail_page(self):
        "[UI][Device detail] Basic info 的編輯圖示進到編輯頁"  # 🤝 AI
        device = self._create(name=uuid_name("dt"))

        DeviceDetailPage.open(self, device["id"])
        DeviceDetailPage.go_to_edit(self)  # asserts the URL contains /edit
        self.assert_url_contains(f"/devices/{device['id']}/edit")

    def test_delete_from_the_detail_page(self):
        "[UI][Device detail] F5 詳細頁刪除：確認後回列表，API 查不到"  # 🤝 AI
        name = uuid_name("dt")
        device = self._create(name=name)

        DeviceDetailPage.open(self, device["id"])
        DeviceDetailPage.delete(
            self, confirm=True
        )  # confirms, then asserts we are back on /devices

        Toast.assert_success(self, f"Device {name} deleted")
        assert self.device_api.get(device["id"]).status_code == 404

    def test_cancel_the_dialog(self):
        "[UI][Device detail] F5 取消刪除：留在詳細頁，裝置還在"  # 🤝 AI
        name = uuid_name("dt")
        device = self._create(name=name)

        DeviceDetailPage.open(self, device["id"])
        DeviceDetailPage.delete(self, confirm=False)

        self.assert_exact_text(name, DeviceDetailPage.page_title)
        assert self.device_api.get(device["id"]).status_code == 200

    @pytest.mark.xfail(strict=True, reason="Demo deferred assert api")
    def test_demo_deferred_assert(self):
        "[UI][Device detail] Demo deferred assert api"
        name = uuid_name("dt")
        device = self._create(name=name, type="Switch", status="offline", location="B2")

        DeviceDetailPage.open(self, device["id"])

        # deferred: a wrong field is recorded and the test keeps going, so one run shows every broken field
        self.deferred_assert_exact_text("fail", DeviceDetailPage.page_title)
        self.deferred_assert_exact_text(name, DeviceDetailPage.breadcrumb_name)
        self.deferred_assert_exact_text("fail", DeviceDetailPage.type)
        self.deferred_assert_element(DeviceDetailPage.status_offline)
        self.deferred_assert_exact_text("fail", DeviceDetailPage.location)
        self.process_deferred_asserts()  # required: without it every deferred failure is silently dropped
