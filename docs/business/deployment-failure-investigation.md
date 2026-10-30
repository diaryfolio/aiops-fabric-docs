# Investigate a failed deployment

ViewSense turns release, cluster and telemetry evidence into a useful investigation, coordinating
agent-assisted findings, access controls, evidence validation and authorized delivery.

> **Proposed workflow.** Real investigation connectors, governed tools and delivery require
> implementation and acceptance. The current synthetic check does not investigate or change clusters.
> See [current capabilities](../design/high-level/00-implementation-conformance.md).

## The request

> Investigate why the latest orders-api rollout is unhealthy. Show the evidence, identify missing
> information and propose the next checks. Do not change the environment.

A verified pipeline event, monitoring alert or authorized engineer can initiate the investigation.
ViewSense binds it to the permitted tenant, environment, service and immutable release identity.
A service name in a prompt does not grant access to a namespace or another team's telemetry.

## The workflow at a glance

1. **Gather the evidence**

    Read the permitted release, rollout and telemetry facts for one service.

2. **Investigate with ViewSense**

    Compare evidence with approved runbooks and check every finding.

3. **Brief the right people**

    Give engineers the technical investigation and service owners a scoped summary.

## The workflow in detail

1. **Resolve the run.** Verify the initiating identity/event and bind the deployment, image digest,
   source revision and request ID. Deduplicate repeated event delivery so retries do not start
   uncontrolled duplicate investigations.
2. **Collect bounded evidence.** Approved connectors read rollout conditions, readiness failures,
   selected events/metrics, pipeline status and relevant configuration changes. Apply explicit
   time-window, namespace/service and field limits. Exclude secrets and minimize/redact log
   payloads before they reach the model; a read-only credential can still expose sensitive data.
3. **Investigate with the configured agent.** ViewSense invokes its agent runtime through supported APIs. It can use
   approved read-only APIs or MCP tools and retrieve an applicable runbook. It receives neither
   an unrestricted shell nor permission to follow commands embedded in logs or documentation.
4. **Validate the result.** Check cited source references, deployed versions and structured findings.
   Separate observed facts, supported explanations and unverified hypotheses. Identify missing,
   stale or contradictory evidence and preserve the source owner's completeness indicators.
5. **Deliver the permitted result.** On-call engineers receive relevant technical findings;
   service owners receive the scoped impact and next-step summary. Delivery to a wider incident
   channel requires its own recipient authorization and payload minimization.

## A synthetic investigation

The service and versions below are fictional. These are supplied example facts, not observations
about the development cluster or evidence of an executed connector.

| Source | Supplied observation |
|---|---|
| Release record | orders-api changed from version 2.4.0 to 2.4.1 |
| Deployment metadata | The new pods are running but their readiness checks fail |
| Selected events | The readiness probe receives HTTP 404 from `/readyz` |
| Approved change record | Version 2.4.1 moved the readiness endpoint to `/health/ready` |
| Approved diagnostic tool | The deployed `/health/ready` endpoint returns HTTP 200 |
| Pipeline result | Unit tests passed, but this result contains no deployed readiness-probe check |

A useful report from those facts would say:

> The deployed readiness probe still targets `/readyz`, which returns 404. The approved change
> record and diagnostic result identify `/health/ready` as the working endpoint for version 2.4.1.
> This mismatch is consistent with the new pods remaining unavailable to service traffic.
> The release owner should review a probe correction through the normal change process and assess
> rollback against the approved runbook. No environment changes were performed.

The supplied evidence supports a concrete configuration mismatch. It does not establish that all
customer failures have that one cause, or that rollback is safe. A passing unit-test result does
not prove deployment readiness. The model must not invent outage duration, affected-customer
counts or a verified recovery.

## Different outcomes for different recipients

| Recipient | Example outcome |
|---|---|
| On-call / SRE | Relevant readiness events, release references, finding, missing evidence and proposed checks |
| Service owner | Unhealthy rollout status, supported explanation, impact limits and a review request |
| Developer / release owner | The relevant change/probe mismatch and a proposed correction to review |
| Wider status audience | Only an approved, minimized status update; internal logs and environment identifiers remain restricted |

These are illustrative business grants, not automatic rights granted by console role names.
Do not reuse a shared privileged runtime session across audiences with different data access.
Apply source/model-context restrictions before analysis and current recipient checks before delivery.

## Who owns what

| Owner | Responsibility |
|---|---|
| CI/source-control/cluster/telemetry systems | Authoritative release identity, configuration, status and observations |
| Agent runtime backend | Agent definition, model connection, supported tools/skills and execution loop |
| ViewSense | Customer connector boundaries, workflow scope, authorization, result validation and delivery/evidence integration |
| Service and change owners | Runbook approval, remediation decision and separately authorized change execution |

Configure models and the saved agent through [runtime administration](../deploy/trueforge-access.md).
The backend is independently maintained and remains unmodified; ViewSense owns customer connectors
and business adaptations. The workflow and administration interface must use the same approved
runtime instance. The current standalone preview and hosted runtime have separate data, so preview
configuration is not hosted integration evidence.

## Safe failure and action boundaries

- Missing telemetry or inaccessible events produce an incomplete investigation, not “no incident.”
- Model failure is visible as unavailable analysis; preserve permitted source facts without
  presenting fabricated or mock findings as successful AI investigation.
- A changed deployment or stale source revision requires refreshing the evidence before acting.
- An investigation identity has no cluster mutation, unrestricted execution or secret-read grant.
- Suggested correction, restart or rollback remains a proposal. A future action step needs fresh
  action-specific authorization, required approval, immutable target binding and reconciliation.
  A native agent approval prompt alone does not establish business change authority.
- Generated and delivered are separate states. Retry approved delivery with deduplication and
  recheck recipients; do not restart agent work merely because a notification failed.

Qualify runtime persistence and retention for prompts/tool results as well as ordinary logs.
Excluding raw logs from application logging does not establish that the agent runtime stores no context.
See the [enterprise controls](../design/high-level/60-enterprise/01-enterprise-integration-controls.md).

## A practical first pilot

Start with the synthetic evidence above, one approved local model connected to the agent runtime and an
authorized ViewSense report view. Compare the structured findings with the supplied reference.
Then qualify one read-only service/environment and one delivery destination. Add APIs/MCP only
as required; a vector database, another agent loop and a new workflow engine are not prerequisites.

Acceptance includes wrong-environment and unauthorized-namespace denial, repeated events,
untrusted instructions in tool results, conflicting/stale evidence, model outage, redaction,
role-scoped views, revoked recipients and delivery retry. Report time to an accepted investigation,
evidence completeness, unsupported claims and reviewer effort against the manual baseline.
This example asserts no measured reduction in incident duration or production-ready remediation.

Browse [Detailed examples](examples/index.md), return to the [value and use-case tables](value-and-use-cases.md), or compare the
[reorganisation-performance walkthrough](hr-departure-workflow.md), which uses the same integration pattern.
