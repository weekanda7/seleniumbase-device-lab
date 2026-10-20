---
name: testid-spec
description: data-testid naming rules (React + Ant Design). Use when adding or changing any UI element in frontend/src, or when writing SeleniumBase locators / Page Objects, so testids are derivable, stable and consistent across the project.
---

> Entry index: `.claude/skills/index/SKILL.md` — where each kind of question is answered in this repo.

# testid-spec

Follow this when adding testids in the frontend or locating elements in tests. The full spec (with cases, pitfalls, Android comparison) is in `references/testid-spec.md`; this is the short version + this repo's mapping table.

## 1. Decide whether to add a testid (locator priority)

| Priority | Strategy | Use for |
|---|---|---|
| 1 | `data-testid` | Form fields, table columns, icon buttons, menus, status indicators, **buttons whose text changes** |
| 2 | Tag + text | Ordinary buttons with fixed text, error messages |
| 3 | Semantic attributes | `aria-label`, `role="tooltip"`, `placeholder` |
| 4 | Framework class (contains) | Third-party components where attributes can't be injected, e.g. antd Modal |
| 5 | None | Elements with no testing need (state "no testid needed" in the spec) |

Special case in this repo: **there is an English / Chinese i18n switch**, so button text isn't stable → every clickable button gets a testid.
The red error Alert gets **no** testid; tests check it by text (which also checks the copy; compare against the current language).

## 2. Naming format

- The attribute name is always `data-testid` (never `data_testid`, `date-testid`)
- All lowercase, kebab-case, English; the subject comes from the on-screen English label: `Email address` → `email-address`
- Basic structure `{subject}-{component type}`; a few categories use a prefix (see section 4)
- Avoid dynamic values; if unavoidable, document the format, e.g. `status-{state}`

## 3. Suffix dictionary

| Suffix | Meaning | Example |
|---|---|---|
| `-field` | Field **label** | `name-field` |
| (none) | Field **read-only value** | `location` |
| `-input` / `-textarea` | Input box | `name-input` |
| `-select` / `-option` | antd Select itself / its options | `type-select` / `type-option` |
| `-button` | Button; icon-only uses `-icon-button` | `save-button`, `back-icon-button` |
| `-edit-button` | Edit icon next to a section title | `basic-info-edit-button` |
| `-link` | Link | `breadcrumb-link` |
| `-checkbox` / `-radio` / `-switch` | Prefixed with the label or option text | `online-radio`, `language-switch` |
| `-tab` / `-title` / `-alert` / `-area` / `-menu-item` | Tab / section title / info box / container / side menu item | `basic-info-title` |

**Field trio**: `{name}-field` (label), `{name}-input` (editable), `{name}` (read-only value).

## 4. Prefix dictionary

| Prefix | Meaning | Example |
|---|---|---|
| `tc-title-` / `tc-` | Table column header / the column's cell in each row | `tc-title-name` / `tc-name` |
| `option-` | Options of an antd **Dropdown** (action menu) | `option-edit`, `option-remove` |
| `status-` | Status indicator | `status-online`, `status-offline` |
| `breadcrumb-` | Breadcrumb | `breadcrumb-link`, `breadcrumb-name` |
| `step-` / `meta-` / `rank-` | Step wizard / dashboard card / leaderboard | `step-completed` |

`-option` (a Select option, belongs to a field) ≠ `option-` (a Dropdown option, is itself an action).

## 5. Page templates

- **List**: `page-title`, `tc-title-{col}` / `tc-{col}`, row-end `more-button` → `option-edit` / `option-remove`, `add-{resource}-button`, `total-num`
- **Detail**: `breadcrumb-link` / `breadcrumb-name`, `back-icon-button`, `page-title`, `{section}-title`, `{section}-edit-button`, the field trio
- **Modal**: the antd Modal container can't take a testid → locate it by `className` (this repo's prefix is `dl-`: `dl-warning-modal`); title / content via `ant-modal-confirm-title` / `ant-modal-confirm-content`; fields and buttons inside follow the normal rules

## 6. Scoping

The same testid may repeat in different containers (`page-title` is on every page; `delete-button` is on both the detail page and the confirm modal).
1. Locate the container first (modal class, table row, `-area`), then search inside it
2. Only globally unique elements (Header, `logout-button`, `language-switch`) may be found directly
3. `tc-*` exists in every row: use a row index, or find the row by text inside it (`tr.ant-table-row` containing some text); antd rows also have `data-row-key={id}`

### 6.1 CSS or XPath (test side, `tests/pages/common/elements.py`)

| Case | Use | Example |
|---|---|---|
| Single element, globally unique or already inside a container | `tid()` (CSS) | `tid("save-button")` |
| Need to match text (options, rows) | `xtid(..., text=)` (XPath) | `xtid("status-option", text="Offline")` |
| Scope to a row / container first, then search inside | `xtid()` appended to an XPath | `f"{row}{xtid('tc-location', tag='td')}"` |
| antd components that only have classes | CSS class | `.ant-table .ant-spin-spinning` |

- CSS and XPath **can't be chained**: once a locator starts as XPath, keep using `xtid()`
- Don't switch everything to XPath: XPath can only match classes with `contains(@class, …)`, which hits similar classes by mistake, and it reads worse

## 7. antd implementation tips (this repo)

| Component | How to add it | Testing notes |
|---|---|---|
| `Input` / `Input.Password` / `Input.Search` | `data-testid` directly; it lands on the `<input>` | — |
| `Select` | `data-testid` lands on the outer `div.ant-select`; wrap options with `optionRender` in `<span data-testid="{name}-option">` | **Click the outer div**; clicking the inner input is blocked by the selection item; options render in a portal at the end of `<body>` |
| `Table` columns | Return the testid from `onHeaderCell` / `onCell` (`tc()` helper) | — |
| `Dropdown` options | `label: <span data-testid="option-edit">` | The menu is also in a portal |
| `Form.Item` label | `label={<FieldLabel name="name">…</FieldLabel>}` → `name-field` | — |
| `Modal.confirm` buttons | `okButtonProps: { ...testId("delete-button") }` (`testId()` is in `src/api.ts`) | Find `.dl-warning-modal` first, then the button |
| `message` toast | No testid; add `className: "toast-success"` / `"toast-error"` | It disappears on its own: check as soon as it appears, don't sleep |

## 8. Mapping table for this repo

| Page | testids |
|---|---|
| Global Header | `id="logo"`, `language-switch` (`en-radio` / `zh-tw-radio`), `logout-button` |
| Login | `page-title`, `username-field` / `username-input`, `password-field` / `password-input`, `login-button` |
| Device list | `page-title`, `add-device-button`, `search-input`, `status-select` / `status-option`, `total-num`, `tc-title-{name,type,status,location}` / `tc-{…}`, `more-button` → `option-edit` / `option-remove` |
| Add / edit | `page-title`, `name-field` / `name-input`, `type-field` / `type-select` / `type-option`, `status-field` / `online-radio` / `offline-radio`, `location-field` / `location-input`, `save-button`, `cancel-button` |
| Device detail | `back-icon-button`, `breadcrumb-link` / `breadcrumb-name`, `page-title`, `delete-button`, `basic-info-title`, `basic-info-edit-button`, `{type,status,location,created}-field`, `type` / `location` / `created`, `status-online` / `status-offline` |
| Version (login page, site-wide Footer) | `version-area` → `web-version`, `api-version` (read-only values, no suffix) |
| Delete confirm modal | `.dl-warning-modal` → `.ant-modal-confirm-title`, `delete-button`, `cancel-button` |

## 9. Checklist for adding a testid

1. Check the dictionaries in sections 3 and 4 first; reuse an existing suffix / prefix, don't invent synonyms
2. Add a prefix / suffix to generic words that collide (`tag`, `item`, `name`)
3. Update the section 8 mapping table (it is the QA / FE contract)
4. Only `data-testid`: `grep -rnE "data_testid|date-testid" frontend/src` should return nothing
5. `make -C frontend lint-check` is green
