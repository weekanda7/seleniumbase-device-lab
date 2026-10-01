# Test ID 命名規範（Test ID Spec）

> 來源：過去 Web 專案（React + Ant Design）的 QA testid wiki，共 21 頁（Elements、Base Pages、Modals、各功能頁）。
> 本文件把當時的規則、慣例與踩過的坑整理成可重用的規範，並在最後附上移植到 Android（Espresso / Compose）的對照。

---

## 1. 目的與原則

1. **測試定位要穩定**：不依賴 DOM 結構、CSS class 或排版位置，改版時測試不需跟著改。
2. **看名字就知道是什麼**：從 testid 能直接讀出「哪個欄位」和「什麼元件」。
3. **可推導、不需查表**：同一類元件用同一套規則，寫測試的人能直接推出 testid。
4. **QA 與 FE 共同維護**：規範由 QA 定義，FE 實作；每頁 wiki 是雙方的契約。

---

## 2. 定位策略優先順序

不是每個元素都要加 testid。依以下順序選擇：

| 優先 | 策略 | 適用情境 | 範例 |
|---|---|---|---|
| 1 | `data-testid` | 表單欄位、表格欄位、icon button、選單、狀態燈號等沒有穩定文字的元素 | `data-testid="login-button"` |
| 2 | 標籤 + 文字 | 有明確文字的一般按鈕、錯誤訊息 | `//button//*[text()="Confirm"]` |
| 3 | 語意屬性 | 無障礙屬性或元件原生屬性已足夠辨識 | `aria-label="Select all"`、`role="tooltip"`、`placeholder="Start date"` |
| 4 | UI 框架的 class（contains 比對） | 第三方元件無法加 testid 時（Ant Design Modal） | `contains(@class, "ant-modal-title")` |
| 5 | 不加 | 無測試需求的元素 | 「Download all」按鈕明確標註不需 testid |

**規則**
- 一般按鈕**優先用文字定位**；只有特殊情況（文字不穩定、重複、純 icon）才加 testid。
- 紅色錯誤訊息（Alert）**不加 testid**，直接用文字驗證，順便驗證了文案。
- 框架產生、無法注入屬性的元素（例如 Tags Select 的選項）要在 wiki 註明「無法加 testid」，並寫出替代定位方式。

---

## 3. 命名格式總則

| 項目 | 規則 |
|---|---|
| 屬性名稱 | 一律 `data-testid`（**不可**用 `data_testid`、`date-testid`） |
| 大小寫 | 全小寫 |
| 分隔符 | kebab-case（`-`） |
| 語言 | 英文，取自畫面上的英文標題 |
| 基本結構 | `{主體}-{元件類型}`，例：`account-input`、`siem-connection-switch` |
| 例外結構 | 少數類別使用**前綴**，例：`option-edit`、`tc-server-name`（見第 5 節） |
| 主體命名 | 依畫面上的標題文字轉成 kebab-case：`Email address` → `email-address` |
| 縮寫 | 可用常見縮寫，但全專案要一致：`web-app`、`app-info`、`ip` |
| 動態值 | 盡量避免；非用不可時寫明變數格式，例：`{project_name}`、`{type}` |

---

## 4. 後綴字典（Suffix）

| 後綴 | 意義 | 範例 |
|---|---|---|
| `-field` | 表單欄位的**標題（label）** | `password-field` |
| （無後綴） | 表單欄位的**唯讀內容值** | `credential-name`、`member-name` |
| `-input` | 文字輸入框 | `password-input` |
| `-textarea` | 多行輸入框 | `reason-textarea` |
| `-select` | 下拉選單本體 | `access-service-select` |
| `-option` | 下拉選單的選項（Select 類） | `access-service-option` |
| `-button` | 按鈕 / icon button | `back-icon-button`、`menu-button` |
| `-edit-button` | 區塊標題旁的編輯圖示 | `basic-info-edit-button` |
| `-export-button` | 列表頁匯出按鈕，前面加資源名稱 | `device-export-button` |
| `-link` | 連結 | `forgot-password-link` |
| `-checkbox` | 核取方塊，前面加其標題 | `case-sensitive-checkbox` |
| `-radio` | 單選按鈕，前面加其選項文字 | `linux-radio` |
| `-switch` | 開關 | `two-factor-authentication-switch` |
| `-tab` | 分頁籤 | `device-tab` |
| `-title` | 區塊 / 表單標題 | `basic-info-title` |
| `-alert` | 說明文字框（藍色或灰色描述） | `security-alert` |
| `-tooltip` | tooltip 觸發 icon，前面加所屬元素 | `new-password-field-tooltip` |
| `-area` | 一整個區塊容器 | `device-status-area` |
| `-label` | 附屬標籤文字 | `trust-this-browser-label` |
| `-img` | 圖片 | `cis-login-footer-img` |
| `-menu-item` | 側邊選單項目 | `audit-log-menu-item` |

**欄位三件組**是最常用的模式，一個表單欄位通常同時有：

```
{name}-field    → 欄位標題 "Account"
{name}-input    → 可編輯時的輸入框（或 -select / -textarea）
{name}          → 唯讀時顯示的值
```

---

## 5. 前綴字典（Prefix）

| 前綴 | 意義 | 範例 |
|---|---|---|
| `option-` | Dropdown 選單（動作選單、More 選單）的選項 | `option-edit`、`option-log-out` |
| `tc-title-` | 表格欄位**標題**（table column title） | `tc-title-server-name` |
| `tc-` | 表格欄位**內容**（每一列都會出現） | `tc-server-name` |
| `step-` | 多步驟精靈的每一步 | `step-select-target`、`step-completed` |
| `meta-` | Dashboard 卡片內的元素 | `meta-title`、`meta-num`、`meta-devices-area` |
| `status-` | 狀態燈號 | `status-running`、`status-stopped` |
| `rank-` | 排行榜元素 | `rank-title`、`rank-item-value` |
| `breadcrumb-` | 導航列 | `breadcrumb-link`、`breadcrumb-name` |

**`-option` 與 `option-` 的區別**
- Ant Design **Select**（表單下拉）→ 後綴 `-option`，因為選項屬於某個欄位：`ip-address-option`。
- Ant Design **Dropdown**（動作選單）→ 前綴 `option-`，因為選項本身就是動作：`option-remove`。

---

## 6. 共用元件規則（Elements）

| 元件 | 規則 | 範例 |
|---|---|---|
| Logo | 用 `id` | `id="logo"` |
| 錯誤訊息（紅色 Alert） | 不加，用文字驗證 | `//*[text()="..."]` |
| 一般按鈕 | 優先文字；特殊情況 `{文字}-button` | `connect-button` |
| Icon button | `{功能}-icon-button` 或 `{功能}-button` | `back-icon-button` |
| 全選 Checkbox | `aria-label="Select all"` | — |
| Checkbox | `{標題}-checkbox` | `exact-match-url-checkbox` |
| Radio（有文字） | `{文字}-radio` | `windows-radio` |
| Radio（無文字） | `{所屬項目}-radio` | `secret-radio` |
| Switch | `{標題}-switch` | `alert-switch` |
| Link | `{文字}-link` | `view-all-server-link` |
| 未讀紅點 | 固定值 | `unread`；閃動版 `flash-unread` |
| 狀態燈號 | `status-{狀態}` | `status-running` / `processing` / `stopped` / `warning` / `unknown` |
| Tag 元件 | 固定值 | `tag`；「+N」為 `tag-more` |
| Tag 的欄位與值 | 特規，避免與 `tag` 撞名 | `tag-field`、`tag-value` |
| Tooltip 文字框 | `role="tooltip"` | — |
| Tooltip icon | `{所屬元素}-tooltip` | `test-connection-field-tooltip` |
| 說明文字框 | `{標題}-alert` | `key-pair-file-alert` |
| Tags 輸入框 | 固定值；選項無法加 testid | `tags-select` |
| Badge（數字或 All） | 固定值 | `badge` |
| JSON 檢視區 | 固定值 | `json-view` |
| Date Period | 固定值 | `date-period-select`、`date-period-option` |
| Date Picker | 用 placeholder | `placeholder="Start date"` / `"End date"` |

---

## 7. 頁面模板（Base Pages）

### 7.1 List Page

| 元素 | testid |
|---|---|
| 頁面標題 | `page-title` |
| 表格欄位標題 | `tc-title-{欄位}` |
| 表格欄位內容 | `tc-{欄位}` |
| 列尾 More icon | `more-button` |
| More 選單選項 | `option-edit`、`option-start`、`option-stop`、`option-remove` |
| 匯出按鈕 | `{資源}-export-button` |
| 建立按鈕 | `create-{資源}-button` 或 `add-{資源}-button` |

### 7.2 Detail Page

| 元素 | testid |
|---|---|
| 導航列：資產類型（連結） | `breadcrumb-link` |
| 導航列：資產名稱 | `breadcrumb-name` |
| 返回按鈕 | `back-icon-button` |
| 頁面標題 | `page-title` |
| 區塊標題 | `{區塊}-title`，例 `basic-info-title` |
| 區塊編輯圖示 | `{區塊}-edit-button` |
| 欄位標題 / 內容 | `{欄位}-field` / `{欄位}` |
| Tag 標題 / 內容 / 單一 tag | `tags-field` / `tags` / `tag` |

### 7.3 Modal

Ant Design 的 Modal 容器無法穩定加 testid，改用 class 的 `contains` 比對：

| Modal 類型 | 容器 | 標題 | 內容 |
|---|---|---|---|
| 一般 Modal | `pt-modal` | `ant-modal-title` | — |
| Warning Modal | `pt-warning-modal` | `ant-modal-confirm-title` | `ant-modal-confirm-content` |
| Info Modal | `pt-info-modal` | `ant-modal-confirm-title` | `ant-modal-confirm-content` |

Modal 內的欄位仍照一般規則：`select-app-provider-field`。

### 7.4 其他常見結構

| 結構 | 規則 | 範例 |
|---|---|---|
| Tabs | `{名稱}-tab` | `connection-counts-tab` |
| 步驟精靈 | `step-{步驟動作}` | `step-set-secret-content` |
| Dashboard 區塊 | `{名稱}-area` | `connection-details-area` |
| Dashboard 卡片 | `meta-{名稱}-area`，卡片內 `meta-title` / `meta-num` | `meta-members-area` |
| 區塊內的通用元素 | 固定值，靠外層 `-area` 限定範圍 | `title`、`info`、`info-list`、`total-num`、`status` |
| Header 下拉 | `{名稱}-select` / `{名稱}-select-option` | `project-select-option` |
| 側邊選單 | `{名稱}-menu-item` | `system-policy-menu-item` |

---

## 8. 範圍限定（Scoping）

同一個 testid **可以**在不同容器重複出現，例如 `name-field` 出現在 Connect device / application / SFTP 三個 Modal，`page-title` 出現在每一頁，`title`、`info` 出現在每個 Dashboard 區塊。

使用規則：
1. 測試時**先定位容器**（`-area`、Modal class、表格列），再往內找元素。
2. 只有**全域唯一**的元素（Header、Menu）才可直接以 testid 查找。
3. 表格內容 `tc-*` 每列都有，要搭配列索引或列內其他文字定位。

---

## 9. 例外與特規

| 情況 | 處理 | 原因 |
|---|---|---|
| Tag 欄位 | 用 `tag-field` / `tag-value` 而非 `tag` | 與 Tag 元件的 `tag` 撞名 |
| 稽核日誌分類欄 | 用 `tc-classification`、`tc-substance` | 刻意避開 `item`、`category` 等常見詞，降低未來撞名機率 |
| Notification 列表 | 每個 item 用 `{project_name}`；內部為 `{type}`、`unread`、`event`、`date` | 需區分不同專案；`type` 為 `success` / `error` / `warning` / `info` |
| 2FA OTP 輸入框 | 外層 `otp`；六格原用 `data-id` 0–5 | 後續版本已移除，需追蹤版本 |
| 隱藏標題的表格 | 只標內容 `tc-*`，不標 `tc-title-*` | 畫面上沒有欄位標題 |
| 無測試需求的按鈕 | 明確寫「不需 testid」 | 避免 FE 誤以為漏加 |

---

## 10. 維護流程

1. **一頁一份 wiki**：表格欄位固定為 `element | attribute | ref. | remark`。
2. **共用規則用引用**：`ref.` 欄寫 `REF: Elements`、`Base Pages`，不重複定義。
3. **狀態標註**：`remark` 欄使用固定標籤：
   - `待FE補上`：規範已定，前端尚未實作
   - `待FE修改`：前端已實作但不符規範
   - `missing`：驗收時發現缺漏
   - `vX.Y 新增 / 刪除 / 要追加`：與版本綁定的變更
4. **文案變更同步**：畫面標題改名時，一併評估 testid 是否要改（例：Email → Email address）。
5. **以 Epic 分組**：共用元件（epic）先定，再做各功能頁（group1、group2）。

---

## 11. 踩過的坑（Lessons Learned）

| 問題 | 實際案例 | 預防方式 |
|---|---|---|
| 屬性名稱不一致 | 文件與實作混用 `data_testid`、`date-testid` | 加 lint 規則或 CI 掃描，只允許 `data-testid` |
| 拼字錯誤 | `tc-tiitle-member` | 用腳本比對 wiki 與原始碼中的 testid 清單 |
| 同義詞命名不一致 | `back-icon-button` 標註「應統一」 | 維護後綴 / 前綴字典，新名稱先查表 |
| 通用詞撞名 | `tag` 同時代表元件與欄位 | 保留字清單；通用詞加前後綴 |
| 版本差異 | LDAP 按鈕在 v1.14 移除、OTP 六格在 v1.11 移除 | remark 必寫版本；測試依版本分支 |
| FE 漏加 | 多個欄位標為 `待FE補上` | 把 testid 列入 PR checklist 與驗收條件 |
| 框架元件無法加屬性 | Modal、Tags Select 選項 | 事先約定替代定位法並寫入規範 |
| 重複 testid 導致誤抓 | 多個 Modal 都有 `name-field` | 強制先定位容器（第 8 節） |

---

## 12. 移植到 Android（Espresso / Compose）

### 12.1 對照表

| Web 做法 | Android View + Espresso | Jetpack Compose |
|---|---|---|
| `data-testid` | `android:id` → `withId(R.id.xxx)` | `Modifier.testTag("xxx")` → `onNodeWithTag` |
| 文字定位 | `withText("Confirm")` | `onNodeWithText("Confirm")` |
| `aria-label` | `contentDescription` → `withContentDescription` | `semantics { contentDescription = ... }` |
| `placeholder` | `android:hint` → `withHint` | `onNodeWithText` 比對 placeholder |
| 先定位容器 | `allOf(withId(..), isDescendantOfA(withId(..)))` | `onNode(hasTestTag(..) and hasAnyAncestor(..))` |
| Ant Design Modal class | `inRoot(isDialog())` + `withText` | `onNode(isDialog())` |
| 下拉選項 | `inRoot(isPlatformPopup())`、`onData` | `onNodeWithTag` |
| 表格列 `tc-*` | `RecyclerViewActions` + `hasDescendant` | `onAllNodesWithTag(..)[index]` |

### 12.2 命名轉換

Android resource 名稱**不能包含 `-`**，所以 View 系統改用 snake_case，其餘規則不變：

| Web | Android View（`android:id`） | Compose（`testTag`） |
|---|---|---|
| `account-input` | `account_input` | `account-input` 或 `account_input` |
| `tc-title-server-name` | `tc_title_server_name` | 同左擇一，全專案一致 |
| `option-edit` | `option_edit` | — |

建議：Compose 也統一用 snake_case，讓兩套 UI 共用同一份命名表。

### 12.3 Android 特有注意事項

1. **ID 在同一個 layout 內要唯一**；跨 layout 可重複（例如每個 RecyclerView row 都有 `tc_server_name`），測試時靠 `isDescendantOfA` 或 `RecyclerViewActions` 限定範圍，否則會丟出 `AmbiguousViewMatcherException`。
2. **文字定位要考慮多語系**：Web 專案可直接用英文文字，Android 若有多語系，測試應用 `withText(R.string.xxx)` 而不是寫死字串。
3. **Toast 與 Snackbar** 不適合用 id，改用 `withText` 並搭配對應的 root matcher。
4. **狀態燈號**建議加 `contentDescription`（如 `status_running`），同時兼顧無障礙與測試。
5. 第 10 節的維護流程可直接沿用：一個畫面一份規範、`remark` 欄標註實作狀態與版本。
