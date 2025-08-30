# IMA – Multi-Tenant Identity & Access Management Service

IMA is a multi-tenant Identity & Access Management (IAM) service built with FastAPI and Postgres.  
It is being developed incrementally in **small, testable slices**. Each step is a checkpoint: add only what’s needed, verify, then move forward.

---

## Roadmap & Progress

### 1. Hello-World API + test ✅
- 📂 Project scaffolded with `app/` package and `main.py` entrypoint.
- 📝 Added `/v1/health` endpoint → returns `{"status": "ok"}`.
- 🧪 Wrote async test with `httpx.ASGITransport` + `AsyncClient`.
- ⚙️ Added `Makefile` with `make dev` (server) & `make test` (pytest).
- ✅ Definition of Done:
  - Server runs: `GET /v1/health` returns `{"status":"ok"}`.
  - Tests pass: `1 passed`.

### 2. Settings & Structured Logging 🚧
- Planned: Add `app/core/config.py` using `pydantic-settings`.
- Planned: Add `app/core/logging.py` with JSON logging via `python-json-logger`.
- Planned: Integrate settings + logging into app factory.

### 3. DB Engine (Postgres) + `/db-ping`
- Planned: Async SQLAlchemy/SQLModel engine.
- Planned: `/v1/db-ping` endpoint verifying DB connectivity.
- Planned: pytest covering DB ping.

### 4. Tenant Context (read `X-Org-ID`) + `/whoami`
- Planned: Middleware to read `X-Org-ID` header.
- Planned: `/v1/whoami` endpoint echoing org context.
- Planned: Tests for missing vs. present `X-Org-ID`.

### 5. Global Models: `User`, `Organization` (create org)
- Planned: Add global `User` + `Organization` models.
- Planned: `POST /orgs` endpoint → create new organization.
- Planned: `POST /users` endpoint → create new user.
- Planned: DB migrations for global schema.

### 6. Per-Tenant Schema on Org Creation
- Planned: Schema-per-tenant strategy (e.g., `tenant_acme`).
- Planned: Hook in `POST /orgs` to auto-create schema.
- Planned: Migration hook to keep schemas consistent.

### 7. Tenant Tables: `OrgUser`, `Membership`
- Planned: Add `OrgUser` + `Membership` models in tenant schema.
- Planned: Endpoint to list members in a tenant.
- Planned: Tests verifying tenant isolation.

### 8. Password Auth + JWT with `org_id` claim
- Planned: `/auth/register` & `/auth/login`.
- Planned: JWT tokens scoped with `org_id`.
- Planned: `/auth/refresh` & logout flow.

### 9. RBAC (owner/admin/member/viewer) + Guards
- Planned: Role-based access control.
- Planned: Guards (`require_role`) dependency for endpoints.
- Planned: Owner has full org-wide access; strict org isolation.

### Docarize and host in AWS/AZURE
---

## Core Goals

- Centralized identity across apps/services.
- Strong tenant isolation (org-scoped users, roles, policies).
- Standards-based authentication (OIDC/OAuth2, JWT rotation, MFA).
- Simple developer ergonomics (SDKs, as-code policies, clear docs).

---

## Progress Status

- ✅ Step 1-7 completed.
- 🚧 Step 8 in progress.
- ⏳ Steps 9–10 planned.
