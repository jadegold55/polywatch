# ADR-0009: Prompt caching on investigator system prompt and tools

**Status:** Accepted
**Date:** 2026-04-11

## Context

The investigator runs a multi-turn agent loop. The system prompt and tool definitions are identical across every turn of every investigation. Without prompt caching, the model re-processes the full system prompt and tool list on every turn, and the API bills for it every time. On a multi-turn loop this adds up fast.

## Decision

Mark the system prompt and tool definitions as cached via Anthropic's prompt caching feature. Structure the API call so the cached portion is stable across turns and the per-turn context (messages, tool results) is the only thing that varies.

## Alternatives considered

- **No caching.** Pays full input-token cost on every turn. Wasteful.
- **Cache everything including per-investigation context.** Cache thrashes between investigations, no hits.
- **Smaller system prompt and fewer tools to reduce the cost instead of caching.** Trades off agent quality for cost. Caching is free quality.

## Consequences

- Per-investigation cost drops substantially after turn 1 — the cached portion bills at a fraction of normal input-token cost.
- Cache invalidates naturally when the system prompt or tool list changes in code. That's a feature, not a bug.
- The `LLMClient` interface must carry cache hints. Providers that don't support caching ignore them.
- Any change to the system prompt or tools should be evaluated for its cost impact — changing them frequently reduces the cache hit rate.
