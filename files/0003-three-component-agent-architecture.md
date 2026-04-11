# ADR-0003: Three-component agent architecture (curator / evaluator / investigator)

**Status:** Accepted
**Date:** 2026-04-11

## Context

The system's premise is "an agent autonomously watches markets and tells me when something interesting happens." The naive implementation — one always-on agent that polls and decides everything — is expensive (LLM cost on every tick), hard to debug, and hard to rate-limit. A pure rule-based system at the other extreme is cheap but can't generate the *explanation* that makes notifications valuable.

## Decision

Split the work into three components with different cadences and different cost profiles:

- **Curator** — slow (every few hours), one LLM call, picks markets to watch and writes per-market thresholds.
- **Evaluator** — fast (every minute), pure Python, no LLM. Compares live prices against thresholds, writes trigger events.
- **Investigator** — on-demand, real agent loop with tools, produces the written notification.

## Alternatives considered

- **Single always-on agent with total freedom.** Expensive, opaque, hard to put guardrails on. Cost scales with tick frequency, not with interesting events.
- **Pure rule-based system with no LLM.** Cheap but no explanation. The whole point of using an LLM is the synthesis in the investigator step.
- **Curator + investigator without the cheap evaluator.** Would require the agent loop to wake up every tick to check thresholds it already set. Pointless LLM cost.

## Consequences

- Clear separation of concerns: curator decides *what to watch*, evaluator decides *when to fire*, investigator decides *what to say*.
- LLM cost is bounded by real events — not by tick frequency.
- Only the investigator needs a real agent loop. The curator is a one-shot LLM call. The evaluator has no LLM at all.
- This is the single most important architectural decision in the project. Everything else flows from it.
