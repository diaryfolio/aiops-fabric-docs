# ITSM service dependency and impact analysis

An incident affects a shared component. ViewSense AI® uses approved MCP connections to bring
service relationships, monitoring evidence and business ownership into one impact brief.

> **Proposed workflow.** ITSM, service-map and monitoring MCP integration, business execution and
> governed delivery require implementation and acceptance. The example below is synthetic; it
> does not inspect a live ServiceNow instance. See [current capabilities](../../design/high-level/00-implementation-conformance.md).

## The incident manager's question

> The orders database has a connection failure. Starting from its ServiceNow or ITSM record,
> find the linked services, explain the potential business impact, and identify the owners.
> Show what is observed, what is only a dependency-based concern, and where evidence is missing.

The same approach can help review a proposed change before it is carried out. An incident review
assesses current observations; a change review describes a scenario and must not label the
predicted effects as an outage already happening.

## The workflow at a glance

1. **Read the service map through MCP**

    Resolve the incident and affected component, then retrieve its permitted service dependencies.

2. **Check the business impact**

    Combine the recorded paths with service health, operating schedules and owner records.

3. **Brief the right people**

    Give responders the evidence and service owners a scoped impact summary with open questions.

## From one component to business services

The configuration management database (CMDB) records configuration items and relationships.
A configuration item can represent a database, application or service. In this fictional map,
**Order processing depends on the orders database**, and **Customer checkout depends on Order processing**.

The diagram follows the possible impact in the opposite direction: from the affected dependency
towards its consumers. Lines represent supplied dependency paths; they do not establish that
every linked service has failed.

[![Synthetic service-impact map: a database connection failure links to Order processing and Reporting export; Customer checkout has observed degradation, Daily sales reporting has potential impact, and Warehouse dispatch needs validation because its map link is stale.](../../assets/images/itsm-service-impact.svg)](../../assets/images/itsm-service-impact.svg)

[Open the service-impact map at full size](../../assets/images/itsm-service-impact.svg).

## The supplied evidence

These identifiers are fictional source references. All health observations belong to the same
incident assessment window; a live workflow must record its actual evidence cut-off and freshness.

| Source | Supplied fact | What it supports |
|---|---|---|
| INC-1 · Incident record | The incident identifies the production component `orders-db-primary`. | A stable starting point; a component name alone does not grant access. |
| MAP-1 · Current service relationships | Order processing and Reporting export depend on that component. Customer checkout depends on Order processing; Daily sales reporting depends on Reporting export. | Two current paths towards business services that warrant impact assessment. |
| MON-1 · Monitoring | Database connection checks fail and the Customer checkout journey check fails in the assessment window. | Observed connection and checkout failures. The map supports investigation of a shared dependency, not proof of one sole root cause. |
| JOB-1 · Reporting schedule | The next Daily sales reporting run has not started; no failed run is supplied. | Potential impact on the next run if the dependency remains unavailable. Current reporting failure is not established. |
| MAP-2 · Older relationship | Warehouse dispatch is linked to Order processing, but the relationship is outside the approved freshness window. | An unverified path requiring owner confirmation, not a confirmed affected service. |
| OWN-1 · Service ownership | Current owner groups are recorded for Checkout and Reporting; the Warehouse dispatch owner is unverified. | Two known owner groups and a separate ownership gap. |

## What the impact brief shows

| Business service | Assessment | Reason and next check | Owner position |
|---|---|---|---|
| Customer checkout | **Observed degradation** | The journey check fails and a current dependency path reaches the affected database. Verify the failure details and other dependencies. | Checkout service owner is recorded. |
| Daily sales reporting | **Potential impact** | A current path reaches the database, but the next reporting run has not started. Check recovery against the scheduled run. | Reporting service owner is recorded. |
| Warehouse dispatch | **Needs validation** | Its dependency link is stale and no current service-health observation is supplied. Confirm the relationship and current operation. | Owner requires confirmation. |

The fixture contains **one observed service degradation, one potential impact and one unverified
service path**. These categories describe the evidence available, not three confirmed outages.
No user count, financial loss, restoration time or complete organisation-wide coverage is supplied.
Other services without a visible link are not automatically classified as unaffected.

An example management brief would say:

> The orders database connection checks and Customer checkout journey check are failing.
> The current service map links Checkout to the database through Order processing. Daily sales
> reporting also has a dependency path, but its next run has not started, so impact is potential.
> Warehouse dispatch requires confirmation because its map relationship is stale and its owner
> is unverified. Contact the recorded Checkout and Reporting owners and resolve the Warehouse
> mapping gap. No recovery action or incident priority change has been performed.

## Where MCP fits

ServiceNow already provides infrastructure and service relationship views. ViewSense should reuse
approved service-map or native impact results and add context from other products, rather than
maintaining a competing CMDB. See [ServiceNow Dependency Views](https://www.servicenow.com/docs/r/servicenow-platform/dependency-views/c_BusinesssServiceManagementMaps.html).

| Illustrative MCP capability | Information needed for this workflow |
|---|---|
| Read the incident and component | Stable incident/component IDs, environment, state, source version and assessment scope. |
| Read service dependencies or native impact results | Relationship type and direction, service types, path references, freshness, pagination and coverage limits. |
| Read service health and schedules | Time-bounded observations and planned job windows; distinguish a failed check from absent telemetry. |
| Read owners and business context | Authorized owner groups, business service definitions and approved criticality or impact rules. |
| Prepare an incident update | A draft with evidence references for review; writing or publishing it is a separately authorized step. |

These are proposed capability contracts, not claims about built-in ServiceNow MCP tool names.
Qualify the selected product MCP server, or use a ViewSense-owned adapter over its supported API.
The server must expose the required operations and preserve source access restrictions; a working
connection alone does not establish business permission or complete CMDB coverage.

## How ViewSense prepares the analysis

1. **Bind the request.** Verify the requester and resolve one incident, component, environment
   and assessment window. Match stable IDs rather than merging similar service names.
2. **Resolve the permitted graph.** Prefer the ITSM platform's approved dependency or impact
   result. Where traversal is required, apply owner-approved relationship meanings and direction,
   deduplicate services, handle cycles and bound traversal depth, result sizes and pagination.
   A hosting, ownership or network link does not automatically mean service-failure propagation.
   [ServiceNow relationship governance](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/relationship-governance.html)
   explains why relationship type and direction need consistent interpretation.
3. **Add operational context.** Read relevant health checks, incident/change records, schedules,
   redundancy and fallback evidence where supplied. A recorded backup path is not proof that
   failover succeeded. Preserve conflicting and unavailable evidence.
4. **Validate the result.** Derive paths, counts and approved impact categories through defined
   rules. The agent explains the findings and cites the sources; it must not invent dependencies,
   business criticality, financial losses, root cause or an expected recovery time.
5. **Deliver scoped views.** Responders receive permitted paths and observations; service owners
   receive their service context; management receives a minimized brief. Check current recipients
   before delivery. An incident update, notification or remediation task needs its own authority.

## Coverage and decisions remain explicit

“All linked services” means the result within the authorized scope and the source's stated
coverage. A filtered, unavailable or truncated response cannot be presented as a complete map.
Do not expose restricted service names or counts through a summary; report coverage limitations
only to the extent permitted by source policy. Record evidence versions and refresh changed or
stale observations before an operational decision.

The ITSM/CMDB owner retains service relationships and incident authority. Monitoring owners
retain health observations. ViewSense owns the proposed cross-product workflow, access checks,
evidence validation and delivery. Its independent agent runtime owns model configuration and
agent execution; all customer adaptations remain in the ViewSense tier.

An impact brief does not authorize a restart, failover, CMDB edit, priority change or public status
update. Those are separately permitted actions with their own owner decisions and execution evidence.
Untrusted instructions in tickets or tool results cannot expand the workflow's tools or audience.

## A practical first pilot

Start with this supplied graph and observations, one configured analysis agent and one authorized
report view. Verify the three distinct assessments before connecting a real service map. Native
MCP and hosted business execution remain qualification work; local preview settings do not prove
that this workflow runs through the hosted platform.

Acceptance should cover reversed relationships, cycles and duplicate paths, stale mappings,
missing owners, partial pages, inaccessible services, telemetry outages, contradictory observations,
model failure and safe delivery retries. Confirm permitted model context, retention and deletion
for service records and tool results. Measure time to a reviewed impact brief, supported findings,
coverage and reviewer corrections against the manual process.

See [adoption gates](../adoption-and-governance.md) and
[enterprise controls](../../design/high-level/60-enterprise/01-enterprise-integration-controls.md).
Browse [Detailed examples](index.md) or return to the [value and use-case tables](../value-and-use-cases.md).
