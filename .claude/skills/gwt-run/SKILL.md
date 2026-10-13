---
name: gwt-run
description: 照 testcase docstring 裡的 Given / When / Then，透過 seleniumbase MCP 在本機 device-lab 跑一次並逐步回報 pass / fail。只在使用者輸入 /gwt-run <pytest node id> 時使用。
disable-model-invocation: true
argument-hint: tests/cases/ui/test_xxx.py::Class::test_name [--debug]
---

# gwt-run（POC v0）

要跑的 case：`$ARGUMENTS`（最後有 `--debug` 就開 debug mode，見下方）

## 前提
- app 已經用 `make up` 起好：UI http://localhost:8080（nginx，`/api` 轉給 backend）
- 帳密：admin / admin123
- 只用 seleniumbase MCP 的 tool 操作瀏覽器

## 步驟
1. **讀 spec**：打開 `$ARGUMENTS` 指到的檔案，**只讀那個 test 的 docstring**，不要看 test 的程式碼（POC 要驗證 spec 本身夠不夠完整）。docstring 資訊不足時先停下來，回報缺什麼。
2. **產生動態值**：docstring 寫 `{name} = uuid_name("test")` → 自己產生 `test-` + 8 碼小寫 hex，整個 case 都用同一個值。
3. **開瀏覽器**：`start_browser` → `open_url` http://localhost:8080 。打不開就直接回報「環境：app 沒起來」，不要繼續。
4. **查 API spec**：GWT 提到 API（例如 `POST /api/devices`）時，先 `curl -s http://localhost:8000/openapi.json` 查 request body 的欄位、必填、enum、default。
   - **選值規則**（讓每次跑結果一致）：GWT 有寫的值照寫；沒寫的欄位有 default 就用 default；必填沒 default → 用 enum **第一個**值。UI 表單也照同一套規則。
5. **Given**：括號裡有寫 API 的步驟，用 API 做，不走 UI：
   - 在 8080 頁面上用 `run_javascript` 執行 `fetch('/api/...')`（同源，不會有 CORS）
   - 登入：`POST /api/auth/login`，body `{"username":"admin","password":"admin123"}` → 回應的 `access_token` 用 `manage_storage` 寫進 **sessionStorage**，key 是 `device-lab-token`
   - 其他 API 帶 header `Authorization: Bearer <token>`；記下建立出來的裝置 id（第 8 步要刪）
   - **`run_javascript` 不會等 Promise**（直接回 `{}`）。固定寫法：第一次 `fetch(...).then(r => r.text().then(t => window.__gwt = r.status + ' ' + t))`，第二次 `run_javascript` 讀 `window.__gwt`。每次 fetch 前先設 `window.__gwt = null`；兩個呼叫**依序送、不要平行**；讀到 null 代表還沒回來，再讀一次
   - 換頁後 `window` 會清空：token 一律從 `sessionStorage.getItem('device-lab-token')` 讀，不要存在 window
6. **When**：照字面用 UI 操作。元素用 `data-testid` 找，看 [testid-spec](../testid-spec/SKILL.md)：
   - **第 3 節後綴字典**：後綴代表什麼（例：`-field` 是欄位**標題**，不是整個欄位；`-input` 才是可輸入的元素）
   - **第 8 節對照表**：每頁有哪些 testid
   - 欄位的驗證錯誤訊息沒有 testid，用**單一層** selector `#device_{欄位}_help`（例：`#device_name_help`，裡面的文字就是錯誤訊息）。seleniumbase MCP 的 tool 不吃有空白的後代 selector（`A B`）
   - antd 下拉選項在 `<body>` 最後面的 portal 裡
7. **Then**：每一行 Then / And 各做一次檢查，**檢查方法固定**（不要用 `assert_condition`，也不要換別的方法）：
   - **畫面文字**：`wait_for_condition` 等元素出現（最多 10 秒）→ `get_content` 讀該元素文字 → 去掉前後空白、連續空白合成一個 → 跟預期**完全相等**
   - **網址**：`get_page_info` 讀目前 URL → 比對路徑
   - **API 結果**：照第 5 步的固定寫法打 API → 比對 status 和內容
   - 等不到元素 → 這步 BLOCKED；讀到了但文字不同 → FAIL
   - **截圖備案**：這步 BLOCKED 時，先 `save_page` 截圖，再用 Read 打開 png 看。截圖上看得到預期結果 → 標 🟡 PASS（截圖），並寫出你在圖上看到什麼；看不到或不確定 → 維持 BLOCKED。精確文字（引號、空白、相似字元）以固定方法為準，截圖只能當旁證
   - 記下預期和實際。全部檢查完用 `save_page` 截一張圖；中途出錯也先截圖再回報。
8. **清理**：用 API `DELETE /api/devices/{id}` 刪掉這次建立的裝置（不管 pass / fail 都要做），最後 `close_browser`。

## 判決規則
每一步只能是三種之一：
- ✅ **PASS**：行為符合預期
- ❌ **FAIL**：**行為**不符合預期（畫面 / API 回的值跟預期不同）
- ⚠️ **BLOCKED**：**檢查方式**有問題（元素找不到、spec 不清楚），無法確認行為對不對；除了下面的截圖備案，不要自己改用別的方式判 PASS 或 FAIL
- 🟡 **PASS（截圖）**：固定方法 BLOCKED，但截圖上看得到預期結果（可信度較低，只當旁證）

**判因**：有任何一步不是 PASS，就讀 [references/triage.md](references/triage.md)，照它的順序替每個非 PASS 步驟判因並附證據。

總結果：全部 PASS → PASS；有 FAIL → FAIL；沒有 FAIL 但有 BLOCKED 或 🟡 → BLOCKED（🟡 不算 PASS，只是告訴人「app 大概是對的，壞的是檢查方式」）。

## 規則
- 不修改任何檔案（debug mode 的 log 檔除外）
- app 的結果不重試、不猜原因、不自己改步驟；照實記錄實際看到的值
- 自己寫的 JS 出錯（語法、變數不見）可以修正後再送一次，回報裡註明
- 每一步都要對應到 docstring 的某一行

## Debug mode（`--debug`）
目的：讓之後的 QA 或 AI agent 不用重跑，就能看懂當時發生什麼。
- 每一個**不是 PASS** 的步驟（FAIL / BLOCKED / 🟡），當下記錄：
  1. 時間（HH:MM:SS）、這步對應的 GWT 行
  2. 用了哪個 tool、完整參數（selector、timeout）、**原始回傳 / 錯誤訊息**（不要改寫）
  3. 當時的 URL（`get_page_info`）
  4. 診斷用 DOM：`run_javascript` 執行 `document.querySelectorAll('<同一個 selector>')` 的數量，和第一個元素父層的 `outerHTML`（最多 2000 字）。**只用來記錄，不能拿來改判決**
  5. 截圖路徑；有看截圖的話，寫看到什麼
  6. 你對原因的推測（標明「推測，未查證」）
- 自己的 JS 出錯重送，也記一筆
- 截圖和 log 都放 `report/gwt/`：MCP server 的工作目錄是 `tests/`，所以 `save_page` 的 folder 寫 `report/gwt`（不要寫 `tests/report/gwt`）
- 結束時寫成檔案：`tests/report/gwt/<test 名稱>-<YYYYMMDD-HHMMSS>.md`（已在 .gitignore），回報最後附上路徑
- 沒有 `--debug` 就不記錄這些

## 回報格式（只在對話裡顯示）
| # | GWT 行 | 結果 | 預期 | 實際 | 判因 | 證據 |
|---|---|---|---|---|---|---|
| 1 | Given 已登入… | ✅ | … | … | — | — |

再列一行「**自己補的值**」：照選值規則補上的欄位和值（例：`type=Router（enum 第一個）`）。

最後一行：`結果：PASS` / `結果：FAIL（第 n 步）` / `結果：BLOCKED（第 n 步）`，加上截圖路徑和這次用的 `{name}`；debug mode 再附 log 檔路徑。
