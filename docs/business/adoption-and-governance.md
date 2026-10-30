---
hide:
  - toc
---

# Business adoption and governance

Adopt ViewSense AI® through a limited evaluation with explicit business and technical owners.
Approve the use case and data before connecting a real provider, then expand only after the
selected environment meets its acceptance criteria.

## The workflow at a glance

1. **Scope the use case**

    Agree the owner, users, data, budget and success measures.

2. **Run and review a pilot**

    Test a limited workflow and review quality, access, cost and recovery evidence.

3. **Make the next decision**

    Expand, revise or stop using the recorded acceptance results.

This is a management process. The four decision gates below require explicit owner decisions. A working demonstration
completes part of the pilot; it does not complete security or operational acceptance.

| Gate | Evidence needed for the decision |
|---|---|
| Agree the use case | Named sponsor, users and data owner; allowed purpose; measurable targets; approved product choices and cost boundary. |
| Run the controlled pilot | Matching application/docs baseline; configured integrations; representative test questions; access tests; human review and a stop procedure. |
| Review acceptance | Quality results, supplier and data-flow approvals, enforced isolation, operational monitoring, recovery evidence, and total operating cost. |
| Decide on expansion | Named service owner and support model; recorded acceptance or remaining blockers; rollout, rollback, training, and review arrangements. |

## Measure the pilot

Compare a small, approved read-only workflow with the manual process before expanding access
or allowing actions. Start with synthetic facts, one accountable owner and one permitted result view.

| Goal | Evidence to agree before the pilot |
|---|---|
| Reduce investigation or reporting effort | Manual baseline, reviewer time and proportion of results accepted. |
| Improve useful findings | Source-grounded accuracy, missing-data handling and reviewer corrections. |
| Preserve access boundaries | Denied source, tool and recipient tests, including revoked membership. |
| Keep operation understandable | Cost per accepted result, visible failures and safe retry/delivery behavior. |
| Preserve supplier choice | An approved model/runtime upgrade without changing business-system contracts. |

The examples establish no measured savings, certified root-cause accuracy or production readiness.

## Who owns what

| Owner | Responsibility |
|---|---|
| Business sponsor | Own the outcome, budget, success measures, and decision to continue or stop. |
| Data owner | Approve information use, permissions, retention, and the removal or correction of unsuitable knowledge. |
| Security and risk | Review identity, data movement, provider admission, isolation evidence, and approval rules. |
| Platform and service owner | Qualify product versions, operate dependencies, monitor the service, and test upgrades, rollback, and recovery. |
| Business reviewers | Assess answer quality, record failures, and decide whether an answer is suitable for use. |
| Procurement and finance | Review supplier terms, support, licences, and the full cost of operation and change. |

## Production acceptance still requires work

The [conformance map](../design/high-level/00-implementation-conformance.md) records a recovered development
network-isolation failure and remaining production mesh/environment acceptance. High availability and disaster
recovery, production identity/session controls, immutable evidence export, durable telemetry, and
coordinated certificate/trust rotation also have outstanding work. These are explicit blockers or
acceptance requirements to resolve for the intended deployment, not features established by a pilot.

Governed business use of native MCP, workflow-engine integrations and autonomous actions remain planned. Do not make
them dependencies of a committed business outcome until implementation and acceptance exist.

## Keep the business baseline aligned with releases

Select the docs version that matches the application release. Record that release alongside the
approved upstream versions and acceptance results. Reassess provider compatibility, data access,
quality, and operating procedures when a release or product changes.

**Latest (main)** can include development changes beyond a released application. The
[release publishing guide](../publishing.md#documentation-per-application-release) explains how
the documentation snapshots are retained. Calendar dates are not used as documentation versions.
