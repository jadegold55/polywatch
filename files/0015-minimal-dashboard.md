# ADR-0015: Minimal read-only dashboard; CLI is the primary client

**Status:** Accepted
**Date:** 2026-04-11

## Context

Users need to see their watchlist (what the curator picked and why), their notification history, and ideally the investigator's reasoning trace for each notification. This can live in a full web app, a minimal dashboard, a CLI, or some combination.

## Decision

- **CLI** handles all *management*: register, login, set interests, configure notification channels, inspect state.
- **Minimal read-only HTML dashboard**, rendered server-side with Jinja templates inside the FastAPI app, provides visual views of the watchlist, notification list, and individual notification detail with reasoning trace. No JavaScript framework. Three to four routes.

## Alternatives considered

- **Full SPA frontend (React/Vue/Svelte).** A whole separate project. Not justified by the learning goals of the backend-focused plan.
- **CLI only, no dashboard at all.** Works, but makes casual state inspection annoying. Looking at a long reasoning trace is better in HTML than in a terminal.
- **Full web app with write operations.** Would need forms, CSRF, session management — a separate set of concerns from the JWT API. Rejected for scope.

## Consequences

- The dashboard is ~200 lines of templates plus three to four FastAPI routes. Low-cost to build.
- The CLI remains the primary management interface — everything you can do, you can do from the terminal.
- A real web frontend is a v2 decision, not blocked by this one. Nothing in the current design prevents adding one later.
- Dashboard routes are also JWT-gated (via cookie-stored token or basic auth, decided during implementation).
