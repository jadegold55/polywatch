# Dev Log

Running record of work sessions. Newest at the top. Low ceremony — the point is to make context-switching back into the project painless after a break.

## How to use this file

- **One entry per work session.** Doesn't matter how short the session was.
- **Three things per entry:** what you did, what's next, what you're stuck on. That's it.
- **Write it at the end of the session**, not the start. Future-you will thank present-you when you come back after a week away and immediately know where you left off.
- **It's fine for "what's next" to be wrong later.** Don't edit old entries.

## Template

```
## YYYY-MM-DD

**Did:** …

**Next:** …

**Stuck on / questions:** …
```

---

<!-- Entries go below this line, newest first -->

## 2026-04-11

**Did:**
- Initial repo scaffold — `pyproject.toml` with full dep stack, `.gitignore`, `.pre-commit-config.yaml`, Dockerfiles, Terraform stubs, scripts, ADRs (0000–0015), architecture/plan docs, and src skeleton
- Added GitHub Actions workflows: `ci.yml` (lint → type-check → tests → docker build, security in parallel), `deploy-dev.yml` (push to Artifact Registry on merge to main), `deploy-prod.yml` (GCP deploy on semver tag with manual approval gate)
- Added `src/polywatch/config.py` — `Settings` class via `pydantic-settings`; also added `ignore_missing_imports` to mypy config so pre-commit passes without all deps installed locally
- Added Postgres service to `docker/docker-compose.yml`
- Added `src/polywatch/api/main.py` — FastAPI app instance with `GET /` and `GET /health` endpoints (entry point for all future routes)
- Added `src/polywatch/logger.py` — `structlog`-based `setup_logging()` and module-level `log` instance
- Opened PR #3 (`feat/fastapi`) documenting that this branch is where FastAPI will be configured

**Next:**
- Define routers and route modules under `src/polywatch/api/routes/`
- Wire up DB session dependency injection
- Add middleware (CORS, request ID, OpenTelemetry tracing)
- Implement lifespan events (startup/shutdown hooks)

**Stuck on / questions:** —
