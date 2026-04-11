# ADR-0012: Claude Code GitHub integration for PR review, advisory only

**Status:** Accepted
**Date:** 2026-04-11

## Context

The project wants an LLM-assisted code review step in the pipeline. Several options exist: Anthropic's official Claude Code GitHub integration, third-party services like CodeRabbit or Greptile, or a hand-rolled GitHub Action that calls an LLM API directly.

## Decision

Use Anthropic's Claude Code GitHub integration as the PR reviewer. Configure it as **advisory** — it posts comments on PRs but its results are *not* a required status check for merge.

## Alternatives considered

- **Third-party services (CodeRabbit, Greptile, Graphite Reviewer).** More polished out of the box with persistent context across PRs. Extra vendor, extra subscription. Not where to start.
- **Hand-rolled GitHub Action.** ~50 lines of YAML + Python to diff the PR and call an LLM. Great learning exercise but not the starting point — get the real pipeline working first.
- **Pre-commit-only LLM review.** Runs locally before push. Faster feedback but skippable and has no PR context. Complements but doesn't replace PR review.

## Consequences

- Zero infrastructure to maintain. The Action handles everything.
- False positives and occasional nonsense cannot block merges — this matters. LLM reviewers produce real mistakes; advisory status is the only safe configuration.
- Human review (self-review for a solo project) remains the authoritative one.
- Rebuilding this as a custom Action is a fine later exercise. If done, both can run in parallel.
