import pytest

from base.base_case import AuthCase, uuid_name
from pages.device.device_list_page import DeviceListPage

pytestmark = pytest.mark.ui


class DeviceListTest(AuthCase):
    """F2 Device list. Tests only assert on devices they created (unique prefix),
    so they stay green with -n auto even while other workers add rows."""

    def tearDown(self):
        self.delete_created_devices()  # API delete first, then logout + driver quit
        super().tearDown()

    def _create(self, name: str, status: str = "online") -> None:
        res = self.device_api.create(name=name, status=status)
        assert res.status_code == 201, res.text
        self.created_ids.append(res.json()["id"])

    # TODO(Henry): test_search_by_name_or_location_case_insensitive

    def test_filter_by_status(self):
        "[UI][Device list] 狀態篩選 Offline 只看到離線裝置，清除篩選後恢復"  # 🤝 AI
        prefix = uuid_name("flt")
        online, offline = f"{prefix}-on", f"{prefix}-off"
        self._create(online, "online")
        self._create(offline, "offline")
        DeviceListPage.open(self)
        DeviceListPage.search(self, prefix)  # narrow to this test's rows only
        DeviceListPage.assert_device_names(self, [online, offline])

        DeviceListPage.filter_status(self, "Offline")
        DeviceListPage.assert_device_names(self, [offline])

        DeviceListPage.clear_status_filter(self)
        DeviceListPage.assert_device_names(self, [online, offline])
