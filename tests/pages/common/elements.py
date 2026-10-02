"""Locator helpers shared by every Page Object.

Rules come from .claude/skills/testid-spec:
- prefer data-testid; scope repeated testids by their container first
- antd renders Select / Dropdown options and Modals in a portal at the end of <body>
"""


def tid(test_id: str) -> str:
    """CSS selector for a data-testid."""
    return f'[data-testid="{test_id}"]'


def within(container: str, child: str) -> str:
    """CSS selector for `child` inside `container` (both CSS)."""
    return f"{container} {child}"


# antd building blocks that cannot take a testid
TABLE_ROW = "tr.ant-table-row"
TABLE_LOADING = ".ant-table .ant-spin-spinning"
ERROR_ALERT = ".ant-alert-error"  # red error Alert: no testid by spec, assert its text
FIELD_ERROR = ".ant-form-item-explain-error"  # validation message under a form field
