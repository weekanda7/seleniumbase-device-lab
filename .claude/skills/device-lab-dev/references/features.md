# Features（Gherkin 驗收條件 + 改動點）

格式：每個 feature = **AC（Gherkin）→ 後端 → 前端 → 改動注意**。
Scenario 名稱就是測試名稱的來源（`test_<scenario snake_case>`），一個 scenario 對一個測試；
標 `@api` 的在 API 層測、`@ui` 在 SeleniumBase 測、`@db` 要直接查 Postgres 驗證。
背景資料：每次 `make down && make up` 後有 3 筆種子：
`core-router-01`（Router, online, Server room）、`office-switch-01`（Switch, online, 3F office）、`lobby-ap-01`（AP, offline, 1F lobby）。

---

## F1 登入 / 登出

```gherkin
Feature: Login and logout
  Only signed-in users can see or change devices.

  @ui @api
  Scenario: Log in with valid credentials
    Given I am on the login page
    When I log in with the configured username and password
    Then I am redirected to the device list

  @ui @api
  Scenario: Log in with a wrong password
    Given I am on the login page
    When I log in with a wrong password
    Then I stay on the login page
    And I see the error "Invalid username or password"
    And the API responds 401

  @ui
  Scenario: Required fields
    Given I am on the login page
    When I submit the form without a username or password
    Then each empty field shows its "required" message
    And no login request is sent

  @ui
  Scenario: Protected pages redirect to login
    Given I am not logged in
    When I open "/devices"
    Then I am redirected to "/login"

  @api
  Scenario: Device API without a token
    When I call GET /api/devices without an Authorization header
    Then the API responds 401

  @ui @api
  Scenario: Log out
    Given I am logged in
    When I click log out
    Then I am on the login page
    And my old token is rejected with 401
```

- **後端**：`auth_service.py`（帳密取自 `APP_USERNAME` / `APP_PASSWORD`；token 存在記憶體）、`routers.py::login / logout / require_token`
- **前端**：`LoginPage.tsx`、`api.ts::auth`（token 在 sessionStorage）、`App.tsx::ProtectedLayout`；任何 401（登入 API 除外）→ 清 token、導回 `/login`
- **改動注意**：token 在記憶體 → backend 重啟後全部失效、只能單一 worker；要多 worker 就改 JWT 或存 DB

---

## F2 裝置列表（搜尋、篩選、排序、分頁）

```gherkin
Feature: Device list
  Background:
    Given I am logged in with the 3 seed devices

  @ui @api
  Scenario: List all devices
    When I open the device list
    Then I see 3 devices
    And the total shows "3 devices"

  @ui @api
  Scenario: Search by name or location, case-insensitive
    When I search for "LOBBY"
    Then I only see "lobby-ap-01"
    When I search for "3f"
    Then I only see "office-switch-01"

  @ui
  Scenario: Search waits until typing stops
    When I type "lobby" quickly
    Then only one list request is sent, about 400 ms after the last key

  @ui @api
  Scenario: Filter by status
    When I filter by status "Offline"
    Then I only see "lobby-ap-01"
    When I clear the status filter
    Then I see 3 devices again

  @api
  Scenario: Invalid status filter
    When I call GET /api/devices?status=broken
    Then the API responds 422

  @ui
  Scenario: Sort by name and filter by type (client side)
    When I sort by name
    Then the rows are in alphabetical order
    When I filter the type column by "Switch"
    Then I only see "office-switch-01"

  @ui
  Scenario: Pagination
    Given there are 6 devices
    Then the first page shows 5 devices
    And the second page shows 1 device
```

- **後端**：`routers.py::list_devices`（`q` 最長 50、`status` 只能 online / offline）→ `repositories.py::list`（name / location `ILIKE`，依 id 排序）
- **前端**：`DeviceListPage.tsx`；搜尋與狀態篩選打 API，**排序、類型篩選、分頁在前端**（只處理已載入的資料）
- **改動注意**：資料量變大時要改成 server-side 分頁（`?page=&size=` + 回傳 total）；`q` 裡的 `%` / `_` 目前沒有跳脫，會被當萬用字元

---

## F3 新增裝置

```gherkin
Feature: Add a device
  Background:
    Given I am logged in

  @ui @api @db
  Scenario: Add a device
    When I add a device named "cam-01" of type "Sensor", status "Offline", location "B1"
    Then I see the toast "Device cam-01 created"
    And I am back on the device list with 4 devices
    And the API responds 201 with the new device
    And the devices table has a row named "cam-01"

  @ui @api @db
  Scenario: Duplicate name
    When I add a device named "lobby-ap-01"
    Then the name field shows "Device name 'lobby-ap-01' already exists"
    And the API responds 409
    And the devices table still has 3 rows

  @ui
  Scenario: Name is required
    When I save the form with an empty or whitespace-only name
    Then the name field shows "Please enter a device name"

  @api
  Scenario Outline: Invalid body
    When I POST /api/devices with <body>
    Then the API responds 422

    Examples:
      | body                                       |
      | {"name": "", "type": "AP"}                 |
      | {"name": "x", "type": "Phone"}             |
      | {"name": "x", "type": "AP", "color": "red"} |
      | a name longer than 50 characters           |
```

- **後端**：`schemas.py::DeviceCreate`（去頭尾空白、1–50 字、type 列舉、status 預設 online、`extra="forbid"`）→ `device_service.py::create_device`（先查重名 → 409；DB unique 約束擋同時送出的競態）
- **前端**：`DeviceNewPage.tsx` + `DeviceForm.tsx`；409 用 `form.setFields` 顯示在名稱欄位下，其他錯誤顯示紅色 Alert
- **改動注意**：加欄位要同時改 model、`DeviceCreate` / `DevicePatch` / `DeviceOut`、`api.ts` 型別、`DeviceForm`、i18n 兩份、testid，並 `make down`

---

## F4 編輯裝置

```gherkin
Feature: Edit a device
  Background:
    Given I am logged in

  @ui @api @db
  Scenario: Change the location
    Given a device "cam-01" exists
    When I edit "cam-01" and change the location to "B2"
    Then I see the toast "Device cam-01 updated"
    And the detail page shows location "B2"
    And the devices table row "cam-01" has location "B2"

  @ui @api
  Scenario: Rename to an existing name
    When I rename "core-router-01" to "lobby-ap-01"
    Then the name field shows the duplicate-name error
    And the API responds 409

  @api
  Scenario: PATCH only changes the fields sent
    When I PATCH a device with {"status": "offline"}
    Then only its status changes

  @api
  Scenario: PUT replaces the whole device
    When I PUT a device with only name and type
    Then its location becomes "" and its status becomes "online"

  @api
  Scenario: PATCH with null
    When I PATCH a device with {"name": null}
    Then the API responds 422

  @api
  Scenario: Update a missing device
    When I PUT or PATCH /api/devices/999999
    Then the API responds 404
```

- **後端**：`DeviceReplace`（PUT，全量）、`DevicePatch`（PATCH，只收有送的欄位、拒絕 null）→ `device_service.py::update_device`（改名才查重名）
- **前端**：`DeviceEditPage.tsx` 用 **PATCH** 送整份表單；成功後到詳細頁。入口：列表 More → Edit、詳細頁 Basic info 的編輯圖示
- **改動注意**：PUT 和 PATCH 的差別是面試常考點（冪等性：兩者都冪等，POST 不是），改的時候兩條 API scenario 都要保持綠

---

## F5 刪除裝置

```gherkin
Feature: Delete a device
  Background:
    Given I am logged in

  @ui @api @db
  Scenario: Delete from the detail page
    Given a device "cam-01" exists
    When I open "cam-01" and click delete
    And I confirm in the dialog
    Then I see the toast "Device cam-01 deleted"
    And I am back on the device list without "cam-01"
    And the API responds 204
    And the devices table has no row named "cam-01"

  @ui
  Scenario: Delete from the list's More menu
    When I choose "Delete" in the More menu of "lobby-ap-01" and confirm
    Then the list no longer shows "lobby-ap-01"

  @ui @db
  Scenario: Cancel the dialog
    When I click delete and then cancel
    Then the device is still listed and still in the database

  @api
  Scenario: Delete a missing device
    When I DELETE /api/devices/999999
    Then the API responds 404
```

- **後端**：`routers.py::delete_device` → `device_service.py::delete_device`（硬刪除）
- **前端**：`useDeleteDevice.ts`（`modal.confirm` + `message.success`），列表與詳細頁共用；Modal 用 `.dl-warning-modal` 定位
- **改動注意**：要改軟刪除（`deleted_at`）時，列表 / 取得 / 唯一約束都要一起改，並補 scenario

---

## F6 中英切換

```gherkin
Feature: Language switch
  @ui
  Scenario: Switch to Chinese
    Given I am on the device list in English
    When I choose "中文"
    Then the page title is "裝置"
    And antd's own texts (pagination, dialog buttons) are in Chinese

  @ui
  Scenario: The choice is remembered
    Given I chose "中文"
    When I reload the page
    Then the page is still in Chinese

  @ui
  Scenario: Available before login
    Given I am on the login page
    Then I can switch the language there too
```

- **後端**：無（API 錯誤訊息是英文；前端遇到 401 / 409 會換成翻譯文字）
- **前端**：`i18n.ts`（預設 en；選擇存在 localStorage）、`Root.tsx`（antd `ConfigProvider` locale 跟著切）、`LanguageSwitch.tsx`
- **改動注意**：zhTW 物件的型別是 `typeof en`，少一個 key 會編譯失敗；測試用文字驗證時要先確定語言（建議測試開頭固定切到 en）
