# ADR-0014: Spin-up-on-demand, not persistent 24/7

**Status:** Accepted
**Date:** 2026-04-11

## Context

The original framing of the project was "an app that utilizes 24/7 availability." Budget constraints and a one-month learning scope conflict with literal 24/7 cloud hosting (~$30–50/month at the cheapest realistic configuration). The question is whether "24/7" is a deployment commitment or a design constraint.

## Decision

Treat "24/7 availability" as a **design constraint** (the system is *built* to run continuously — workers, schedulers, health checks, graceful restarts, no batch-script assumptions) rather than as a **deployment commitment**. Actual uptime during the project:

- Local kind cluster whenever the laptop is on.
- Occasional multi-day cloud runs during the GCP trial window for observation and learning.

## Alternatives considered

- **Persistent cloud hosting at ~$30–50/month.** Real money, real commitment, and doesn't serve the stated learning goal any better than on-demand cloud plus local kind.
- **Pure local, no cloud at all.** Skips the Kubernetes-on-real-cloud and Terraform-on-real-cloud learning. Rejected.

## Consequences

- The architecture is unchanged — this is a deployment decision, not a design decision. The system is the same whether it's running on kind for 2 hours or on GCP for 3 days.
- Expectations about "actual uptime" are explicit: the project is for learning, not for operating a production service.
- If the project is valuable enough after the month to keep running, upgrading from on-demand to persistent is a minimal change (leave the Terraform applied, keep the cluster up). This is a future decision, not this one.
