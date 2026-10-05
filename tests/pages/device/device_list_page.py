import time

from seleniumbase import BaseCase

from config import Config
from pages.common.confirm_modal import ConfirmModal
from pages.common.elements import TABLE_LOADING, TABLE_ROW, tid, xtid

SEARCH_DEBOUNCE_SECONDS = (
    0.4  # frontend waits this long after the last key before calling the API
)


def _tc(column: str) -> str:
    return tid(f"tc-{column}")


class DeviceListPage:
    url = f"{Config.BASE_URL}/devices"

    page_title = tid("page-title")
    add_device_button = tid("add-device-button")
    search_input = tid("search-input")
    search_clear_icon = (
        "//input[@data-testid='search-input']/following-sibling::span"
        "[contains(@class,'ant-input-suffix')]/*[contains(@class,'ant-input-clear-icon')]"
    )
    status_select = tid(
        "status-select"
    )  # outer div.ant-select: click this, not the inner input
    status_option = tid("status-option")  # rendered in a portal at the end of <body>
    total_num = tid("total-num")

    # table: titles appear once, cells repeat on every row (scope by row)
    tc_title_name = tid("tc-title-name")
    tc_title_type = tid("tc-title-type")
    tc_title_status = tid("tc-title-status")
    tc_title_location = tid("tc-title-location")
    tc_name = _tc("name")
    tc_type = _tc("type")
    tc_status = _tc("status")
    tc_location = _tc("location")
    row = TABLE_ROW

    # row-end More menu (antd Dropdown, options in a portal)
    more_button = tid("more-button")
    option_edit = tid("option-edit")
    option_remove = tid("option-remove")

    @staticmethod
    def row_by_name(name: str) -> str:
        """XPath of the table row whose name cell shows `name`."""
        return f"//tr[contains(@class,'ant-table-row')][.{xtid('tc-name', tag='td', text=name)}]"

    # ---------- navigation ----------
    @staticmethod
    def open(sb: BaseCase) -> None:
        sb.open(DeviceListPage.url)
        DeviceListPage.wait_for_loaded(sb)

    @staticmethod
    def wait_for_loaded(sb: BaseCase) -> None:
        sb.wait_for_element_visible(DeviceListPage.page_title)
        sb.wait_for_element_absent(TABLE_LOADING)

    @staticmethod
    def go_to_add_device(sb: BaseCase) -> None:
        sb.click(DeviceListPage.add_device_button)
        sb.assert_url_contains("/devices/new")

    @staticmethod
    def open_device(sb: BaseCase, name: str) -> None:
        sb.click(f"{DeviceListPage.row_by_name(name)}//a")
        sb.assert_url_contains("/devices/")

    # ---------- search / filter / sort ----------
    @staticmethod
    def search(sb: BaseCase, keyword: str) -> None:
        """Type a keyword, then wait out the debounce and the reload.

        Without the debounce wait, the old rows are still on screen and an assert would pass on stale data.
        """
        sb.type(DeviceListPage.search_input, keyword)
        time.sleep(SEARCH_DEBOUNCE_SECONDS + 0.2)
        sb.wait_for_element_absent(TABLE_LOADING)

    @staticmethod
    def clear_search(sb: BaseCase) -> None:
        """Click the input's clear (x) icon. Clearing with type("") may not notify React."""
        sb.click(DeviceListPage.search_clear_icon)
        time.sleep(SEARCH_DEBOUNCE_SECONDS + 0.2)
        sb.wait_for_element_absent(TABLE_LOADING)

    @staticmethod
    def filter_status(sb: BaseCase, label: str) -> None:
        """label is the visible text: "Online" / "Offline" (or 上線 / 離線 in Chinese)."""
        sb.click(DeviceListPage.status_select)
        sb.click(xtid("status-option", text=label))
        sb.wait_for_element_absent(TABLE_LOADING)

    @staticmethod
    def clear_status_filter(sb: BaseCase) -> None:
        sb.hover(DeviceListPage.status_select)
        sb.click(f"{DeviceListPage.status_select} .ant-select-clear")
        sb.wait_for_element_absent(TABLE_LOADING)

    @staticmethod
    def sort_by_name(sb: BaseCase) -> None:
        """Each click cycles ascending -> descending -> unsorted (client side)."""
        sb.click(DeviceListPage.tc_title_name)

    @staticmethod
    def filter_type(sb: BaseCase, device_type: str) -> None:
        """Client-side column filter: funnel icon in the Type header -> checkbox -> OK."""
        sb.click(f"{DeviceListPage.tc_title_type} .ant-table-filter-trigger")
        sb.click(
            f"//div[contains(@class,'ant-table-filter-dropdown')]//li[.//span[normalize-space()='{device_type}']]"
        )
        sb.click(".ant-table-filter-dropdown .ant-btn-primary")

    # ---------- row actions ----------
    @staticmethod
    def open_more_menu(sb: BaseCase, name: str) -> None:
        sb.click(f"{DeviceListPage.row_by_name(name)}{xtid('more-button')}")
        sb.wait_for_element_visible(DeviceListPage.option_edit)

    @staticmethod
    def edit_device(sb: BaseCase, name: str) -> None:
        DeviceListPage.open_more_menu(sb, name)
        sb.click(DeviceListPage.option_edit)
        sb.assert_url_contains("/edit")

    @staticmethod
    def delete_device(sb: BaseCase, name: str, confirm: bool = True) -> None:
        DeviceListPage.open_more_menu(sb, name)
        sb.click(DeviceListPage.option_remove)
        ConfirmModal.assert_title_contains(sb, name)
        if confirm:
            ConfirmModal.confirm(sb)
            sb.wait_for_element_absent(DeviceListPage.row_by_name(name))
        else:
            ConfirmModal.cancel(sb)

    # ---------- reading the table ----------
    @staticmethod
    def get_device_names(sb: BaseCase) -> list[str]:
        """Names on the current page, in display order."""
        return [el.text.strip() for el in sb.find_elements(DeviceListPage.tc_name)]

    @staticmethod
    def get_row(sb: BaseCase, name: str) -> dict[str, str]:
        row = DeviceListPage.row_by_name(name)
        return {
            col: sb.get_text(f"{row}{xtid(f'tc-{col}', tag='td')}").strip()
            for col in ("name", "type", "status", "location")
        }

    @staticmethod
    def assert_device_names(
        sb: BaseCase, expected: list[str], timeout: float = 5
    ) -> None:
        """Wait until the visible names equal `expected` (order-insensitive), then assert."""
        deadline = time.time() + timeout
        names = DeviceListPage.get_device_names(sb)
        while sorted(names) != sorted(expected) and time.time() < deadline:
            time.sleep(0.2)
            names = DeviceListPage.get_device_names(sb)
        assert sorted(names) == sorted(expected), (
            f"expected {sorted(expected)}, got {sorted(names)}"
        )
