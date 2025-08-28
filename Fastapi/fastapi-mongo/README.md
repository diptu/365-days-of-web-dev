
# 🚀 FastAPI + MongoDB App – Production Readiness Guide

This repo contains a FastAPI CRUD app with MongoDB.  
Before pushing to production, run through this checklist and validation runbook.

---

## ✅ Production Readiness Checklist

### 🔐 Security
- [x ] Secrets come from **env/secret manager** (no creds in code or Docker image).
- [ ] CORS locked to **known domains** (no `*` in prod).
- [ ] TLS/HTTPS enforced (redirects + HSTS).
- [ ] Security headers enabled: CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy.
- [ ] JWT auth configured with **expiry, rotation, scopes**.
- [ ] Rate limit on sensitive endpoints (login, OTP).
- [ ] Request size limits + timeouts defined.

### 🗄️ Data & Database
- [ ] Indexes validated with `explain()` on all hot queries.
- [ ] Compound indexes for filter + sort queries.
- [ ] Schema versioning documented.
- [ ] Write concern set to **majority** for critical writes.
- [ ] TTL indexes for short-lived data (sessions, OTPs).
- [ ] Automated backups scheduled + **restore tested**.

### 📜 API Contract
- [ ] Pagination uses **cursor/keyset** (not skip/limit).
- [ ] Consistent error format: `{error: {code, message, details}}`.
- [ ] OpenAPI spec reviewed + published.
- [ ] Deprecated endpoints marked with **Deprecation header** + removal plan.

### 👀 Observability
- [ ] Structured JSON logs with request ID, user ID, trace IDs.
- [ ] Metrics: latency buckets, error rates, cache hits, DB latency.
- [ ] Distributed tracing enabled (OpenTelemetry).
- [ ] Dashboards ready (latency, RPS, error rate).
- [ ] Alerts wired (errors > X%, p95 latency, 429 spikes).

### ⚙️ Reliability
- [ ] POST endpoints support **Idempotency-Key**.
- [ ] Timeouts + retries with jitter on external calls.
- [ ] Circuit breaker tested for DB/Redis outages.
- [ ] Blue-green or canary deployment strategy in place.
- [ ] Readiness probes reflect downstream health.

### 🐳 Docker & Deployment
- [ ] Multi-stage Docker build (slim base image).
- [ ] Container runs as **non-root**.
- [ ] HEALTHCHECK baked into Dockerfile.
- [ ] Config via env only (no baked-in creds).
- [ ] Rollback procedure documented.
- [ ] Infra reproducible (Terraform / Bicep / K8s).

### 🧪 Testing & Quality Gates
- [ ] Unit, integration, and smoke tests pass.
- [ ] Coverage ≥ 80% (pytest-cov).
- [ ] Static checks clean: ruff/flake8, mypy, bandit.
- [ ] Dependencies scanned (pip-audit, Snyk).
- [ ] Load tests run at peak QPS + 20% headroom, p95 < SLA.
- [ ] Chaos test: DB/Redis failure degrades gracefully.

---

## 🚀 Pre-Production Validation Runbook

### Step 1 — Environment Prep
- Deploy to **staging** with production-like infra (DB, Redis).
- Apply same config: env, secrets, TLS certs.

### Step 2 — Smoke Tests
- `/health` → 200 OK.
- `/ping-db` → 200 OK.
- Run a CRUD cycle (create → read → update → delete).

### Step 3 — Functional Checks
- Pagination returns stable cursor + order.
- Rate limiting returns `429` after limit.
- JWT flow works: login → access token → refresh token → scope check.
- OTP flow works: valid accepted, invalid blocked.

### Step 4 — Non-Functional Checks
- Run load test (k6/Locust) at target RPS + 20% margin.
- Monitor DB CPU/memory/index usage.
- Cache hit ratio ≥ target.
- Kill Redis → app degrades gracefully.
- Kill DB → readiness probe flips unhealthy within 5s.

### Step 5 — Observability & Alerts
- Logs include request IDs + correlation IDs.
- Metrics visible (latency, error, 429).
- Trigger error → alert fires.

### Step 6 — Rollout Drill
- Deploy new version to **10% canary** traffic.
- Monitor error/latency dashboards for 10 mins.
- Trigger rollback → previous version restores cleanly.

---

## 📝 Notes
- Keep `.env.example` under version control, never `.env` with secrets.
- Automate as many checks as possible in CI/CD.
- Treat this doc as a **living checklist** — update as your system grows.

---

Happy shipping! 🚀
