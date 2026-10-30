---
hide:
  - toc
---

# Business overview

Connect in-house applications to AI-assisted workflows and deliver useful outcomes to the right
people. ViewSense AI® coordinates approved agents, enterprise integrations and access controls.

## The workflow at a glance

1. **Connect your systems**

    Bring together approved information from in-house applications, events and requests.

2. **Process with ViewSense**

    Use a configured agent and permitted tools, with fabric applying enterprise controls.

3. **Deliver useful outcomes**

    Return reviewed reports, recommendations or approved tasks to the relevant people.


This section is for business sponsors, management, procurement, and risk teams. Start with
[pilot fit](business/compatibility.md), then
[value and use-case tables](business/value-and-use-cases.md) and
[adoption and governance](business/adoption-and-governance.md).

The [example comparison tables](business/value-and-use-cases.md) group ideas by team, including
security, HR, Finance, customer/product teams, Procurement, Operations, Engineering, manufacturing,
facilities and research. Each group contains two to five examples, with MCP as the main product
integration approach. Open [Detailed examples](business/examples/index.md) for ITSM service impact,
supplier renewal, reorganisation-performance and deployment-investigation walkthroughs.

These are target workflows with explicit acceptance gates, not shipped business connectors or
autonomous production operations.

## The management decisions

| Decision | What the organisation controls |
|---|---|
| Where AI runs | The approved deployment location and whether a request may use a local or cloud model. |
| Which knowledge is available | Data ownership, allowed users, permitted purposes, and the information admitted into a pilot. |
| Which suppliers are used | The model, memory, identity, and operational products accepted for the selected application release. |
| Which actions are allowed | Budgets, permissions, and approval requirements; executable business-tool automation remains a planned extension. |
| When to expand | Evidence from quality, cost, security, and operational acceptance. |

## What can be evaluated now

The tested reference includes a fixed synthetic agent-execution check,
PostgreSQL/pgvector memory, basic document ingestion, provider admission APIs and safe evidence
APIs. The old response orchestration and manual agent kernel are retired. Development identity,
static certificates, mock models and mock tools are test components. General business execution,
including the HR example, remains gated.

OpenAI, Ollama, Mem0, enterprise identity, and selected operational integrations have documented
integration paths. They require configuration and acceptance in the organisation's environment.
The local Ollama decision and embedding retrieval path has development evidence; that evidence does
not certify an enterprise deployment.

Autonomous business actions, native MCP transport, workflow-engine adapters, and several production
operations capabilities remain planned. The architecture guide to
[integration compatibility](design/high-level/10-overall/11-integration-compatibility.md)
separates these states, and the [implementation conformance map](design/high-level/00-implementation-conformance.md)
records the technical evidence and outstanding gaps.

## A useful first commitment

Choose one read-only reporting or investigation pilot with a named owner, approved information,
a limited user group and human review. Start with synthetic facts and one authorized result view.
Agree success measures and environment acceptance before
connecting sensitive data or expanding the service. The [adoption guide](business/adoption-and-governance.md)
provides the decision gates and responsibilities.

Use the release dropdown to read documentation for the corresponding ViewSense AI® application
version. **Latest (main)** describes ongoing development; release documentation records the selected
baseline. Neither label establishes the acceptance status of a customer installation.
