# ADR-0013: GCP with GKE Standard during trial credit, kind for ongoing dev

**Status:** Accepted
**Date:** 2026-04-11

## Context

Need a cloud environment to learn Kubernetes and Terraform in a realistic setting. Budget is near-zero. GCP offers a $300 trial credit valid for 90 days to new accounts. Azure and AWS offer comparable or smaller credits. Managed Kubernetes control planes have real per-month costs on all three.

## Decision

Use GCP. During the trial credit window, provision a GKE Standard cluster and Cloud SQL for Postgres via Terraform for focused deploy/verify sessions. Develop day-to-day on a local kind cluster. `terraform destroy` between cloud sessions.

## Alternatives considered

- **Azure AKS.** Free control plane is genuinely attractive. Comparable Terraform support. Decided against primarily on GCP's better documentation for a solo learner and a more generous trial credit.
- **AWS EKS.** $73/month control plane fee and the most complex of the three providers. Actively the wrong choice for a learning project with a budget constraint.
- **DigitalOcean.** Cheapest option. Less "industry standard" for Terraform learning; smaller ecosystem of modules and examples. Valid but suboptimal for the stated learning goals.
- **Always-free e2-micro with k3s.** $0 forever. Skips most of the Kubernetes and Terraform learning — single-node k3s on a 1GB VM is not representative of what the project is supposed to teach. Rejected.
- **GKE Autopilot.** Has a ~$75/month control plane fee (changed from free in a previous pricing update). Standard mode avoids this. Use Standard.

## Consequences

- The cloud environment is ephemeral. It exists during deploy sessions, not between them.
- Out-of-pocket cost is $0 during the trial and $0 between sessions.
- Real Kubernetes and Terraform learning happens on real managed infrastructure.
- No persistent production. This is acknowledged and embraced — see ADR-0014.
- All Terraform and k8s manifests must be written so that `terraform destroy` + `terraform apply` brings up a working system from nothing. No ClickOps.
