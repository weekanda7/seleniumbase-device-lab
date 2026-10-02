from seleniumbase import BaseCase

from pages.common.elements import tid, within


class ConfirmModal:
    """Delete confirmation (antd Modal.confirm).

    The Modal container can't take a testid, so it is located by class, and its
    buttons are scoped inside it: the detail page has its own `delete-button` too.
    """

    container = ".dl-warning-modal"
    title = within(container, ".ant-modal-confirm-title")
    content = within(container, ".ant-modal-confirm-content")
    delete_button = within(container, tid("delete-button"))
    cancel_button = within(container, tid("cancel-button"))

    @staticmethod
    def assert_title_contains(sb: BaseCase, text: str) -> None:
        sb.assert_text(text, ConfirmModal.title)

    @staticmethod
    def confirm(sb: BaseCase) -> None:
        sb.click(ConfirmModal.delete_button)
        sb.wait_for_element_absent(ConfirmModal.container)

    @staticmethod
    def cancel(sb: BaseCase) -> None:
        sb.click(ConfirmModal.cancel_button)
        sb.wait_for_element_absent(ConfirmModal.container)
