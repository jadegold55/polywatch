# Polymarket Autonomous Research Agent — Project Plan

## 1. Project Summary

A self-directed agent that watches Polymarket prediction markets on behalf of its users. Users give the system a free-text description of what they're interested in; a curator component picks relevant markets to watch; a cheap evaluator flags notable movement; and an investigator agent uses browser automation and LLM reasoning to figure out *what* happened and *why*, then writes a human-readable notification and dispatches it to the user's configured channels (webhook, Discord, email).

The app is a vehicle for learning a production-shaped Python backend stack: FastAPI, Postgres, Kubernetes, Terraform, Docker, Playwright, a real CI/CD pipeline, and hand-written LLM agent loops. The target is a working, deployable system in roughly one month of evening/weekend work by a single developer.

For the "why" behind every design choice in this document, see the ADRs in `docs/adr/`. For ongoing work notes, see `LOG.md`. For things learned along the way, see `LEARNING.md`. For a living map of the codebase, see `docs/ARCHITECTURE.md`.

## 2. Goals and Non-Goals

### Goals

- Learn how the pieces of a modern Python backend fit together — API, workers, scheduler, database, migrations, testing, containerization, orchestration, IaC.
- Learn Kubernetes fundamentals (deployments, services, jobs, cronjobs, configmaps, secrets, namespaces) by running workloads on both a local kind cluster and a real cloud cluster.
- Learn Terraform by provisioning a real GCP environment from scratch (GKE, Cloud SQL, networking, secrets).
- Learn how to design and implement a real agent loop by hand — tool definitions, the tool-use cycle, cost controls, prompt caching — without hiding behind a framework.
- Learn a disciplined CI/CD pipeline with linting, type checking, testing, security scanning, container builds, automated deploys, and LLM-assisted code review.
- Produce a system that genuinely does the useful thing it claims to do: autonomously surface notable Polymarket events.

### Non-Goals

- **Persistent 24/7 cloud hosting.** The system runs on GCP only during focused deploy/verify sessions using trial credit. Between sessions it lives on a local kind cluster.
- **Web frontend beyond a minimal read-only dashboard.**
- **SMS/phone notifications.** Twilio costs per message and adds verification flows. Deferred indefinitely.
- **Self-hosted LLMs.** A swappable LLM client interface is in scope; actually running llama.cpp or vLLM is not.
- **A Discord bot.** Discord integration uses webhook URLs only.
- **Public multi-tenant hosting.** Multi-user auth is in scope as a learning exercise. The system is not hardened for the public internet.
- **Agent frameworks.** No LangChain, LlamaIndex, CrewAI, AutoGen. The agent loop is written by hand. See ADR-0004.

## 3. Architecture Overview

The system has three execution paths with very different cadences and cost profiles. Keeping them separate is the single most important architectural decision in this project — conflating them would either make everything expensive (cheap path pays LLM cost) or make everything dumb (smart path runs on hardcoded rules). See ADR-0003.

```
                          ┌────────────────────────────┐
                          │   Polymarket CLOB / Gamma  │
                          │   (external HTTP API)      │
                          └─────────────┬──────────────┘
                                        │
       ┌────────────────────────────────┼────────────────────────────────┐
       │                                │                                │
       ▼                                ▼                                ▼
┌────────────┐                  ┌────────────┐                  ┌──────────────┐
│  Curator   │                  │ Evaluator  │                  │ Investigator │
│ (CronJob,  │                  │ (Deploy,   │                  │ (triggered,  │
│  slow)     │                  │  tight     │                  │  agent loop  │
│ LLM call   │                  │  loop)     │                  │  + Playwright│
│ every few  │                  │ no LLM     │                  │  + LLM tools)│
│ hours      │                  │ every min  │                  │              │
└─────┬──────┘                  └─────┬──────┘                  └──────┬───────┘
      │                               │                                │
      │ writes watchlist              │ reads watchlist                 │ reads trigger event
      │ + per-market notes            │ writes price history            │ writes notification
      │                               │ writes trigger events           │ + reasoning trace
      ▼                               ▼                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                              Postgres                                    │
│  users · interests · watchlist · price_history · trigger_events          │
│  notifications · notification_log · agent_memory · llm_call_log          │
└──────────────────────────────────────────────────────────────────────────┘
      ▲                                                                ▲
      │ reads/writes                                                   │ reads notifications
      │                                                                │ fans out to channels
┌─────┴──────┐                                                   ┌─────┴──────┐
│  FastAPI   │                                                   │  Notifier  │
│  (REST)    │◄──── CLI client ─────────────────────────────────►│  workers   │
│  + dashbd  │                                                   │ (webhook,  │
└────────────┘                                                   │  Discord,  │
                                                                 │  email)    │
                                                                 └────────────┘
```

### The three execution paths

**Curator.** Runs on a Kubernetes CronJob every few hours. Makes a single LLM call (not an agent loop) with the current list of active Polymarket markets, the user's interests, and the existing watchlist. Returns an updated watchlist with per-market notes describing what to look for and at what thresholds. Writes to the `watchlist` table. No tools, no loop — a thoughtful one-shot.

**Evaluator.** Runs continuously as a Kubernetes Deployment with an internal loop (sleeps a minute, works, repeats). Pure Python, no LLM. Each tick: read the watchlist, pull current prices from Polymarket in bulk, write fresh rows to `price_history`, compare against the curator's per-market thresholds plus built-in movement heuristics, write rows to `trigger_events` when something fires. Fast, cheap, deterministic.

**Investigator.** Triggered by new rows in `trigger_events`. The only true agent loop in the system. Given a trigger event, runs the tool-use cycle with access to a small set of tools (fetch market details, fetch price history, browse Polymarket market page via Playwright, fetch comments, optionally web search) and produces a short written notification explaining what happened. Writes the notification plus the full reasoning trace to `notifications` and `notification_log`.

### API and CLI

**FastAPI** serves a REST API for user management, interests, watchlist viewing, and notification history. It also serves a small read-only HTML dashboard for the same. It contains no agent logic — it is strictly an interface onto the state the workers manage.

**CLI** is a separate Python binary (Typer-based) that talks to the REST API over HTTP. Subcommands for account management, interests, watchlist, notifications. Shares no code with the API server — it's a genuine client.

## 4. Component Inventory

| Component | Deployable | Purpose |
|---|---|---|
| `api` | k8s Deployment + Service | FastAPI server: REST + HTML dashboard |
| `curator` | k8s CronJob | Periodic LLM-driven watchlist curation |
| `evaluator` | k8s Deployment | Continuous price polling and trigger detection |
| `investigator` | k8s Deployment | Agent loop: consumes trigger events, writes notifications |
| `notifier` | k8s Deployment | Consumes new notifications, fans out to webhook/Discord/email |
| `migrations` | k8s Job (one-shot) | Alembic migrations run on deploy |
| `postgres` | Managed (Cloud SQL in cloud; StatefulSet in kind) | System of record |
| `cli` | Built and distributed as a wheel; not deployed | Management client |

Each component is a separate Docker image built from the same monorepo, with a shared base image for Python dependencies.

## 5. Data Model (high level)

Tables, not full DDL. Exact columns get designed during week 1.

- **`users`** — id, email, password_hash, created_at
- **`interests`** — user_id, description (TEXT), updated_at
- **`notification_channels`** — id, user_id, kind (`webhook`/`discord`/`email`), config (JSONB), enabled
- **`markets`** — cached Polymarket market metadata
- **`watchlist`** — id, user_id, market_id, curator_notes (TEXT), thresholds (JSONB), added_at, expires_at
- **`price_history`** — market_id, timestamp, price, volume_24h. Retention: 30 days.
- **`trigger_events`** — id, watchlist_id, market_id, kind, payload (JSONB), created_at, investigated_at
- **`notifications`** — id, user_id, trigger_event_id, title, body, created_at
- **`notification_log`** — notification_id, channel_id, attempt_at, success, error
- **`agent_memory`** — key-value store for small persistent state used by curator and investigator
- **`llm_call_log`** — every LLM call: component, model, input_tokens, output_tokens, cached_tokens, cost_cents, latency_ms, created_at

The `llm_call_log` table is non-negotiable. Without it you cannot answer "what am I spending and why," and that question will come up.

## 6. Agent Design (investigator)

The investigator is the only component that runs a real agent loop. The loop is ~40 lines of hand-written Python. See ADR-0004 for why no framework.

### Shape of the loop

```python
async def investigate(event: TriggerEvent) -> Notification:
    messages = [build_initial_message(event)]
    for turn in range(MAX_TURNS):  # hard cap, e.g. 8
        response = await llm.complete(
            system=INVESTIGATOR_SYSTEM_PROMPT,  # cached
            tools=INVESTIGATOR_TOOLS,            # cached
            messages=messages,
        )
        messages.append(assistant_message(response))
        if response.stop_reason == "end_turn":
            return parse_final_notification(response)
        tool_results = await run_tools(response.tool_uses)
        messages.append(user_message(tool_results))
    raise InvestigationExceededTurns(event.id)
```

### Tools available to the investigator

- `get_market_details(market_id)` — full market metadata
- `get_price_history(market_id, hours)` — recent price series
- `get_market_comments(market_id, limit)` — recent comments via Playwright
- `browse_url(url)` — fetch and render a URL, return extracted text
- `search_web(query)` — optional, deferred if costs are a concern
- `finalize(title, body)` — "I'm done" tool. Forcing the final answer through a tool gives structured output without JSON-mode brittleness.

### System prompt sketch

Rough shape, not final wording:

> You are an analyst investigating unusual activity in a Polymarket prediction market. You will be given a trigger event describing what moved. Use your tools to determine what happened and why. When you have enough information, call `finalize` with a short title and a 2–4 sentence body. The body should explain the movement in plain language and cite the evidence you used. Do not speculate beyond what your tools returned.

### Cost controls

- **Max turns per investigation: 8.** Hard cap.
- **Prompt caching on system prompt + tool definitions.** See ADR-0009.
- **Per-user rate limit: N investigations per hour.**
- **Global kill switch** — env var `LLM_ENABLED=false` short-circuits all LLM calls.
- **Daily budget cap** — the investigator checks `llm_call_log` sum for the day and refuses to run if over budget.
- **Model tiering** — cheap model for cheap work, better model for final synthesis.

## 7. Tech Stack

### Language and framework
- Python 3.12+
- FastAPI (async routes throughout)
- Pydantic v2
- Uvicorn (ASGI server)

### Data
- Postgres 16 (Cloud SQL in cloud, StatefulSet locally)
- SQLAlchemy 2.0 async (SQLModel optional)
- asyncpg
- Alembic

### External I/O
- httpx
- Playwright (async Python API, Chromium only)
- Anthropic Python SDK (wrapped in a swappable interface — see ADR-0008)

### CLI
- Typer
- Rich

### Observability
- structlog (structured JSON logging)
- OpenTelemetry (v2)

### Dev tooling
- Ruff (lint + format)
- mypy
- pytest, pytest-asyncio, pytest-cov
- testcontainers-python
- pre-commit
- bandit, pip-audit

### Infra
- Docker + Docker Compose
- kind (local Kubernetes)
- kubectl, helm as needed
- Terraform (GCP provider)
- GitHub Actions
- Claude Code GitHub integration (PR review)

## 8. Repository Layout

```
polywatch/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── deploy-dev.yml
│       ├── deploy-prod.yml
│       └── claude-review.yml
├── docs/
│   ├── adr/                          # one file per decision — see README.md
│   └── ARCHITECTURE.md               # living map of the codebase
├── src/
│   ├── polywatch/
│   │   ├── api/
│   │   │   ├── main.py
│   │   │   ├── routes/
│   │   │   ├── deps.py
│   │   │   ├── auth.py
│   │   │   └── dashboard/
│   │   ├── curator/
│   │   ├── evaluator/
│   │   ├── investigator/
│   │   │   ├── loop.py
│   │   │   ├── tools.py
│   │   │   └── prompts.py
│   │   ├── notifier/
│   │   │   └── channels/             # webhook.py, discord.py, email.py
│   │   ├── llm/
│   │   │   ├── client.py             # protocol
│   │   │   ├── anthropic_impl.py
│   │   │   └── budget.py
│   │   ├── polymarket/
│   │   ├── db/
│   │   │   ├── models.py
│   │   │   ├── session.py
│   │   │   └── migrations/
│   │   ├── config.py
│   │   └── logging.py
│   └── cli/
│       └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── agent/
│   └── e2e/
├── deploy/
│   ├── k8s/
│   │   ├── base/
│   │   └── overlays/
│   │       ├── local-kind/
│   │       └── gcp/
│   └── terraform/
│       ├── main.tf
│       ├── gke.tf
│       ├── cloud-sql.tf
│       └── network.tf
├── docker/
│   ├── base.Dockerfile
│   ├── api.Dockerfile
│   ├── worker.Dockerfile
│   └── docker-compose.yml
├── scripts/
│   ├── bootstrap-kind.sh
│   └── seed-db.sh
├── LEARNING.md
├── LOG.md
├── README.md
├── pyproject.toml
└── .pre-commit-config.yaml
```

## 9. Infrastructure

### Local: kind

- `scripts/bootstrap-kind.sh` creates a kind cluster, installs an ingress controller, creates namespaces, applies the `local-kind` kustomize overlay.
- Postgres runs as a StatefulSet inside the cluster.
- Secrets from a `.env` file loaded via script, not committed.
- Playwright Chromium installed during worker image build.
- Reach the API via `kubectl port-forward` or ingress with a `/etc/hosts` entry.

### Cloud: GCP (trial credit only — see ADR-0013)

Terraform provisions:

- **GKE Standard** cluster, single region, one small node pool, autoscaling off.
- **Cloud SQL for Postgres**, smallest tier, private IP only.
- **VPC** with a single subnet, Cloud NAT for pod egress.
- **Secret Manager** entries for LLM keys, Postgres password, channel creds.
- **Artifact Registry** repo for Docker images.
- **Workload Identity** so pods access Secret Manager without JSON keys.

Deploy flow:

1. `terraform apply` — ~10 minutes.
2. CI pushes images to Artifact Registry on merge to main.
3. `kubectl apply -k deploy/k8s/overlays/gcp`.
4. Verify pods, smoke-test via port-forward.
5. Observe running for however long is useful, within credit budget.
6. `terraform destroy` when done.

## 10. CI/CD Pipeline

GitHub Actions. Job DAG — fast checks gate slower ones.

### On every push and PR

```
lint ──┐
type ──┼─► unit-tests ──► integration-tests ──► docker-build
       │                                             │
security ────────────────────────────────────────────┘
```

1. **lint** — `ruff check .` and `ruff format --check .`
2. **type** — `mypy src/`
3. **unit-tests** — `pytest tests/unit`
4. **integration-tests** — `pytest tests/integration` with Postgres service container
5. **security** — `bandit -r src/` and `pip-audit`
6. **docker-build** — buildx with GHA layer cache; no push on PRs

### On PR only

7. **claude-review** — Claude Code GitHub integration. Advisory only, not a required check.
8. **openapi-drift** — export FastAPI OpenAPI schema, diff against `docs/openapi.json`. Fails on unexpected changes.

### On merge to main

9. **push-images** — re-run docker-build with `push: true` to Artifact Registry.

### On git tag `v*.*.*`

10. **deploy-prod** — Terraform + k8s manifests to GCP. Manual approval gate.

### Caching

- `actions/cache` on `~/.cache/pip` and `~/.cache/ms-playwright`
- buildx GHA cache on Docker layers
- `actions/setup-python` keyed to `pyproject.toml` hash

### Pre-commit

`.pre-commit-config.yaml` runs Ruff and fast mypy on changed files. CI runs the full suite as a safety net. Same tools, same config, zero drift.

## 11. Testing Strategy

Four layers:

### Unit tests (`tests/unit/`)
Pure functions. No DB, no network, no LLM. Whole suite in a few seconds. Target: evaluator comparison logic, notifier channel formatters, Polymarket client parsing, LLM budget calculator.

### Integration tests (`tests/integration/`)
API routes via `TestClient` against real Postgres launched by `testcontainers-python`. No DB mocking. Mocked LLM, Polymarket, Playwright. Target: auth flows, CRUD, permission enforcement.

### Agent tests (`tests/agent/`)
Three sub-tiers:
- **Mocked-LLM tests** — fake LLM returns scripted responses including scripted tool uses. Verifies loop logic.
- **Replay tests** — record real investigations to fixtures, replay in tests. Catches prompt/tool regressions.
- **Smoke tests** — hit the real API in CI on main only. Assert structural properties. Budget: cents per run.

### E2E tests (`tests/e2e/`)
Docker Compose brings up the full stack. Seed synthetic data, assert a notification appears end-to-end. Run on main only.

### Coverage target
70% unit + integration for v1. Don't chase 100%.

## 12. Week-by-Week Milestones

Four weeks of evening/weekend work. Each week produces a working artifact you could demo. If a week slips, cut from later weeks before cutting foundations.

### Week 1 — Foundations (no agent, no infra)

**Goal:** Working FastAPI app with auth, users, interests, notifications table. Running locally against Postgres in Docker Compose. No Kubernetes yet. No LLM yet.

- Init repo, pyproject.toml, Ruff, mypy, pre-commit, pytest.
- GitHub Actions CI: lint, type, unit test. Get it green.
- Docker Compose with Postgres. Alembic init + first migration.
- FastAPI skeleton: config, logging, DB session, DI scaffold.
- JWT auth: register, login, refresh, `get_current_user` dep.
- CRUD routes for interests and notification channels.
- Unit tests for auth helpers, integration tests for auth + CRUD with testcontainers.
- Start `LEARNING.md` and `LOG.md`. Commit daily.
- Write ADR-0001, 0002, 0006, 0007.

**End of week 1:** `docker compose up` then `pytest` passes. Register/login/set interests via curl.

### Week 2 — Containers, kind, CI/CD maturity

**Goal:** Everything from week 1 deployed to a local kind cluster, with a complete CI pipeline including Docker builds and PR review.

- Dockerfiles: `base`, `api`, `worker` (with Playwright Chromium).
- Add `docker-build` and `integration-tests` jobs with caching.
- Add security scanning (bandit, pip-audit).
- Install kind, write `bootstrap-kind.sh`.
- K8s manifests/kustomize: namespace, postgres StatefulSet + Service, api Deployment + Service, ingress, ConfigMap, Secret.
- Deploy to kind. Verify via port-forward.
- One-shot migrations Job as prerequisite for api Deployment.
- Set up Claude Code GitHub integration. Open a test PR.
- CLI skeleton: `poly register/login/interests set/show`. Install editable.
- Write ADR-0010, 0011, 0012.

**End of week 2:** `bootstrap-kind.sh`, deploy, interact via CLI. PRs get Claude review comments.

### Week 3 — The agent

**Goal:** Curator, evaluator, investigator running on kind, talking to real Polymarket and real LLM, producing notifications end-to-end.

- `polymarket/client.py` with listing, details, prices, comments (Playwright). Unit test parsing.
- Migrations: `markets`, `watchlist`, `price_history`, `trigger_events`, `agent_memory`, `llm_call_log`.
- `llm/` package: `LLMClient` protocol, Anthropic impl, budget tracker.
- Curator: one-shot entrypoint, LLM call, writes watchlist. Deploy as CronJob.
- Evaluator: loop, thresholds, trigger writes. Deploy as Deployment.
- Investigator: loop, tools, prompts, finalize tool. Deploy as Deployment.
- Notifier: consumes notifications, fans out to webhook/Discord/email.
- Agent tests: mocked-LLM for loop logic, one replay test.
- Run locally against live APIs for an hour at a time, watch it work.
- Write ADR-0003, 0004, 0005, 0008, 0009.

**End of week 3:** You can set interests via CLI and within an hour see the curator pick markets, the evaluator fire triggers, and the investigator send a notification.

### Week 4 — Terraform, GCP, polish

**Goal:** A working Terraform setup that deploys the system to GCP from scratch in one command, plus the minimal dashboard and any remaining polish.

- Terraform: VPC, GKE Standard cluster, Cloud SQL, Secret Manager, Artifact Registry, Workload Identity.
- Test the full cycle: `terraform apply` → push images → deploy → verify → `terraform destroy`. Do it twice.
- `deploy-prod.yml` workflow with manual approval gate.
- Minimal HTML dashboard: Jinja templates, 3–4 routes (watchlist, notifications, notification detail). Read-only.
- Smoke tests in CI for agent behavior.
- Finalize `docs/ARCHITECTURE.md`.
- Write ADR-0013, 0014, 0015.
- Final cost audit of `llm_call_log`.
- README polish.

**End of week 4:** One-command deploy to GCP. Dashboard works. System runs autonomously for an observation window of hours or days within the trial credit.

## 13. Open Questions for Future-You

Things deliberately not decided here:

- **Which transactional email provider.** Resend, Postmark, Mailtrap for dev. Decide during week 3 when you wire up the email channel.
- **Which model tier for curator vs investigator.** Decide empirically — start both on the same cheap-but-capable model, upgrade the investigator's final-synthesis step if output quality is poor.
- **Whether to use SQLModel or plain SQLAlchemy.** Start with SQLModel; fall back to plain SQLAlchemy if it limits you.
- **Whether to add a `search_web` tool to the investigator.** Defer until you've seen investigations without it and identified cases where it would help.
- **Whether to wrap the Polymarket tools as an MCP server.** A v2 refactor if you feel like it. Not on the critical path.
- **Whether to add OpenTelemetry traces.** After the basic system works. The value is high but the payoff comes from actually debugging a weird production issue, which requires first having production.
