# ADR-0002: Postgres as the sole datastore

**Status:** Accepted
**Date:** 2026-04-11

## Context

The system needs storage for users, interests, markets metadata, price history, trigger events, notifications, agent memory, and LLM call logs. The access patterns are mostly relational, with a few time-series-ish reads (price history for the investigator). The project is solo and the scale is small — hundreds of watched markets, minute-granularity polling, 30-day retention.

## Decision

One Postgres instance, used for everything. JSONB columns where the structure is loose (channel configs, curator thresholds, trigger payloads).

## Alternatives considered

- **Redis for price history or caching.** Extra moving part, extra failure mode, extra thing to learn to operate. Not justified at this scale.
- **TimescaleDB for price history.** Legitimate fit for the time-series pattern but adds an extension to manage. Plain Postgres with a sensible index on `(market_id, timestamp)` handles the workload fine.
- **Splitting transactional and analytical data across databases.** Overkill.

## Consequences

- One backup, one migration path, one connection pool, one set of ops knowledge.
- At current scale Postgres handles everything trivially. Revisit if `price_history` row counts become painful (unlikely within a 30-day retention window).
- JSONB gives flexibility without abandoning relational modeling for the things that are naturally relational.
