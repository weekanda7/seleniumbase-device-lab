# Triage rules v0

After the verdict (PASS / FAIL / BLOCKED / 🟡), classify **every step that is not PASS** in the order below. Start at category 1 and **stop at the first one that holds**; if none holds → unknown.

## Source of truth
- The **product spec** is the judge, not the GWT and not the app:
  - Scenarios and on-screen text: `.claude/skills/device-lab-dev/references/features.md` (Gherkin)
  - API: `http://localhost:8000/openapi.json`
  - testids: `.claude/skills/testid-spec/SKILL.md` (section 3 suffixes, section 8 mapping table)

## Categories (in order)
| Order | Category | Evidence required |
|---|---|---|
| 1 | Environment | The API returns **502 / 503 / 504** or can't be reached; confirm with `GET /api/version` (no login needed): if that fails too → environment |
| 2 | testid | Element not found; compare with testid-spec. Precondition: it should be there but isn't, and you are **not on a different page** (a different page means an earlier step broke the flow; keep going down the list) |
| 3 | Test bug | The test code or the GWT / spec is wrong or incomplete: **the app matches the product spec but the GWT doesn't**; or the GWT lacks information to run |
| 4 | Product bug | The check worked + **the app doesn't match the product spec** (quote the spec line); or **any API 500** |
| 5 | Unknown | None of the above holds, or the product spec doesn't cover it → hand it to a human |

## Allowed / not allowed while diagnosing
- Allowed: call APIs (including `/api/version`), read the product spec, query the DOM with `run_javascript` (`querySelectorAll`, current URL), look at screenshots
- Not allowed: change the verdict, modify any file, redo the app actions

## Report
Add two columns to every non-PASS step:
- **Cause**: environment / testid / test bug / product bug / unknown
- **Evidence**: one sentence + a citation (status code, the spec line, the DOM query result)
