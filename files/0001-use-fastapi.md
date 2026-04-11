# ADR-0001: Use FastAPI over Flask

**Status:** Accepted
**Date:** 2026-04-11

## Context

Need a Python web framework for the REST API and read-only dashboard. The service does significant async I/O — database, LLM calls, Polymarket API, Playwright, notification fan-out. The contract with the CLI benefits from auto-generated OpenAPI. The project is for learning "real backend" Python, so embracing modern idioms (type hints, async, pydantic) is itself a goal.

## Decision

Use FastAPI.

## Alternatives considered

- **Flask.** Synchronous by default; async support is bolted on. No built-in validation — marshmallow or pydantic wired in separately. No auto-OpenAPI without extensions. Type hints are ignored by the framework. Fine for server-rendered HTML apps; weaker fit here.
- **Starlette directly.** Lower-level — reinventing pieces FastAPI already gives. No reason to do this unless actively avoiding FastAPI's magic.
- **Django.** Too heavy for an API-first service. Django REST Framework is solid but the rest of the Django machinery (admin, forms, templates) is not useful here.

## Consequences

- Async all the way down becomes a discipline: asyncpg, httpx, async Playwright, async SQLAlchemy. A blocking call inside an async route silently tanks performance.
- Pydantic v2 is load-bearing for request/response schemas.
- Auto-generated `/docs` (Swagger UI) and OpenAPI schema are free — the CLI can consume the schema or read it by hand.
- Type hints stop being decorative and start being checked by the framework itself.
