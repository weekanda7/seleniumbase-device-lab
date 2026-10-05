from seleniumbase import BaseCase

from config import Config
from pages.common.elements import ERROR_ALERT, FIELD_ERROR, tid, xtid


class DeviceFormPage:
    """Shared by "Add device" (/devices/new) and "Edit device" (/devices/{id}/edit)."""

    new_url = f"{Config.BASE_URL}/devices/new"

    page_title = tid("page-title")
    name_field = tid("name-field")
    name_input = tid("name-input")
    type_field = tid("type-field")
    type_select = tid(
        "type-select"
    )  # outer div.ant-select: click this, not the inner input
    type_option = tid("type-option")  # rendered in a portal at the end of <body>
    status_field = tid("status-field")
    online_radio = tid("online-radio")
    offline_radio = tid("offline-radio")
    location_field = tid("location-field")
    location_input = tid("location-input")
    save_button = tid("save-button")
    cancel_button = tid("cancel-button")
    error_alert = ERROR_ALERT

    @staticmethod
    def open_new(sb: BaseCase) -> None:
        sb.open(DeviceFormPage.new_url)
        sb.wait_for_element_visible(DeviceFormPage.save_button)

    @staticmethod
    def select_type(sb: BaseCase, device_type: str) -> None:
        sb.click(DeviceFormPage.type_select)
        sb.click(xtid("type-option", text=device_type))

    @staticmethod
    def select_status(sb: BaseCase, status: str) -> None:
        """status: "online" or "offline"."""
        if sb.is_selected(tid(f"{status}-radio")):
            return
        sb.click(tid(f"{status}-radio"))

    @staticmethod
    def fill(
        sb: BaseCase,
        name: str | None = None,
        device_type: str | None = None,
        status: str | None = None,
        location: str | None = None,
    ) -> None:
        """Only touches the fields you pass (handy for the edit page)."""
        if name is not None:
            sb.type(DeviceFormPage.name_input, name)
        if device_type is not None:
            DeviceFormPage.select_type(sb, device_type)
        if status is not None:
            DeviceFormPage.select_status(sb, status)
        if location is not None:
            sb.type(DeviceFormPage.location_input, location)

    @staticmethod
    def save(sb: BaseCase) -> None:
        sb.click(DeviceFormPage.save_button)

    @staticmethod
    def cancel(sb: BaseCase) -> None:
        sb.click(DeviceFormPage.cancel_button)

    @staticmethod
    def create_device(
        sb: BaseCase,
        name: str,
        device_type: str = "Router",
        status: str = "online",
        location: str = "",
    ) -> None:
        """Open the add page, fill everything, save. Does not assert the result."""
        DeviceFormPage.open_new(sb)
        DeviceFormPage.fill(
            sb, name=name, device_type=device_type, status=status, location=location
        )
        DeviceFormPage.save(sb)

    @staticmethod
    def assert_name_error(sb: BaseCase, text: str) -> None:
        sb.assert_text(text, f"#device_name_help {FIELD_ERROR}")
