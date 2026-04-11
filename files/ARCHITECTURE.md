# Architecture Map

A living description of what's in the codebase and how the pieces fit together. Updated whenever the structure changes. This is the *what* — for the *why* behind any specific decision, see `docs/adr/`.

## How to use this file

- **Update it when you add a component, move a module, or change how two pieces talk to each other.**
- **Keep it descriptive, not prescriptive.** This file describes the code as it currently exists, not as it was planned. If the code drifts from the plan, update this file to match the code and (if the drift was a real decision) write a new ADR.
- **Short is good.** If a section is getting long, it probably wants to be its own document.

## Top-level layout

*(Fill in as directories come into existence during week 1.)*

```
polywatch/
├── src/polywatch/     # application code
├── src/cli/           # management CLI
├── tests/             # unit, integration, agent, e2e
├── deploy/            # k8s manifests and terraform
├── docker/            # Dockerfiles
├── docs/              # ADRs and this file
└── scripts/           # local dev helpers
```

## Components

*(One subsection per deployable component. Fill in as each is built.)*

### api

Status: not started.

### curator

Status: not started.

### evaluator

Status: not started.

### investigator

Status: not started.

### notifier

Status: not started.

### cli

Status: not started.

## How components talk to each other

*(Fill in once the first inter-component call exists. The three-component agent flow from `PLAN.md` is the starting template — copy it here and adjust as the real shape emerges.)*

## Data flow

*(Fill in as the first real tables and migrations land in week 1.)*

## External dependencies

*(Polymarket API, LLM provider, Playwright, notification channel endpoints. Fill in with actual URLs and rate limits once you've hit them.)*
