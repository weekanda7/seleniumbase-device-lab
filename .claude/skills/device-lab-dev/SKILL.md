---
name: device-lab-dev
description: seleniumbase-device-lab 的開發規範（FastAPI 分層 + React/antd）。在 backend/ 或 frontend/ 新增、修改任何 feature、API、頁面、欄位前使用；含分層規則、contract-first 流程、REST 慣例、Definition of Done，以及現有 feature（登入、列表、新增、編輯、刪除、中英切換）的 Gherkin 驗收條件。
---

# device-lab-dev

改 app 之前先讀這份。每個 feature 的驗收條件（Gherkin）和改動點在 `references/features.md`；testid 命名看 `testid-spec` skill。

## 1. 架構

```
browser ──8080──> web (nginx) ──/api──> backend (FastAPI :8000) ──> db (Postgres :5433)
```

### 後端分層（backend/app/）

| 層 | 檔案 | 放什麼 | 不可以 |
|---|---|---|---|
| api | `api/routers.py`、`api/schemas.py` | HTTP：路由、Pydantic 驗證（→ 422）、auth 依賴、回應模型 | 寫 SQL、寫業務規則 |
| application | `application/*_service.py` | 業務規則（名稱唯一 → 409、找不到 → 404）、交易 commit | 碰 HTTP 物件（Request / status code） |
| domain | `domain/models.py`、`exceptions.py` | 資料定義（ORM model、列舉常數）、domain 例外 | import 其他層 |
| infrastructure | `infrastructure/*.py` | DB 連線、repository（所有 SQL） | 業務判斷 |

- 依賴方向只能往內：`api → application → infrastructure → domain`
- domain 例外 → HTTP 狀態碼只在 `main.py` 的 `_STATUS` 對照，**不在 service 裡寫狀態碼**
- service 自己 `commit()`；`get_db` 只負責開關 session（commit 放在 yield 之後會在回應送出後才失敗）

### 前端（frontend/src/）

| 位置 | 放什麼 |
|---|---|
| `api.ts` | 唯一呼叫 fetch 的地方：型別、token、`ApiError`、`testId()` |
| `pages/*Page.tsx` | 一個路由一個頁面；資料讀取 + 組畫面 |
| `pages/DeviceForm.tsx` | 新增 / 編輯共用表單（同一套驗證） |
| `components/` | 跨頁共用小元件（`StatusTag`、`LanguageSwitch`、`FieldLabel`） |
| `useDeleteDevice.ts` | 跨頁共用行為（確認 Modal + toast） |
| `i18n.ts` | 所有畫面文字（en / zh-TW 兩份，型別強制同結構） |
| `Root.tsx` / `App.tsx` | Provider（antd locale、theme、App）/ 路由與登入保護 |

- 畫面文字**一律**走 `t("…")`，不准寫死字串
- antd 的 message / modal 用 `App.useApp()` 取得（才吃得到 locale 和 theme），不要用靜態 `message.success`

## 2. 新增 / 修改 feature 的流程（contract-first）

1. **寫 AC**：在 `references/features.md` 加或改 Gherkin scenario（先寫「預期」，再寫 code）
2. **API 合約**：`schemas.py` 定義輸入 / 輸出；決定狀態碼（第 3 節）
3. **規則**：service 實作業務規則，新錯誤加到 `exceptions.py` + `main.py::_STATUS`
4. **資料**：model / repository；有 schema 變更看第 4 節
5. **路由**：`routers.py`，需要登入的掛在 `devices` router 下（自帶 `require_token`）
6. **前端 API**：`api.ts` 加型別和函式
7. **畫面**：頁面 / 元件；文字進 `i18n.ts`（**en 和 zh-TW 都要**）
8. **testid**：照 `testid-spec` 加，並更新它的第 8 節對照表
9. **驗證**：`make lint-check`、`make down && make up` 手動走過新加的 scenario
10. **commit**：一個 feature 一個 commit，訊息寫 feature 編號（例：`F4: allow renaming via PATCH`）

## 3. REST 慣例（RFC 9110 語意）

| 情況 | 狀態碼 | 本 repo 例子 |
|---|---|---|
| 讀取成功 | 200 | `GET /api/devices` |
| 建立成功 | 201 + 回傳新資源 | `POST /api/devices` |
| 更新成功 | 200 + 回傳更新後資源 | `PUT` / `PATCH /api/devices/{id}` |
| 刪除成功 | 204、無 body | `DELETE /api/devices/{id}` |
| 沒帶 / 錯誤 token、登入失敗 | 401 | `require_token`、`InvalidCredentials` |
| 資源不存在 | 404 | `DeviceNotFound` |
| 與現有資料衝突 | 409 | `DuplicateDeviceName` |
| 格式 / 欄位驗證失敗 | 422（FastAPI 自動） | 空名稱、未知 type、多餘欄位、PATCH 傳 null |

- **PUT = 全量取代**（沒給的選填欄位回到預設值）；**PATCH = 部分更新**（`model_dump(exclude_unset=True)`，只改有送的欄位）
- 輸入 schema 一律 `extra="forbid"`：多餘欄位回 422，不默默忽略
- 錯誤格式統一 `{"detail": "<message>"}`；422 是 FastAPI 的 list 格式，前端 `toMessage()` 已處理
- 列表篩選用 query string（`?q=&status=`），不用 POST body
- URL 用複數名詞、不放動詞：`/api/devices/{id}`，不是 `/api/deleteDevice`

## 4. DB 變更

- 目前沒有 migration：`create_all()` 只建新表，**不會改既有表** → 改 model 後要 `make down && make up`（會清資料、重灌 3 筆種子）
- 業界做法是 Alembic migration（待補）；在那之前，改 model 的 PR 描述要寫「需要 make down」
- 種子資料在 `seed.py`，只在空表時寫入；測試依賴這 3 筆，改它要同步改測試

## 5. Definition of Done

- [ ] `references/features.md` 的 scenario 有寫、跟實作一致
- [ ] 狀態碼符合第 3 節
- [ ] 文字 en / zh-TW 都有，切換語言畫面正常
- [ ] testid 符合 `testid-spec`、對照表已更新
- [ ] `make lint-check` 綠
- [ ] `make down && make up` 後手動走過新 scenario
- [ ] 分工：app 由 AI 寫；Page Object、測試、測資 fixture 由 Henry 自己寫（不要幫寫測試）

## 6. Feature 索引（細節在 references/features.md）

| ID | Feature | API | 頁面 |
|---|---|---|---|
| F1 | 登入 / 登出 | `POST /api/auth/login`、`/logout` | `/login`、Header |
| F2 | 裝置列表 | `GET /api/devices?q=&status=` | `/devices` |
| F3 | 新增裝置 | `POST /api/devices` | `/devices/new` |
| F4 | 編輯裝置 | `PATCH /api/devices/{id}`（PUT 只在 API） | `/devices/{id}/edit` |
| F5 | 刪除裝置 | `DELETE /api/devices/{id}` | 列表 More 選單、詳細頁 |
| F6 | 中英切換 | — | 全站 Header、登入頁 |
| F7 | 版本顯示 | `GET /api/version` | 登入頁、全站 Footer |
| — | 裝置詳細 | `GET /api/devices/{id}` | `/devices/{id}` |
