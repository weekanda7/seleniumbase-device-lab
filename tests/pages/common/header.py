from seleniumbase import BaseCase

from pages.common.elements import tid


class Header:
    """Global header on every logged-in page (globally unique testids, no scoping needed)."""

    logo = "#logo"
    language_switch = tid("language-switch")
    en_radio = tid("en-radio")
    zh_tw_radio = tid("zh-tw-radio")
    logout_button = tid("logout-button")

    @staticmethod
    def switch_language(sb: BaseCase, lang: str = "en") -> None:
        """lang: "en" or "zh-TW". The choice is saved in localStorage."""
        sb.click(Header.en_radio if lang == "en" else Header.zh_tw_radio)

    @staticmethod
    def logout(sb: BaseCase) -> None:
        sb.click(Header.logout_button)
        sb.assert_url_contains("/login")
