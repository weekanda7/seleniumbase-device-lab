---
name: testid-spec
description: data-testid 命名規範（React + Ant Design）。在 frontend/src 新增或修改任何 UI 元素、或撰寫 SeleniumBase locator / Page Object 時使用，確保 testid 可推導、穩定、全專案一致。
---

# testid-spec

前端加 testid、或測試要找元素時，照這份做。完整規範（含案例、踩坑、Android 對照）在 `references/testid-spec.md`；這裡是精簡版 + 本 repo 的對照表。

## 1. 先決定要不要加 testid（定位優先順序）

| 優先 | 策略 | 用在 |
|---|---|---|
| 1 | `data-testid` | 表單欄位、表格欄位、icon button、選單、狀態燈號、**文字會變的按鈕** |
| 2 | 標籤 + 文字 | 文字固定的一般按鈕、錯誤訊息 |
| 3 | 語意屬性 | `aria-label`、`role="tooltip"`、`placeholder` |
| 4 | 框架 class（contains） | 無法注入屬性的第三方元件，例如 antd Modal |
| 5 | 不加 | 沒有測試需求的元素（在規範裡寫明「不需 testid」） |

本 repo 特例：**有 i18n 中英切換**，按鈕文字不穩定 → 會被點的按鈕一律加 testid。
紅色錯誤 Alert **不加** testid，測試用文字驗證（順便驗證文案；依當下語言比對）。

## 2. 命名格式

- 屬性名只能是 `data-testid`（不可 `data_testid`、`date-testid`）
- 全小寫、kebab-case、英文；主體取自畫面的英文標題：`Email address` → `email-address`
- 基本結構 `{主體}-{元件類型}`，少數類別用前綴（見第 4 節）
- 避免動態值；非用不可時寫明格式，例：`status-{state}`

## 3. 後綴字典

| 後綴 | 意義 | 例 |
|---|---|---|
| `-field` | 欄位**標題** | `name-field` |
| （無） | 欄位**唯讀值** | `location` |
| `-input` / `-textarea` | 輸入框 | `name-input` |
| `-select` / `-option` | antd Select 本體 / 其選項 | `type-select` / `type-option` |
| `-button` | 按鈕；純 icon 用 `-icon-button` | `save-button`、`back-icon-button` |
| `-edit-button` | 區塊標題旁的編輯圖示 | `basic-info-edit-button` |
| `-link` | 連結 | `breadcrumb-link` |
| `-checkbox` / `-radio` / `-switch` | 前面接標題或選項文字 | `online-radio`、`language-switch` |
| `-tab` / `-title` / `-alert` / `-area` / `-menu-item` | 分頁籤 / 區塊標題 / 說明框 / 容器 / 側邊選單 | `basic-info-title` |

**欄位三件組**：`{name}-field`（標題）、`{name}-input`（可編輯）、`{name}`（唯讀值）。

## 4. 前綴字典

| 前綴 | 意義 | 例 |
|---|---|---|
| `tc-title-` / `tc-` | 表格欄位標題 / 每列的欄位內容 | `tc-title-name` / `tc-name` |
| `option-` | antd **Dropdown**（動作選單）的選項 | `option-edit`、`option-remove` |
| `status-` | 狀態燈號 | `status-online`、`status-offline` |
| `breadcrumb-` | 導航列 | `breadcrumb-link`、`breadcrumb-name` |
| `step-` / `meta-` / `rank-` | 步驟精靈 / Dashboard 卡片 / 排行榜 | `step-completed` |

`-option`（Select 選項，屬於某欄位）≠ `option-`（Dropdown 選項，本身就是動作）。

## 5. 頁面模板

- **List**：`page-title`、`tc-title-{col}` / `tc-{col}`、列尾 `more-button` → `option-edit` / `option-remove`、`add-{資源}-button`、`total-num`
- **Detail**：`breadcrumb-link` / `breadcrumb-name`、`back-icon-button`、`page-title`、`{區塊}-title`、`{區塊}-edit-button`、欄位三件組
- **Modal**：antd Modal 容器加不了 testid → 用 `className` 定位（本 repo 前綴 `dl-`：`dl-warning-modal`），標題 / 內容用 `ant-modal-confirm-title` / `ant-modal-confirm-content`；裡面的欄位與按鈕照一般規則

## 6. 範圍限定（Scoping）

同一個 testid 可以在不同容器重複（`page-title` 每頁都有；`delete-button` 同時在詳細頁和確認 Modal）。
1. 先定位容器（Modal class、表格列、`-area`），再往內找
2. 只有全域唯一的元素（Header、`logout-button`、`language-switch`）可直接找
3. `tc-*` 每列都有：用列索引，或用列內文字找到列（`tr.ant-table-row` 含某文字）；antd 列另有 `data-row-key={id}`

### 6.1 CSS 還是 XPath（測試端，`tests/pages/common/elements.py`）

| 情況 | 用 | 例 |
|---|---|---|
| 單一元素、全域唯一或已在容器內 | `tid()`（CSS） | `tid("save-button")` |
| 要比對文字（選項、列） | `xtid(..., text=)`（XPath） | `xtid("status-option", text="Offline")` |
| 要先限定在某一列 / 容器再往內找 | `xtid()` 接在 XPath 後面 | `f"{row}{xtid('tc-location', tag='td')}"` |
| 只能用 class 的 antd 元件 | CSS class | `.ant-table .ant-spin-spinning` |

- CSS 和 XPath **不能串接**：locator 一旦以 XPath 開頭，後面一律用 `xtid()`
- 不全面改 XPath：XPath 比對 class 只能 `contains(@class, …)`，會誤中相似 class；可讀性也較差

## 7. antd 實作技巧（本 repo）

| 元件 | 怎麼加 | 測試注意 |
|---|---|---|
| `Input` / `Input.Password` / `Input.Search` | 直接 `data-testid`，會落在 `<input>` 上 | — |
| `Select` | `data-testid` 落在外層 `div.ant-select`；選項用 `optionRender` 包 `<span data-testid="{name}-option">` | **點外層 div**，點內部 input 會被 selection-item 擋；選項在 `<body>` 尾端的 portal |
| `Table` 欄位 | `onHeaderCell` / `onCell` 回傳 testid（`tc()` helper） | — |
| `Dropdown` 選項 | `label: <span data-testid="option-edit">` | 選單也在 portal |
| `Form.Item` 標題 | `label={<FieldLabel name="name">…</FieldLabel>}` → `name-field` | — |
| `Modal.confirm` 按鈕 | `okButtonProps: { ...testId("delete-button") }`（`testId()` 在 `src/api.ts`） | 先找 `.dl-warning-modal` 再找按鈕 |
| `message` toast | 不加 testid，加 `className: "toast-success"` / `"toast-error"` | 會自動消失：等出現就驗，不要 sleep |

## 8. 本 repo 對照表

| 頁面 | testid |
|---|---|
| 全域 Header | `id="logo"`、`language-switch`（`en-radio` / `zh-tw-radio`）、`logout-button` |
| Login | `page-title`、`username-field` / `username-input`、`password-field` / `password-input`、`login-button` |
| 裝置列表 | `page-title`、`add-device-button`、`search-input`、`status-select` / `status-option`、`total-num`、`tc-title-{name,type,status,location}` / `tc-{…}`、`more-button` → `option-edit` / `option-remove` |
| 新增 / 編輯 | `page-title`、`name-field` / `name-input`、`type-field` / `type-select` / `type-option`、`status-field` / `online-radio` / `offline-radio`、`location-field` / `location-input`、`save-button`、`cancel-button` |
| 裝置詳細 | `back-icon-button`、`breadcrumb-link` / `breadcrumb-name`、`page-title`、`delete-button`、`basic-info-title`、`basic-info-edit-button`、`{type,status,location,created}-field`、`type` / `location` / `created`、`status-online` / `status-offline` |
| 版本（登入頁、全站 Footer） | `version-area` → `web-version`、`api-version`（唯讀值，無後綴） |
| 刪除確認 Modal | `.dl-warning-modal` → `.ant-modal-confirm-title`、`delete-button`、`cancel-button` |

## 9. 新增 testid 的檢查清單

1. 先查第 3、4 節字典，有現成後綴 / 前綴就用，不要發明同義詞
2. 會撞名的通用詞（`tag`、`item`、`name`）加前後綴
3. 更新第 8 節對照表（這份就是 QA / FE 的契約）
4. 只用 `data-testid`：`grep -rnE "data_testid|date-testid" frontend/src` 應該沒有結果
5. `make -C frontend lint-check` 綠燈
