"""Locator helpers shared by every Page Object.

Rules come from .claude/skills/testid-spec:
- prefer data-testid; scope repeated testids by their container first
- antd renders Select / Dropdown options and Modals in a portal at the end of <body>
"""


def tid(test_id: str) -> str:
    """CSS selector for a data-testid. Default for a single element."""
    return f'[data-testid="{test_id}"]'


def xtid(test_id: str, tag: str = "*", text: str | None = None) -> str:
    """XPath step for a data-testid, starting with `//` so it can be appended to another XPath.

    Use it when you need scoping or text, which CSS can't do:
        xtid("status-option", text="Offline")          -> pick an option by its label
        f"{row}{xtid('tc-location', tag='td')}"        -> a cell inside one table row
    CSS and XPath can't be concatenated, so once a locator starts as XPath, keep using xtid().
    """
    step = f"//{tag}[@data-testid='{test_id}']"
    if text is not None:
        step += f"[normalize-space()='{text}']"
    return step


def within(container: str, child: str) -> str:
    """CSS selector for `child` inside `container` (both CSS)."""
    return f"{container} {child}"


# antd building blocks that cannot take a testid
TABLE_ROW = "tr.ant-table-row"
TABLE_LOADING = ".ant-table .ant-spin-spinning"
ERROR_ALERT = ".ant-alert-error"  # red error Alert: no testid by spec, assert its text
FIELD_ERROR = ".ant-form-item-explain-error"  # validation message under a form field
