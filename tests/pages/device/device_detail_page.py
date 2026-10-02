from seleniumbase import BaseCase

from config import Config
from pages.common.confirm_modal import ConfirmModal
from pages.common.elements import tid, within


class DeviceDetailPage:
    back_icon_button = tid("back-icon-button")
    breadcrumb_link = tid("breadcrumb-link")
    breadcrumb_name = tid("breadcrumb-name")
    page_title = tid("page-title")  # the device name
    # scoped: the confirm Modal also has a delete-button
    delete_button = within(".page-header", tid("delete-button"))
    basic_info_title = tid("basic-info-title")
    basic_info_edit_button = tid("basic-info-edit-button")

    # read-only field trio: {name}-field (title) / {name} (value)
    type_field = tid("type-field")
    type = tid("type")
    status_field = tid("status-field")
    status_online = tid("status-online")
    status_offline = tid("status-offline")
    location_field = tid("location-field")
    location = tid("location")
    created_field = tid("created-field")
    created = tid("created")

    @staticmethod
    def open(sb: BaseCase, device_id: int) -> None:
        sb.open(f"{Config.BASE_URL}/devices/{device_id}")
        sb.wait_for_element_visible(DeviceDetailPage.basic_info_title)

    @staticmethod
    def wait_for_loaded(sb: BaseCase) -> None:
        sb.wait_for_element_visible(DeviceDetailPage.basic_info_title)

    @staticmethod
    def get_status(sb: BaseCase) -> str:
        """ "online" or "offline", read from which status-{state} testid is present."""
        return (
            "online"
            if sb.is_element_present(DeviceDetailPage.status_online)
            else "offline"
        )

    @staticmethod
    def get_info(sb: BaseCase) -> dict[str, str]:
        DeviceDetailPage.wait_for_loaded(sb)
        return {
            "name": sb.get_text(DeviceDetailPage.page_title).strip(),
            "type": sb.get_text(DeviceDetailPage.type).strip(),
            "status": DeviceDetailPage.get_status(sb),
            "location": sb.get_text(DeviceDetailPage.location).strip(),
        }

    @staticmethod
    def go_to_edit(sb: BaseCase) -> None:
        sb.click(DeviceDetailPage.basic_info_edit_button)
        sb.assert_url_contains("/edit")

    @staticmethod
    def back_to_list(sb: BaseCase) -> None:
        sb.click(DeviceDetailPage.back_icon_button)
        sb.assert_url_contains("/devices")

    @staticmethod
    def delete(sb: BaseCase, confirm: bool = True) -> None:
        name = sb.get_text(DeviceDetailPage.page_title).strip()
        sb.click(DeviceDetailPage.delete_button)
        ConfirmModal.assert_title_contains(sb, name)
        if confirm:
            ConfirmModal.confirm(sb)
            sb.wait_for_element_absent(DeviceDetailPage.basic_info_title)
            sb.assert_url_contains("/devices")
        else:
            ConfirmModal.cancel(sb)
