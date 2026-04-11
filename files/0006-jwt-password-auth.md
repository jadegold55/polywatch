# ADR-0006: Multi-user with JWT + password login

**Status:** Accepted
**Date:** 2026-04-11

## Context

The project is for learning "real backend" Python. A realistic auth surface is part of that. The system needs to distinguish users so the curator reads the right interests and notifications go to the right channels. No real users will exist in production — this is a learning exercise — but the auth should work the way a real system's auth would.

## Decision

Multi-user from day one. Email + password. Passwords hashed with argon2. Access tokens as short-TTL JWTs. Refresh tokens stored in the database to allow revocation.

## Alternatives considered

- **Single-user (no auth at all).** Trivial, teaches nothing about auth. Rejected.
- **API keys only.** Each user gets a long random token they put in a header. ~20 lines of code. A cop-out for learning purposes — skips the interesting parts (password storage, token lifecycle, refresh, revocation).
- **OAuth with Google/GitHub.** More realistic for real apps but a rabbit hole of redirect flows, client registration, and provider-specific quirks. Not what this project is about.

## Consequences

- Real auth surface to build and test. Register endpoint, login endpoint, refresh endpoint, logout (revocation) endpoint.
- `get_current_user` FastAPI dependency gates all authenticated routes.
- JWT signing secret lives in Secret Manager in cloud, in a k8s Secret locally.
- Password reset flow is *not* in scope for v1 — it requires email sending infrastructure just for this, which is out of proportion for a learning project.
- All permission checks must be explicit: user A must not be able to read user B's interests or notifications. Integration tests enforce this.
