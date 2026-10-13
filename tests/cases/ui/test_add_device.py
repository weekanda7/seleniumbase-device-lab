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
        self.track_devices_named(self.name)  # UI-created device: find its id by name
        self.delete_created_devices()  # API delete first, then logout + driver quit
        super().tearDown()

    def test_add_device_success(self):
        """
        [UI][Add device] Add a device successfully

        Given I am logged in (admin; API shortcut: POST /api/auth/login, token written to sessionStorage)
        When I enter a unique name {name}, type Router, status online on the add-device page (/devices/new) and press Save
        Then a success toast shows "Device {name} created"

        {name} = uuid_name("test"), e.g. test-1a2b3c4d
        """
        DeviceFormPage.create_device(self, name=self.name)
        Toast.assert_success(self, f"Device {self.name} created")

    def test_duplicate_name(self):
        """
        [UI][Add device] Duplicate name: the field shows it already exists and the page stays on the add form

        Given I am logged in (admin; API shortcut: POST /api/auth/login, token written to sessionStorage)
        And a device named {name} was created via the API (POST /api/devices -> 201)
        When I enter the same name {name} on the add-device page (/devices/new) and press Save
        Then the name field shows "Device name '{name}' already exists"
        And the URL is still /devices/new
        And searching by name returns exactly 1 device (GET /api/devices?q={name})

        {name} = uuid_name("test"), e.g. test-1a2b3c4d
        """
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
