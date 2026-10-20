---
name: device-lab-dev
description: Development rules for seleniumbase-device-lab (layered FastAPI + React/antd). Use before adding or changing any feature, API, page or field in backend/ or frontend/; covers layering rules, the contract-first flow, REST conventions, the Definition of Done, and the Gherkin acceptance criteria for existing features (login, list, add, edit, delete, language switch).
---

> Entry index: `.claude/skills/index/SKILL.md` — where each kind of question is answered in this repo.

# device-lab-dev

Read this before changing the app. Each feature's acceptance criteria (Gherkin) and touch points are in `references/features.md`; testid naming is in the `testid-spec` skill.

## 1. Architecture

```
browser ──8080──> web (nginx) ──/api──> backend (FastAPI :8000) ──> db (Postgres :5433)
```

### Backend layers (backend/app/)

| Layer | Files | What goes here | Not allowed |
|---|---|---|---|
| api | `api/routers.py`, `api/schemas.py` | HTTP: routes, Pydantic validation (→ 422), auth dependencies, response models | SQL, business rules |
| application | `application/*_service.py` | Business rules (unique name → 409, not found → 404), transaction commit | Touching HTTP objects (Request / status code) |
| domain | `domain/models.py`, `exceptions.py` | Data definitions (ORM models, enum constants), domain exceptions | Importing other layers |
| infrastructure | `infrastructure/*.py` | DB connection, repositories (all SQL) | Business decisions |

- Dependencies only point inward: `api → application → infrastructure → domain`
- Domain exception → HTTP status mapping lives only in `_STATUS` in `main.py`; **never write status codes in a service**
- The service calls `commit()` itself; `get_db` only opens and closes the session (a commit after the yield would fail after the response is sent)

### Frontend (frontend/src/)

| Location | What goes here |
|---|---|
| `api.ts` | The only place that calls fetch: types, token, `ApiError`, `testId()` |
| `pages/*Page.tsx` | One page per route; data loading + layout |
| `pages/DeviceForm.tsx` | Shared add / edit form (same validation) |
| `components/` | Small cross-page components (`StatusTag`, `LanguageSwitch`, `FieldLabel`) |
| `useDeleteDevice.ts` | Shared cross-page behaviour (confirm modal + toast) |
| `i18n.ts` | All on-screen text (en / zh-TW, types force the same structure) |
| `Root.tsx` / `App.tsx` | Providers (antd locale, theme, App) / routes and login guard |

- On-screen text **always** goes through `t("…")`; no hard-coded strings
- Get antd message / modal from `App.useApp()` (so they pick up locale and theme); don't use the static `message.success`

## 2. Adding / changing a feature (contract-first)

1. **Write the AC**: add or change the Gherkin scenario in `references/features.md` (write the expectation before the code)
2. **API contract**: define input / output in `schemas.py`; choose status codes (section 3)
3. **Rules**: implement business rules in the service; add new errors to `exceptions.py` + `main.py::_STATUS`
4. **Data**: model / repository; for schema changes see section 4
5. **Routes**: `routers.py`; anything that needs login goes under the `devices` router (it carries `require_token`)
6. **Frontend API**: add types and functions to `api.ts`
7. **UI**: pages / components; text goes into `i18n.ts` (**both en and zh-TW**)
8. **testid**: add them per `testid-spec` and update its section 8 mapping table
9. **Verify**: `make lint-check`, then `make down && make up` and walk through the new scenario by hand
10. **Commit**: one commit per feature, message names the feature ID (e.g. `F4: allow renaming via PATCH`)

## 3. REST conventions (RFC 9110 semantics)

| Case | Status | Example in this repo |
|---|---|---|
| Read succeeded | 200 | `GET /api/devices` |
| Created | 201 + the new resource | `POST /api/devices` |
| Updated | 200 + the updated resource | `PUT` / `PATCH /api/devices/{id}` |
| Deleted | 204, no body | `DELETE /api/devices/{id}` |
| Missing / bad token, login failed | 401 | `require_token`, `InvalidCredentials` |
| Resource not found | 404 | `DeviceNotFound` |
| Conflicts with existing data | 409 | `DuplicateDeviceName` |
| Format / field validation failed | 422 (FastAPI automatic) | empty name, unknown type, extra fields, null in PATCH |

- **PUT = full replacement** (omitted optional fields go back to defaults); **PATCH = partial update** (`model_dump(exclude_unset=True)`, only the fields sent change)
- Input schemas always use `extra="forbid"`: extra fields return 422 instead of being silently ignored
- Errors always look like `{"detail": "<message>"}`; 422 uses FastAPI's list format, which the frontend `toMessage()` handles
- List filters use the query string (`?q=&status=`), not a POST body
- URLs use plural nouns and no verbs: `/api/devices/{id}`, not `/api/deleteDevice`

## 4. DB changes

- There are no migrations yet: `create_all()` only creates new tables and **does not alter existing ones** → after changing a model run `make down && make up` (wipes data, reloads the 3 seed rows)
- The industry approach is Alembic migrations (to do); until then, a PR that changes a model must say "needs make down"
- Seed data is in `seed.py` and is only written into an empty table; tests depend on those 3 rows, so change the tests along with it

## 5. Definition of Done

- [ ] The scenario in `references/features.md` is written and matches the implementation
- [ ] Status codes follow section 3
- [ ] Text exists in both en and zh-TW, and switching language works
- [ ] testids follow `testid-spec` and the mapping table is updated
- [ ] `make lint-check` is green
- [ ] After `make down && make up`, the new scenario was walked through by hand
- [ ] Ownership: AI writes the app; Henry writes the Page Objects, tests and test-data fixtures himself (don't write tests for him)

## 6. Feature index (details in references/features.md)

| ID | Feature | API | Page |
|---|---|---|---|
| F1 | Login / logout | `POST /api/auth/login`, `/logout` | `/login`, Header |
| F2 | Device list | `GET /api/devices?q=&status=` | `/devices` |
| F3 | Add device | `POST /api/devices` | `/devices/new` |
| F4 | Edit device | `PATCH /api/devices/{id}` (PUT is API only) | `/devices/{id}/edit` |
| F5 | Delete device | `DELETE /api/devices/{id}` | List More menu, detail page |
| F6 | Language switch | — | Site-wide Header, login page |
| F7 | Version display | `GET /api/version` | Login page, site-wide Footer |
| — | Device detail | `GET /api/devices/{id}` | `/devices/{id}` |
