# Test ID Spec

> Distilled from experience writing testid conventions for React + Ant Design web apps.
> All names below are generic examples. A mapping to Android (Espresso / Compose) is at the end.

---

## 1. Goals and principles

1. **Stable locators**: don't depend on DOM structure, CSS classes or layout position, so tests don't change with every redesign.
2. **The name says what it is**: a testid tells you "which field" and "which component".
3. **Derivable, no lookup needed**: the same kind of component follows the same rule, so test authors can derive the testid.
4. **Owned by QA and FE together**: QA defines the spec, FE implements it; each page's wiki is the contract between them.

---

## 2. Locator priority

Not every element needs a testid. Choose in this order:

| Priority | Strategy | When | Example |
|---|---|---|---|
| 1 | `data-testid` | Form fields, table columns, icon buttons, menus, status indicators and other elements without stable text | `data-testid="login-button"` |
| 2 | Tag + text | Ordinary buttons with clear text, error messages | `//button//*[text()="Confirm"]` |
| 3 | Semantic attributes | Accessibility or native attributes are enough to identify it | `aria-label="Select all"`, `role="tooltip"`, `placeholder="Start date"` |
| 4 | UI framework class (contains match) | Third-party components that can't take a testid (Ant Design Modal) | `contains(@class, "ant-modal-title")` |
| 5 | None | Elements with no testing need | The "Download all" button is explicitly marked as needing no testid |

**Rules**
- Ordinary buttons are **located by text first**; add a testid only in special cases (unstable text, duplicates, icon only).
- Red error messages (Alert) get **no testid**; verify them by text, which also verifies the copy.
- Framework-generated elements that can't take attributes (e.g. Tags Select options) must be marked "cannot take a testid" in the wiki, with the alternative locator written down.

---

## 3. Naming format

| Item | Rule |
|---|---|
| Attribute name | Always `data-testid` (**never** `data_testid`, `date-testid`) |
| Case | All lowercase |
| Separator | kebab-case (`-`) |
| Language | English, taken from the on-screen English label |
| Basic structure | `{subject}-{component type}`, e.g. `account-input`, `notification-switch` |
| Exceptions | A few categories use a **prefix**, e.g. `option-edit`, `tc-server-name` (see section 5) |
| Subject | The on-screen label in kebab-case: `Email address` → `email-address` |
| Abbreviations | Common abbreviations are fine but must be consistent project-wide: `web-app`, `app-info`, `ip` |
| Dynamic values | Avoid; if unavoidable, document the variable format, e.g. `{project_name}`, `{type}` |

---

## 4. Suffix dictionary

| Suffix | Meaning | Example |
|---|---|---|
| `-field` | A form field's **label** | `password-field` |
| (no suffix) | A form field's **read-only value** | `owner-name`, `member-name` |
| `-input` | Text input | `password-input` |
| `-textarea` | Multi-line input | `reason-textarea` |
| `-select` | The dropdown itself | `region-select` |
| `-option` | A dropdown option (Select type) | `region-option` |
| `-button` | Button / icon button | `back-icon-button`, `menu-button` |
| `-edit-button` | Edit icon next to a section title | `basic-info-edit-button` |
| `-export-button` | Export button on a list page, prefixed with the resource name | `device-export-button` |
| `-link` | Link | `forgot-password-link` |
| `-checkbox` | Checkbox, prefixed with its label | `case-sensitive-checkbox` |
| `-radio` | Radio button, prefixed with its option text | `linux-radio` |
| `-switch` | Toggle | `two-factor-authentication-switch` |
| `-tab` | Tab | `device-tab` |
| `-title` | Section / form title | `basic-info-title` |
| `-alert` | Info box (blue or grey description) | `info-alert` |
| `-tooltip` | Tooltip trigger icon, prefixed with the element it belongs to | `new-password-field-tooltip` |
| `-area` | A whole section container | `device-status-area` |
| `-label` | Secondary label text | `remember-me-label` |
| `-img` | Image | `login-footer-img` |
| `-menu-item` | Side menu item | `settings-menu-item` |

The **field trio** is the most common pattern; a form field usually has all three:

```
{name}-field    → the field label "Account"
{name}-input    → the input when editable (or -select / -textarea)
{name}          → the value shown when read-only
```

---

## 5. Prefix dictionary

| Prefix | Meaning | Example |
|---|---|---|
| `option-` | Options of a Dropdown (action menu, More menu) | `option-edit`, `option-log-out` |
| `tc-title-` | Table column **header** (table column title) | `tc-title-server-name` |
| `tc-` | Table column **content** (appears in every row) | `tc-server-name` |
| `step-` | Each step of a multi-step wizard | `step-select-target`, `step-completed` |
| `meta-` | Elements inside a dashboard card | `meta-title`, `meta-num`, `meta-devices-area` |
| `status-` | Status indicator | `status-running`, `status-stopped` |
| `rank-` | Leaderboard elements | `rank-title`, `rank-item-value` |
| `breadcrumb-` | Breadcrumb | `breadcrumb-link`, `breadcrumb-name` |

**`-option` vs `option-`**
- Ant Design **Select** (form dropdown) → suffix `-option`, because the option belongs to a field: `ip-address-option`.
- Ant Design **Dropdown** (action menu) → prefix `option-`, because the option is itself an action: `option-remove`.

---

## 6. Shared component rules (Elements)

| Component | Rule | Example |
|---|---|---|
| Logo | Use `id` | `id="logo"` |
| Error message (red Alert) | None; verify by text | `//*[text()="..."]` |
| Ordinary button | Text first; in special cases `{text}-button` | `connect-button` |
| Icon button | `{function}-icon-button` or `{function}-button` | `back-icon-button` |
| Select-all checkbox | `aria-label="Select all"` | — |
| Checkbox | `{label}-checkbox` | `exact-match-checkbox` |
| Radio (with text) | `{text}-radio` | `windows-radio` |
| Radio (no text) | `{owning item}-radio` | `default-radio` |
| Switch | `{label}-switch` | `alert-switch` |
| Link | `{text}-link` | `view-all-link` |
| Unread dot | Fixed value | `unread`; blinking version `flash-unread` |
| Status indicator | `status-{state}` | `status-running` / `processing` / `stopped` / `warning` / `unknown` |
| Tag component | Fixed value | `tag`; "+N" is `tag-more` |
| Tag field and value | Special rule to avoid colliding with `tag` | `tag-field`, `tag-value` |
| Tooltip text box | `role="tooltip"` | — |
| Tooltip icon | `{owning element}-tooltip` | `port-field-tooltip` |
| Info box | `{title}-alert` | `upload-file-alert` |
| Tags input | Fixed value; options can't take a testid | `tags-select` |
| Badge (number or All) | Fixed value | `badge` |
| JSON viewer | Fixed value | `json-view` |
| Date Period | Fixed value | `date-period-select`, `date-period-option` |
| Date Picker | Use placeholder | `placeholder="Start date"` / `"End date"` |

---

## 7. Page templates (Base Pages)

### 7.1 List Page

| Element | testid |
|---|---|
| Page title | `page-title` |
| Table column header | `tc-title-{column}` |
| Table column content | `tc-{column}` |
| Row-end More icon | `more-button` |
| More menu options | `option-edit`, `option-start`, `option-stop`, `option-remove` |
| Export button | `{resource}-export-button` |
| Create button | `create-{resource}-button` or `add-{resource}-button` |

### 7.2 Detail Page

| Element | testid |
|---|---|
| Breadcrumb: asset type (link) | `breadcrumb-link` |
| Breadcrumb: asset name | `breadcrumb-name` |
| Back button | `back-icon-button` |
| Page title | `page-title` |
| Section title | `{section}-title`, e.g. `basic-info-title` |
| Section edit icon | `{section}-edit-button` |
| Field label / value | `{field}-field` / `{field}` |
| Tags label / value / single tag | `tags-field` / `tags` / `tag` |

### 7.3 Modal

Ant Design Modal containers can't reliably take a testid, so match their classes with `contains`:

| Modal type | Container | Title | Content |
|---|---|---|---|
| Normal Modal | `app-modal` | `ant-modal-title` | — |
| Warning Modal | `app-warning-modal` | `ant-modal-confirm-title` | `ant-modal-confirm-content` |
| Info Modal | `app-info-modal` | `ant-modal-confirm-title` | `ant-modal-confirm-content` |

Use one project prefix for these classes (this repo uses `dl-`). Fields inside a Modal still follow the normal rules: `provider-field`.

### 7.4 Other common structures

| Structure | Rule | Example |
|---|---|---|
| Tabs | `{name}-tab` | `overview-tab` |
| Step wizard | `step-{step action}` | `step-set-content` |
| Dashboard section | `{name}-area` | `activity-area` |
| Dashboard card | `meta-{name}-area`; inside the card `meta-title` / `meta-num` | `meta-members-area` |
| Generic elements inside a section | Fixed values, scoped by the outer `-area` | `title`, `info`, `info-list`, `total-num`, `status` |
| Header dropdown | `{name}-select` / `{name}-select-option` | `project-select-option` |
| Side menu | `{name}-menu-item` | `settings-menu-item` |

---

## 8. Scoping

The same testid **may** appear in different containers, e.g. `name-field` in several create / edit / import modals, `page-title` on every page, `title` and `info` in every dashboard section.

Rules:
1. In tests, **locate the container first** (`-area`, modal class, table row), then search inside it.
2. Only **globally unique** elements (Header, Menu) may be found directly by testid.
3. Table content `tc-*` appears in every row; combine it with a row index or other text in the row.

---

## 9. Exceptions and special rules

| Case | Handling | Reason |
|---|---|---|
| Tag field | Use `tag-field` / `tag-value` instead of `tag` | Collides with the Tag component's `tag` |
| Log list columns | Use specific names like `tc-event-type` | Deliberately avoids common words like `item`, `category` to lower future collisions |
| Notification list | Each item uses `{project_name}`; inside are `{type}`, `unread`, `event`, `date` | Projects must be distinguishable; `type` is `success` / `error` / `warning` / `info` |
| 2FA OTP input | Outer `otp`; the six boxes originally used `data-id` 0–5 | Removed in a later version; track the version |
| Table with hidden headers | Only label the content `tc-*`, not `tc-title-*` | There are no column headers on screen |
| Buttons with no testing need | Write "no testid needed" explicitly | So FE doesn't think it was forgotten |

---

## 10. Maintenance process

1. **One wiki page per screen**: the table columns are always `element | attribute | ref. | remark`.
2. **Reference shared rules**: write `REF: Elements`, `Base Pages` in the `ref.` column instead of redefining them.
3. **Status labels**: the `remark` column uses fixed labels:
   - `FE to add`: the spec is set, the frontend hasn't implemented it
   - `FE to fix`: implemented but doesn't follow the spec
   - `missing`: found missing during acceptance
   - `added / removed / to add in vX.Y`: changes tied to a version
4. **Sync with copy changes**: when an on-screen label is renamed, check whether the testid should change too (e.g. Email → Email address).
5. **Group by epic**: define shared components (epic) first, then each feature page (group1, group2).

---

## 11. Lessons learned

| Problem | Real case | Prevention |
|---|---|---|
| Inconsistent attribute name | Docs and code mixed `data_testid`, `date-testid` | Add a lint rule or CI scan that only allows `data-testid` |
| Typos | `tc-tiitle-member` | Script that compares the wiki and the testids in the source |
| Inconsistent synonyms | `back-icon-button` marked "should be unified" | Keep the suffix / prefix dictionaries; check them before naming |
| Generic words colliding | `tag` meant both the component and the field | Reserved-word list; add prefixes / suffixes to generic words |
| Version differences | A login button and an OTP input group were removed in later versions | Always write the version in remark; branch tests by version |
| FE forgot to add them | Several fields marked `FE to add` | Put testids on the PR checklist and in the acceptance criteria |
| Framework components can't take attributes | Modal, Tags Select options | Agree on the alternative locator up front and write it into the spec |
| Duplicate testids matched the wrong element | Several modals all have `name-field` | Always locate the container first (section 8) |

---

## 12. Porting to Android (Espresso / Compose)

### 12.1 Mapping

| Web | Android View + Espresso | Jetpack Compose |
|---|---|---|
| `data-testid` | `android:id` → `withId(R.id.xxx)` | `Modifier.testTag("xxx")` → `onNodeWithTag` |
| Locate by text | `withText("Confirm")` | `onNodeWithText("Confirm")` |
| `aria-label` | `contentDescription` → `withContentDescription` | `semantics { contentDescription = ... }` |
| `placeholder` | `android:hint` → `withHint` | `onNodeWithText` matching the placeholder |
| Locate the container first | `allOf(withId(..), isDescendantOfA(withId(..)))` | `onNode(hasTestTag(..) and hasAnyAncestor(..))` |
| Ant Design Modal class | `inRoot(isDialog())` + `withText` | `onNode(isDialog())` |
| Dropdown options | `inRoot(isPlatformPopup())`, `onData` | `onNodeWithTag` |
| Table rows `tc-*` | `RecyclerViewActions` + `hasDescendant` | `onAllNodesWithTag(..)[index]` |

### 12.2 Name conversion

Android resource names **can't contain `-`**, so the View system uses snake_case; every other rule stays the same:

| Web | Android View (`android:id`) | Compose (`testTag`) |
|---|---|---|
| `account-input` | `account_input` | `account-input` or `account_input` |
| `tc-title-server-name` | `tc_title_server_name` | Pick one, consistent project-wide |
| `option-edit` | `option_edit` | — |

Recommendation: use snake_case in Compose too, so both UI toolkits share one naming table.

### 12.3 Android-specific notes

1. **IDs must be unique within a layout**; they may repeat across layouts (e.g. every RecyclerView row has `tc_server_name`); scope tests with `isDescendantOfA` or `RecyclerViewActions`, otherwise you get `AmbiguousViewMatcherException`.
2. **Text locators must handle localization**: the web project could use English text directly; on Android with multiple languages, tests should use `withText(R.string.xxx)` instead of hard-coded strings.
3. **Toast and Snackbar** don't suit ids; use `withText` with the matching root matcher.
4. **Status indicators** should get a `contentDescription` (e.g. `status_running`), which serves both accessibility and testing.
5. The maintenance process in section 10 carries over as-is: one spec per screen, with implementation status and version in the `remark` column.
