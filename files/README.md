# Architecture Decision Records

This folder contains the ADR log for the project. Each file captures one decision.

## How to use this folder

- **One decision per file.** Numbered sequentially: `0001-slug.md`, `0002-slug.md`, etc.
- **ADRs are immutable.** If you change your mind, write a *new* ADR that supersedes the old one. Mark the old one's status as "Superseded by ADR-NNNN" and leave everything else alone.
- **Use the template** in `0000-adr-template.md` when creating a new ADR.
- **Keep them short.** ~150–300 words each. ADRs are not essays.

## Why this format

Writing decisions down as you make them forces you to articulate *why*, which is how you actually learn from the decisions. The alternatives-considered section is the most valuable part — if you can't list what you didn't pick and why, you haven't really made a decision, you've just picked the first thing that came to mind.

## Index

| # | Title | Status |
|---|---|---|
| 0001 | [Use FastAPI over Flask](0001-use-fastapi.md) | Accepted |
| 0002 | [Postgres as the sole datastore](0002-postgres-for-everything.md) | Accepted |
| 0003 | [Three-component agent architecture](0003-three-component-agent-architecture.md) | Accepted |
| 0004 | [Write the agent loop by hand](0004-write-agent-loop-by-hand.md) | Accepted |
| 0005 | [Polymarket API first, Playwright as fallback](0005-api-first-playwright-fallback.md) | Accepted |
| 0006 | [Multi-user with JWT + password login](0006-jwt-password-auth.md) | Accepted |
| 0007 | [Free-text interests over categories](0007-free-text-interests.md) | Accepted |
| 0008 | [Swappable LLM client; Anthropic as default](0008-swappable-llm-client.md) | Accepted |
| 0009 | [Prompt caching on investigator system prompt and tools](0009-prompt-caching.md) | Accepted |
| 0010 | [Ruff + mypy for lint/format/type](0010-ruff-and-mypy.md) | Accepted |
| 0011 | [GitHub Actions for CI/CD](0011-github-actions.md) | Accepted |
| 0012 | [Claude Code GitHub integration for PR review](0012-claude-code-pr-review.md) | Accepted |
| 0013 | [GCP with GKE Standard during trial credit](0013-gcp-trial-credit.md) | Accepted |
| 0014 | [Spin-up-on-demand, not persistent 24/7](0014-spin-up-on-demand.md) | Accepted |
| 0015 | [Minimal read-only dashboard; CLI is the primary client](0015-minimal-dashboard.md) | Accepted |
