from seleniumbase import BaseCase


class Toast:
    """antd message toasts. They disappear after ~3 s: wait for them, never sleep first."""

    success = ".toast-success"
    error = ".toast-error"

    @staticmethod
    def assert_success(sb: BaseCase, text: str, timeout: float = 5) -> None:
        sb.assert_text(text, Toast.success, timeout=timeout)

    @staticmethod
    def assert_error(sb: BaseCase, text: str, timeout: float = 5) -> None:
        sb.assert_text(text, Toast.error, timeout=timeout)
