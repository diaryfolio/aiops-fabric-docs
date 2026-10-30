# Supplier assurance and renewal decision

A critical supplier is approaching renewal. ViewSense AI® brings together commercial, security
and operational evidence so procurement, risk and business owners can make an informed decision.

> **Proposed workflow.** Supplier, contract, assurance and service connectors and governed report
> delivery require implementation and acceptance. The scenario below is fictional; no supplier
> has been assessed. See [current capabilities](../../design/high-level/00-implementation-conformance.md).

## The business question

> Should we renew our customer-support supplier? Show the cost change, unresolved security
> findings and business dependencies. Identify what needs resolving and who must decide.
> Do not accept a contract, approve a risk exception or change supplier access.

The value is a shared evidence pack across departments: Procurement can see the commercial
position, Security can see assurance gaps, and the service owner can see the consequences of
continuing or replacing the supplier. Each receives only the information they may access.

## The workflow at a glance

1. **Connect the supplier evidence**

    Gather approved contracts, assessments, findings and service dependencies for one supplier.

2. **Prepare the renewal brief**

    Compare evidence with approved renewal criteria and separate facts, gaps and proposals.

3. **Put decisions with their owners**

    Give Procurement, Risk and the service owner the relevant evidence and outstanding decisions.

## A synthetic renewal review

**Supplier A** is a fictional customer-support service used by three internal teams.
The example considers one supplier legal entity, one service and one proposed renewal term.
References below are fictional evidence identifiers, not links to live systems.

| Evidence | Supplied observation | What the brief can say |
|---|---|---|
| SUP-1 · Supplier and service register | Three teams depend on the service; it handles customer contact details and ticket content. | The service has an established business dependency and needs a data-owner review. No customer count or breach is established. |
| COM-1 · Finance-checked commercial comparison | Annual fixed fees rise from £120,000 to £132,000 for the same service scope and currency, excluding tax and usage charges. | Comparable fixed fees increase by £12,000, or 10%. This is not a total-cost-of-ownership estimate. |
| ASS-1 · Security findings register | Two findings remain open: an overdue privileged-access review and missing evidence of a restore test. | Both findings need owner review and evidence. Missing restore evidence does not prove recovery will fail. |
| EXC-1 · Risk exception register | The earlier acceptance for the overdue access review has expired. | The old acceptance cannot be presented as a current approval. An authorized risk owner must determine the next step. |
| DOC-1 · Assurance report and service scope | The report covers the named service but excludes a newly proposed downstream data processor. | The report does not establish assurance coverage for the changed processing arrangement. |
| OPS-1 · Approved service report | The report records the agreed availability target as met in each of the last three complete reporting months. | Recorded availability met that target for that window; it does not resolve security findings or prove future resilience. |
| DEP-1 · Continuity plan | The service owner has a documented fallback, but no exercise result is supplied. | The fallback is documented; its effectiveness remains unverified. |

The fixed-fee comparison is calculated before model analysis:
**£132,000 − £120,000 = £12,000**, and **£12,000 ÷ £120,000 = 10%**.
Source owners must confirm that the two amounts describe the same scope and period. Usage,
transition costs and alternative supplier pricing are outside this fixture.

## What the decision pack looks like

Keep commercial, service and assurance findings separate. A lower price or good uptime must not
silently offset a mandatory security or data-handling requirement.

| Decision area | Position in this fixture | Next owner decision |
|---|---|---|
| Commercial | Comparable annual fixed fee increases by 10%. | Procurement and Finance review value and negotiation options. |
| Assurance | Two open findings, an expired exception and incomplete processor coverage. | Security, the risk owner and data owner determine required evidence and approvals under the applicable policy. |
| Continuity | Three teams depend on the service; fallback testing is not evidenced. | The service owner reviews continuation and transition options before proposing a service change. |
| Renewal readiness | Evidence and approval gaps remain unresolved. | The authorized owners decide whether renewal criteria are met and record the rationale. |

An example executive narrative would be:

> Supplier A serves three internal teams. The comparable annual fixed fee increases by
> £12,000 (10%), and the supplied service report records its availability target as met for the
> last three reporting months. Renewal preparation still has unresolved assurance issues:
> two open findings, an expired risk exception and missing coverage for a proposed data processor.
> The fallback plan has no supplied exercise result. Obtain the missing evidence and authorized
> owner decisions before presenting the renewal as approved. No contract or access changes were made.

The pack can describe options for review: renew when approved criteria are satisfied, consider a
limited extension only where policy and authorized owners permit it, or assess a replacement.
It does not invent permission for an extension, recommend an untested cutover or issue a legal
opinion. Risk acceptance and contract interpretation stay with the designated owners.

## Different views for different teams

| Recipient | Permitted example output |
|---|---|
| Procurement and Finance | Commercial comparison, service scope and negotiation questions; only the assurance details their grants permit. |
| Security and risk owners | Relevant findings, exception status, evidence references and proposed follow-ups. |
| Business service owner | Dependencies, continuity gaps and decisions affecting service operation. |
| Authorized management sponsor | A minimized summary of cost, business dependency, assurance gaps and pending decisions. |
| Supplier contact | Only explicitly approved questions or an approved extract, not internal risk deliberations or other teams' records. |

These are illustrative business grants, not rights conferred by console role names. Restrict
sources and model context before analysis, then check current recipients before delivery. A
shared privileged session followed by redaction is not sufficient audience isolation.

## How ViewSense prepares the result

1. **Fix the scope.** Verify the requester and bind the supplier legal entity, service, contract,
   renewal version, permitted evidence window and approved decision criteria. Similar supplier
   names or an assurance report for another product must not be silently matched.
2. **Collect permitted evidence.** Use scoped read-only connectors with source references, versions,
   coverage and freshness indicators. Minimize personal information and restricted commercial
   terms. A missing source produces an explicit coverage gap.
3. **Apply defined checks.** Calculate comparable costs, reconcile finding and exception states,
   and verify report scope against owner-approved rules. The model explains the results; it
   does not invent risk scores, policy thresholds, assurance claims or contractual obligations.
4. **Review the draft.** Validate citations and calculations, distinguish supplier assertions
   from independently verified evidence, and surface conflicts. Supplier questionnaires and
   attachments are untrusted information, never instructions to change workflow or recipient rules.
5. **Deliver and record the decision.** Send the scoped draft for review. The future workflow
   must distinguish draft generation, approval, delivery and the owner's actual decision.
   Recording a recommendation does not close a finding or approve a renewal.

## Responsibilities and operating limits

Business systems remain authoritative for supplier, financial, finding and approval records.
ViewSense owns the proposed integration scope, access checks, result validation and delivery.
Its independent agent runtime owns model configuration and the execution loop; all customer
adaptations remain in the ViewSense tier through supported interfaces.

A practical first pilot uses the supplied facts, one configured analysis agent and one authorized
report view. The preview and hosted runtime currently have separate state; preview configuration
alone does not demonstrate that this workflow executes through the hosted platform.

Before connecting live supplier information, qualify wrong-supplier and unauthorized-recipient
denial, expired exceptions, stale or conflicting evidence, malicious attachment instructions,
model failure and duplicate delivery. Recheck changed evidence before a decision. Confirm
retention and deletion requirements for prompts, attachments and results as well as application
logs. Report generation and delivery need separate failure states and safe retry behavior.

Measure time to an accepted brief, evidence coverage, factual corrections and reviewer effort
against the manual process. No measured savings or certification is established by this example.
See [adoption gates](../adoption-and-governance.md) and [enterprise controls](../../design/high-level/60-enterprise/01-enterprise-integration-controls.md).

For background on identifying, assessing and mitigating supplier cybersecurity risk, see
[NIST SP 800-161 Rev. 1](https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final).
This walkthrough is an illustrative application, not a complete control checklist or a claim of NIST certification.

Browse [Detailed examples](index.md) or return to the [value and use-case tables](../value-and-use-cases.md).
