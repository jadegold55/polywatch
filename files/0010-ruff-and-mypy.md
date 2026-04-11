# ADR-0010: Ruff + mypy for lint, format, and type checking

**Status:** Accepted
**Date:** 2026-04-11

## Context

Need linting, formatting, import sorting, and type checking. The Python ecosystem has historically required three or four separate tools for this. Ruff has consolidated most of them into one fast Rust-based binary.

## Decision

- **Ruff** for linting (`ruff check`) and formatting (`ruff format`). Replaces flake8, black, isort, pyupgrade, pep8-naming, and several others.
- **mypy** for static type checking.

Enforced in pre-commit locally and as blocking jobs in CI.

## Alternatives considered

- **Black + flake8 + isort.** Three tools where Ruff is one. Slower. More config files. No reason in 2026 to still split these.
- **Pyright instead of mypy.** Faster, sometimes catches more, better editor integration via Pylance. mypy has marginally better ecosystem support with some libraries (especially SQLAlchemy). Either would work; mypy is the safer default. Revisit if mypy becomes a bottleneck.
- **pylint.** Slow, noisy, opinionated in ways that don't add value over Ruff's curated rule set.

## Consequences

- One config section (`[tool.ruff]` in `pyproject.toml`) for lint and format.
- Type hints must be *real* — not decorative — because mypy will complain when they're wrong or missing.
- Ruff's rule set is tightened incrementally. Start with a sensible baseline (`E`, `F`, `I`, `B`, `SIM`, `N`, `UP`) and add more as the codebase matures.
- Pre-commit and CI use the exact same versions of both tools, pinned in `pyproject.toml` and `.pre-commit-config.yaml`.
