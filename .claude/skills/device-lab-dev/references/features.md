# Features (Gherkin acceptance criteria + touch points)

> Entry index: `.claude/skills/index/SKILL.md` — where each kind of question is answered in this repo.

Format: each feature = **AC (Gherkin) → backend → frontend → change notes**.
The scenario name is the source of the test name (`test_<scenario snake_case>`), one scenario per test;
`@api` is tested at the API layer, `@ui` with SeleniumBase, `@db` by querying Postgres directly.
Background data: after every `make down && make up` there are 3 seed rows:
`core-router-01` (Router, online, Server room), `office-switch-01` (Switch, online, 3F office), `lobby-ap-01` (AP, offline, 1F lobby).

---

## F1 Login / logout

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

- **Backend**: `auth_service.py` (credentials from `APP_USERNAME` / `APP_PASSWORD`; tokens kept in memory), `routers.py::login / logout / require_token`
- **Frontend**: `LoginPage.tsx`, `api.ts::auth` (token in sessionStorage), `App.tsx::ProtectedLayout`; any 401 (except the login API) → clear the token, redirect to `/login`
- **Change notes**: tokens live in memory → all invalid after a backend restart, single worker only; for multiple workers switch to JWT or store them in the DB

---

## F2 Device list (search, filter, sort, pagination)

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

- **Backend**: `routers.py::list_devices` (`q` max 50, `status` only online / offline) → `repositories.py::list` (name / location `ILIKE`, ordered by id)
- **Frontend**: `DeviceListPage.tsx`; search and status filter call the API, **sorting, type filter and pagination happen in the frontend** (only on loaded data)
- **Change notes**: with more data, switch to server-side pagination (`?page=&size=` + return total); `%` / `_` in `q` are not escaped yet and act as wildcards

---

## F3 Add device

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

- **Backend**: `schemas.py::DeviceCreate` (trimmed, 1–50 chars, type enum, status defaults to online, `extra="forbid"`) → `device_service.py::create_device` (checks for a duplicate name first → 409; a DB unique constraint covers the concurrent-submit race)
- **Frontend**: `DeviceNewPage.tsx` + `DeviceForm.tsx`; a 409 is shown under the name field via `form.setFields`, other errors as a red Alert
- **Change notes**: adding a field means changing the model, `DeviceCreate` / `DevicePatch` / `DeviceOut`, the `api.ts` types, `DeviceForm`, both i18n sets and the testids, then `make down`

---

## F4 Edit device

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

- **Backend**: `DeviceReplace` (PUT, full), `DevicePatch` (PATCH, only fields sent, rejects null) → `device_service.py::update_device` (checks for duplicates only when renaming)
- **Frontend**: `DeviceEditPage.tsx` sends the whole form with **PATCH**; on success goes to the detail page. Entry points: list More → Edit, the Basic info edit icon on the detail page
- **Change notes**: PUT vs PATCH is a common interview question (idempotency: both are idempotent, POST isn't); keep both API scenarios green when changing them

---

## F5 Delete device

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

- **Backend**: `routers.py::delete_device` → `device_service.py::delete_device` (hard delete)
- **Frontend**: `useDeleteDevice.ts` (`modal.confirm` + `message.success`), shared by the list and the detail page; the modal is located via `.dl-warning-modal`
- **Change notes**: switching to soft delete (`deleted_at`) means changing list / get / the unique constraint together, and adding scenarios

---

## Device detail

```gherkin
Feature: Device detail
  Background:
    Given I am logged in

  @ui
  Scenario: Show device info
    Given a device "dt-01" exists with type "Switch", status "offline", location "B2"
    When I open its detail page
    Then the title and breadcrumb show "dt-01"
    And the type, status and location fields show "Switch", offline, "B2"
    # every field is checked with deferred asserts: one run reports all wrong fields

  @ui
  Scenario: Back to the list
    When I click the back button on the detail page
    Then I am on the device list

  @ui
  Scenario: Open edit from the detail page
    When I click the Basic info edit icon
    Then I am on /devices/{id}/edit
```

- **Frontend**: `DeviceDetailPage.tsx` (`GET /api/devices/{id}`); delete goes through F5's `useDeleteDevice.ts`
- **Tests**: `tests/cases/ui/test_device_detail.py` (F5's Delete from the detail page / Cancel the dialog live here too)

---

## F6 Language switch (English / Chinese)

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

- **Backend**: none (API error messages are English; the frontend replaces 401 / 409 with translated text)
- **Frontend**: `i18n.ts` (default en; choice stored in localStorage), `Root.tsx` (antd `ConfigProvider` locale follows), `LanguageSwitch.tsx`
- **Change notes**: the zhTW object is typed `typeof en`, so a missing key fails the build; tests that check text must pin the language first (switching to en at the start is recommended)

---

## F7 Version display

```gherkin
Feature: Version info
  @api
  Scenario: Version returns valid value
    When I GET /api/version without a token
    Then the status is 200
    And "version" looks like a git describe value (v0.1.0, v0.1.0-3-gabc1234, a short sha, or dev)
    And "commit" is a short git sha (or unknown)

  @ui
  Scenario: Web and API versions match
    Given I am on the login page
    Then the footer shows "Web <version> (<commit>) · API <version> (<commit>)"
    And the Web and API parts are the same
```

- **Backend**: `GET /api/version` (no login, like `/health`) → `VersionOut{version, commit}`, reads env `APP_VERSION` / `GIT_SHA` (Dockerfile `ARG` → `ENV`)
- **Frontend**: `components/VersionInfo.tsx`: the Web version is injected at build time (`VITE_APP_VERSION` / `VITE_GIT_SHA`), the API version comes from `/api/version`; shown on the login page and in the footer of the logged-in layout
- **Version source**: git tags only (`git describe --tags --always`). `make up`, CI and `images.yml` pass build args; a plain `docker compose up` shows `dev (unknown)`
- **Change notes**: tests are black-box and can't see the app's git → the API test checks the format; to verify an exact version, the deploy pipeline sets `EXPECTED_VERSION`
