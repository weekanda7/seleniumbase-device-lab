from seleniumbase import BaseCase

from pages.common.elements import tid

LOADING = "…"  # shown until GET /api/version answers


class VersionInfo:
    """Web / API version line: login page and the footer of every page behind login."""

    web_version = tid("web-version")
    api_version = tid("api-version")

    @staticmethod
    def read(sb: BaseCase) -> tuple[str, str]:
        """Wait until the API version has loaded, then return (web, api), e.g. ("v0.1.0 (abc1234)", ...)."""
        sb.wait_for_element_visible(VersionInfo.api_version)
        sb.wait_for_text_not_visible(LOADING, VersionInfo.api_version)
        return sb.get_text(VersionInfo.web_version), sb.get_text(
            VersionInfo.api_version
        )
