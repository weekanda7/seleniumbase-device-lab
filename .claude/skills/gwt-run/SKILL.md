---
name: gwt-run
description: Run the Given / When / Then in a testcase docstring once against the local device-lab app through the seleniumbase MCP, and report pass / fail per step. Use only when the user types /gwt-run <pytest node id>.
disable-model-invocation: true
argument-hint: tests/cases/ui/test_xxx.py::Class::test_name [--debug]
---

> Entry index: `.claude/skills/index/SKILL.md` — where each kind of question is answered in this repo.

# gwt-run (POC v0)

Case to run: `$ARGUMENTS` (if it ends with `--debug`, turn on debug mode, see below)

## Prerequisites
- The app is already up via `make up`: UI http://localhost:8080 (nginx, forwards `/api` to the backend)
- Credentials: admin / admin123
- Drive the browser only with the seleniumbase MCP tools

## Steps
1. **Read the spec**: open the file `$ARGUMENTS` points to and **read only that test's docstring**, not the test code (the POC checks whether the spec alone is complete). If the docstring is missing information, stop and report what is missing.
2. **Generate dynamic values**: when the docstring says `{name} = uuid_name("test")`, generate `test-` + 8 lowercase hex characters yourself and use the same value for the whole case.
3. **Open the browser**: `start_browser` → `open_url` http://localhost:8080. If it doesn't load, report "environment: app is not up" and stop.
4. **Look up the API spec**: when the GWT mentions an API (e.g. `POST /api/devices`), first run `curl -s http://localhost:8000/openapi.json` to get the request body fields, required fields, enums and defaults.
   - **Value rules** (so every run behaves the same): use values written in the GWT as-is; for fields the GWT doesn't mention, use the default if there is one; for a required field with no default, use the **first** enum value. The UI form follows the same rules.
5. **Given**: steps with an API in parentheses are done through the API, not the UI:
   - On the 8080 page, run `fetch('/api/...')` with `run_javascript` (same origin, no CORS)
   - Login: `POST /api/auth/login`, body `{"username":"admin","password":"admin123"}` → write the `access_token` from the response into **sessionStorage** with `manage_storage`, key `device-lab-token`
   - Other API calls send the header `Authorization: Bearer <token>`; record the ids of devices you create (step 8 deletes them)
   - **`run_javascript` does not await Promises** (it returns `{}`). Fixed pattern: first call `fetch(...).then(r => r.text().then(t => window.__gwt = r.status + ' ' + t))`, then a second `run_javascript` reads `window.__gwt`. Set `window.__gwt = null` before every fetch; send the two calls **in order, never in parallel**; if you read null the response hasn't arrived yet, read again
   - `window` is cleared on navigation: always read the token from `sessionStorage.getItem('device-lab-token')`, never keep it on window
6. **When**: perform the UI actions literally. Find elements by `data-testid`, see [testid-spec](../testid-spec/SKILL.md):
   - **Section 3, suffix dictionary**: what each suffix means (e.g. `-field` is the field **label**, not the whole field; `-input` is the editable element)
   - **Section 8, mapping table**: which testids each page has
   - Field validation messages have no testid; use the **single-level** selector `#device_{field}_help` (e.g. `#device_name_help`; its text is the error message). The seleniumbase MCP tools don't accept descendant selectors with a space (`A B`)
   - antd dropdown options render in a portal at the end of `<body>`
7. **Then**: check each Then / And line once, **with a fixed method** (don't use `assert_condition`, and don't switch methods):
   - **On-screen text**: `wait_for_condition` until the element appears (up to 10 s) → run `sleep 1` in the shell (lets antd's enter animation finish; the element is re-rendered while it animates) → `get_content` to read its text → trim, collapse repeated whitespace → must **equal** the expected text exactly
   - **URL**: `get_page_info` for the current URL → compare the path
   - **API result**: call the API with the fixed pattern from step 5 → compare status and content
   - Element never appears → BLOCKED; element read but text differs → FAIL
   - **Screenshot fallback**: when a step is BLOCKED, take a screenshot with `save_page`, then open the png with Read. If the screenshot shows the expected result → mark 🟡 PASS (screenshot) and write what you saw in the image; if not, or unsure → keep BLOCKED. Exact text (quotes, whitespace, look-alike characters) is decided by the fixed method; a screenshot is only supporting evidence
   - Record expected and actual. After all checks take one screenshot with `save_page`; if something fails midway, screenshot first, then report.
8. **Clean up**: delete the devices created in this run with `DELETE /api/devices/{id}` (always, pass or fail), then `close_browser`.

## Verdict rules
Each step is exactly one of:
- ✅ **PASS**: behaviour matches the expectation
- ❌ **FAIL**: **behaviour** doesn't match (the screen / API value differs from the expectation)
- ⚠️ **BLOCKED**: the **check itself** has a problem (element not found, unclear spec), so the behaviour can't be confirmed; apart from the screenshot fallback below, don't switch to another method to decide PASS or FAIL
- 🟡 **PASS (screenshot)**: the fixed method was BLOCKED but the screenshot shows the expected result (lower confidence, supporting evidence only)

**Triage**: if any step is not PASS, read [references/triage.md](references/triage.md) and classify every non-PASS step in its order, with evidence.

Overall result: all PASS → PASS; any FAIL → FAIL; no FAIL but any BLOCKED or 🟡 → BLOCKED (🟡 doesn't count as PASS; it only tells a human "the app is probably fine, the check is what broke").

## Rules
- Don't modify any file (except the debug mode log)
- Don't retry the app's results, don't guess causes, don't change steps; record what you actually saw
- If your own JS breaks (syntax, missing variable) you may fix it and send it again; say so in the report
- Every step must map to a line in the docstring

## Debug mode (`--debug`)
Goal: a later QA or AI agent can understand what happened without rerunning.
- For every step that is **not PASS** (FAIL / BLOCKED / 🟡), record at that moment:
  1. Time (HH:MM:SS) and the GWT line for the step
  2. Which tool, its full arguments (selector, timeout), and the **raw return value / error message** (don't paraphrase)
  3. The current URL (`get_page_info`)
  4. Diagnostic DOM: run `document.querySelectorAll('<same selector>')` with `run_javascript` and record the count and the first element's parent `outerHTML` (up to 2000 characters). **For the record only; never use it to change the verdict**
  5. Screenshot path; if you looked at the screenshot, what you saw
  6. Your guess at the cause (label it "guess, not verified")
- Also log any time your own JS had to be fixed and resent
- Screenshots and logs go in `report/gwt/`: the MCP server's working directory is `tests/`, so pass `report/gwt` as the `save_page` folder (not `tests/report/gwt`)
- At the end write the file `tests/report/gwt/<test name>-<YYYYMMDD-HHMMSS>.md` (already in .gitignore) and add its path to the report
- Without `--debug`, don't record any of this

## Report format (shown in the conversation only)
| # | GWT line | Result | Expected | Actual | Cause | Evidence |
|---|---|---|---|---|---|---|
| 1 | Given I am logged in… | ✅ | … | … | — | — |

Then one line, **Values I filled in**: fields and values added by the value rules (e.g. `type=Router (first enum value)`).

Last line: `Result: PASS` / `Result: FAIL (step n)` / `Result: BLOCKED (step n)`, plus the screenshot path and the `{name}` used; in debug mode also the log path.
