# ADR-0011: GitHub Actions for CI/CD

**Status:** Accepted
**Date:** 2026-04-11

## Context

The repository is hosted on GitHub. The project needs a CI system that runs lint, type check, tests, security scans, container builds, and eventually deploys. The Claude Code PR review integration is an official GitHub Action.

## Decision

Use GitHub Actions for all CI and CD workflows.

## Alternatives considered

- **GitLab CI.** Would require migrating the repo to GitLab. No reason to.
- **CircleCI.** Extra account, extra config, no advantage at this scale.
- **Self-hosted Jenkins.** Operational burden that defeats the point of a solo learning project.
- **Buildkite / Drone / etc.** Same as CircleCI — no advantage worth the switching cost.

## Consequences

- Free tier covers this project comfortably (2,000 min/month on private repos, unlimited on public).
- Ecosystem is large: official Actions for Docker buildx, GCP auth, Terraform, kubectl, Python setup with caching, and the Claude Code PR review.
- Workflows live in `.github/workflows/`. Reviewable in PRs like any other code.
- Self-hosted runners are an option later if specific jobs need them (e.g., longer-running e2e tests); not needed for v1.
