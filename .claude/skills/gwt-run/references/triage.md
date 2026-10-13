# 判因規則（triage）v0

判決（PASS / FAIL / BLOCKED / 🟡）之後，**每一個不是 PASS 的步驟**照下面的順序判斷原因。從第 1 類開始，**成立就停**；都不成立 → unknown。

## 裁判（source of truth）
- **產品 spec** 是裁判，不是 GWT，也不是 app：
  - 情境與畫面文字：`.claude/skills/device-lab-dev/references/features.md`（Gherkin）
  - API：`http://localhost:8000/openapi.json`
  - testid：`.claude/skills/testid-spec/SKILL.md`（第 3 節後綴、第 8 節對照表）

## 分類（照順序）
| 順序 | 類別 | 判斷依據（要有證據） |
|---|---|---|
| 1 | 環境 | API 回 **502 / 503 / 504** 或連不上；再打 `GET /api/version`（不用登入）確認，也失敗 → 環境 |
| 2 | testid | 元素找不到，對照 testid-spec。前提：該出現卻沒出現，而且**沒有停在別的頁面**（停在別頁 = 前一步流程壞了，往下判） |
| 3 | test bug | test code 或 GWT / spec 有錯、不足：**app 跟產品 spec 一致，GWT 不一致**；或 GWT 缺資訊跑不下去 |
| 4 | product bug | 檢查方法正常 + **app 跟產品 spec 不一致**（要引用 spec 那一行）；或**任何 API 500** |
| 5 | unknown | 以上都不成立，或產品 spec 沒寫到 → 交給人看 |

## 診斷時可以做 / 不可以做
- 可以：打 API（含 `/api/version`）、讀產品 spec、用 `run_javascript` 查 DOM（`querySelectorAll`、目前 URL）、看截圖
- 不可以：改判決結果、改任何檔案、重跑 app 的動作

## 回報
每個不是 PASS 的步驟加兩欄：
- **判因**：環境 / testid / test bug / product bug / unknown
- **證據**：一句話 + 引用（status code、spec 的那一行、DOM 查詢結果）
