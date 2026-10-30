# Value and use cases

ViewSense AI® brings together permitted information, AI-assisted analysis and reviewed outcomes.
Choose a team below. Linked titles open a walkthrough under **Detailed examples**.

Product-suite integrations in these target workflows primarily use approved MCP tools and
resources. ViewSense combines their results with business rules, review and delivery; a product
without a suitable MCP server needs an adapter over its supported API.

> **Proposed workflows.** Business connectors, governed tools and delivery still require
> implementation and acceptance. See [current capabilities](../design/high-level/00-implementation-conformance.md).

## Security, risk and supplier assurance

Five selected examples cover security operations (SOC), governance/risk/compliance (GRC) and
cybersecurity supply-chain risk.

| Example | ViewSense brings together and compares | Outcome and recipients |
|---|---|---|
| S1 · Suspicious privileged access | Sign-in alerts, administrator activity, approved changes and service ownership | SOC analysts receive an evidence timeline and unanswered questions; service owners receive relevant exposure. |
| S2 · Vulnerability business impact | Scanner findings, deployed versions, exploitation advisories and service criticality | Security receives a rule-based priority review; engineering receives affected components and owners. |
| G1 · Change-approval audit evidence | Production releases, change tickets, approvals and recorded exceptions | Control owners receive evidence gaps; reviewers receive linked records for assessment, without an automatic compliance verdict. |
| C1 · Supplier breach impact | Supplier notices, connected services, data-sharing records and access grants | Security receives exposure questions; business owners receive dependencies; procurement receives supplier follow-ups. |
| C3 · [Supplier assurance and renewal](examples/supplier-assurance-renewal.md) | Assessments, open findings, contract terms, service history and business dependencies | Procurement and risk owners receive a renewal brief with evidence gaps, conditions and decisions for authorized owners. |

## People and HR

| Example | ViewSense brings together and compares | Outcome and recipients |
|---|---|---|
| HR1 · [Reorganisation and business performance](hr-departure-workflow.md) | Six months of confirmed HR exits, department mappings, staffing and financial measures | Authorized leaders receive comparative charts and an explanation of evidence limits. |
| HR2 · Employee onboarding readiness | Confirmed starters, role requirements, equipment and training records | HR receives readiness gaps; IT and managers receive proposed tasks for review. |
| HR3 · Workforce capacity planning | Approved workload forecasts, staffing, skills and leave coverage | Department managers receive aggregate capacity gaps and planning scenarios, without individual performance rankings. |

## Finance

| Example | ViewSense brings together and compares | Outcome and recipients |
|---|---|---|
| FIN1 · Invoice discrepancy review | Invoices, purchase orders and goods receipts | Finance receives matched records and discrepancies; procurement receives supplier questions. |
| FIN2 · Budget variance explanation | Approved budgets, actual expenditure, commitments and department mappings | Budget owners receive validated variances, supporting transactions and questions requiring explanation. |
| FIN3 · Cloud cost and capacity review | Billing, utilization, workload schedules and ownership records | Finance and platform owners receive cost drivers and candidates to investigate, without automatic resource changes. |
| FIN4 · Software licence optimization | Identity, software inventory, measured usage and purchasing records | Finance and asset owners receive unused or duplicate licence candidates and renewal questions for review. |

## Sales, customer service and product

| Example | ViewSense brings together and compares | Outcome and recipients |
|---|---|---|
| CX1 · Sales opportunity discovery | CRM accounts, product usage and contract entitlements | Account managers receive evidence-backed opportunities for their permitted customers. |
| CX2 · Customer support resolution | Support tickets, approved documentation and service status | Support agents receive a response draft; engineering receives unresolved technical findings. |
| CX3 · Customer renewal preparation | Customer contract milestones, adoption, support history and account plans | Account owners receive a renewal brief with observed concerns and follow-ups, without invented churn probabilities. |
| CX4 · Customer feedback to product priorities | Support cases, customer feedback, product analytics and engineering backlog | Product managers receive recurring problems with source evidence and proposed backlog items for review. |

## Procurement and legal

| Example | ViewSense brings together and compares | Outcome and recipients |
|---|---|---|
| PROC1 · Supplier commercial renewal | Supplier contracts, usage, prices and service history | Procurement and Finance receive comparable costs and negotiation questions; assurance concerns link to the separate security review. |
| PROC2 · Supplier delivery exceptions | Purchase commitments, promised deliveries, receipts and affected work | Procurement receives supplier follow-ups; operations receives dependencies and confirmed delays. |
| PROC3 · Contract obligation tracking | Approved obligations, notice periods, assigned owners and completion evidence | Contract owners receive upcoming obligations and missing evidence; legal reviewers receive questions requiring interpretation. |

## Operations and project delivery

| Example | ViewSense brings together and compares | Outcome and recipients |
|---|---|---|
| OPS1 · [ITSM service dependency and impact](examples/itsm-service-impact.md) | ServiceNow or another ITSM service map, incident records, monitoring and service owners through MCP | Responders receive dependency paths; business owners receive observed, potential and unverified impacts. |
| OPS2 · Project delivery health | Milestones, work tracking, incidents and dependency updates | Project managers receive blockers; sponsors receive scoped delivery concerns and owner decisions. |
| OPS3 · Service-demand planning | Request volumes, approved service targets, staffing and backlog age | Operations managers receive validated demand trends and capacity scenarios for review. |

## Engineering and DevOps

| Example | ViewSense brings together and compares | Outcome and recipients |
|---|---|---|
| ENG1 · [Deployment-failure investigation](deployment-failure-investigation.md) | Release identity, rollout status, selected telemetry and approved runbooks | On-call engineers receive findings and proposed checks; service owners receive a scoped brief. |
| ENG2 · CI and test-failure triage | Failed builds, test results, sanitized job logs and source changes | Developers receive a failure summary, supporting evidence and hypotheses to verify. |
| ENG3 · API-change impact analysis | Proposed contracts, known consumers and contract-test results | API owners receive evidenced compatibility risks; consuming teams receive migration and testing proposals. |

## Logistics and manufacturing

| Example | ViewSense brings together and compares | Outcome and recipients |
|---|---|---|
| LM1 · Order-to-delivery disruption | Order management, warehouse stock, carrier tracking and CRM through MCP | Operations receives affected orders and recovery options; account owners receive customer-specific update drafts. |
| LM2 · Quality complaint and batch traceability | Customer complaints, quality records, production batches and component traceability through MCP | Quality and Engineering receive shared batch/component evidence, coverage gaps and investigation proposals. |

## Facilities, energy and continuity

| Example | ViewSense brings together and compares | Outcome and recipients |
|---|---|---|
| FAC1 · Maintenance before disruption | Equipment observations, maintenance history, spare parts and operating schedules through MCP | Maintenance owners receive an evidence-backed work proposal and operational dependencies; no equipment changes are automatic. |
| FAC2 · Energy-use investigation | Meter readings, site activity, facilities records and approved conversion factors through MCP | Facilities and sustainability teams receive comparable trends, missing measurements and investigation candidates. |
| FAC3 · Business continuity preparedness | Business-process dependencies, service catalog, continuity plans and exercise records through MCP | Process owners receive dependencies, untested fallback assumptions and preparedness tasks for review. |

## Data and research

| Example | ViewSense brings together and compares | Outcome and recipients |
|---|---|---|
| DR1 · Conflicting business figures | CRM, billing, Finance reports and data-catalog definitions through MCP | Data and business owners receive a reconciliation of definitions, periods and records, with unresolved differences assigned for review. |
| DR2 · Reuse previous research | Experiment records, internal documents, source repositories and issue tracking through MCP | Researchers receive referenced prior approaches, conflicting results and unanswered questions within their permitted scope. |

These examples begin with read-only analysis and human review. Calculations and comparisons use
approved rules; AI helps explain the evidence. Missing information remains visible. A report does
not authorize payments, contract acceptance, account changes or production operations.

Continue to [Detailed examples](examples/index.md) for the walkthroughs, or
[Adoption and governance](adoption-and-governance.md) to plan a pilot.
