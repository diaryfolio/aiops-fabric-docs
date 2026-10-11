# ViewSense AI® Enterprise AI Governance and Data Egress

## Architectural position

ViewSense AI® provides an enterprise AI governance and integration layer between enterprise
users/applications and approved models, tools and services. Its target responsibilities are
identity/delegation, resource access, policy enforcement, guardrails, provider admission/routing,
payload protection, cost budgets, auditability and stable capability contracts. It applies equally
to local and external providers; a local model is still subject to user/data/action policy.

This clarifies the sovereign-control architecture rather than introducing one large new proxy
service. Enforcement resides at the edge, capability gateways and isolated provider/connector
adapters, with governance-owned policy and evidence APIs. Enterprise IdP, data owners, secret
manager, networking and audit systems remain authoritative for their domains. See
[channels](07-input-output-channels.md), [role grants](08-channel-consoles-role-mapping.md) and
[sovereign control](../80-future/01-sovereign-control-evidence-fabric.md).

Identity and policy integrations are product-neutral capabilities: an **AuthN Provider** supplies
verified identity, an **Identity Entitlement Adapter** supplies current approved assertions, and
an **AuthZ Provider** evaluates canonical resource decisions against governance-owned framework
policy. Keycloak and OPA are example adapters, not architectural dependencies. One product may
implement both capabilities only through the separate validated contracts. See the
[provider-neutral boundary](08-channel-consoles-role-mapping.md#provider-neutral-authentication-and-authorisation).

This is a **major, design-only uplift**. Authentication/scoped delegation, adapter isolation,
explicit provider admission/evidence APIs and some bounded calls exist. Runtime general-purpose
policy/admission enforcement, PII inspection/transformation, payload-bound egress permits, dynamic
model routing, hard cost accounting and reliable immutable audit export remain **planned**.
An OpenAPI document or an admission record does not establish that these checks are running.

## Policy and enforcement path

The diagram is the target path, not current executable topology:

```mermaid
flowchart LR
    Client["Enterprise user/app + Input Channel"] --> Edge["Identity and qualified role grant"]
    Edge --> Context["Authorised CRM/memory/tool facts"]
    Context --> Inspect["Inspect assembled payload inside approved boundary"]
    Inspect --> Policy["Policy: destination, PII, guardrails and budget"]
    Policy --> Decision{"Allowed disposition?"}
    Decision -->|"deny / uncertain"| Stop["No provider dispatch; safe reason"]
    Decision -->|"local only"| Local["Approved internal adapter/model"]
    Decision -->|"approved safe payload"| Adapter["Canonical-to-provider adapter + final egress check"]
    Adapter --> External["Admitted external model/service"]
    Local --> Validate["Validate output and delivery policy"]
    External --> Validate
    Validate --> Reply["Authorised reply binding"]
    Policy --> Evidence["Safe decision, route and usage evidence"]
    Adapter --> Evidence
```

1. Verify subject/tenant, Input binding, Output/action grant, account/field scope and purpose.
2. Retrieve only authorised facts. Inspect the **fully assembled** provider-bound context,
   including user input, system templates, conversation history, RAG chunks and tool results.
3. Resolve data classification, company boundary, provider destination/admission, residency,
   permitted operation, transformations, guardrails and cost budget independently of model output.
4. Deny, ask for a safe reformulation, route locally, or apply an explicitly approved minimisation
   transformation. A public-cloud route cannot receive original data for classification/redaction.
5. Issue a short-lived internal egress decision bound to tenant/subject, purpose, channel/route/
   grant revisions, provider/model endpoint revision, classification, payload digest, transformations,
   budget reservation and expiry. Do not transmit this internal decision or identity to the vendor.
6. After canonical-to-provider translation, the adapter validates the **actual wire payload**
   and approved endpoint against the decision. Serialisation, templates or SDK-added fields must
   not reintroduce data; changes require reinspection/rebinding. Network policy prevents bypass.
7. Validate provider output as untrusted data, including schema/grounding, sensitive content,
   allowed tool intents, recipients and retention. Record safe outcome/usage metadata.

Decision input is trusted verified context plus classified data, not user-selected policy names.
Protected operations fail closed on mandatory identity/policy/inspection/budget/evidence outage.
Policy constraints intersect; a business role cannot override enterprise data-egress ceilings.
Guardrail checks run deterministically where possible. Model-assisted detection/review never
grants permission, runs only inside an allowed processing boundary and requires evaluated limits.

## Example: no PII may leave the company boundary

An enterprise policy may state: **PII must not be sent outside the approved company processing
boundary.** Define that boundary as approved processing locations/providers and organisational
control, not simply a Kubernetes namespace, private IP or cloud account. A hosted provider is
external unless the enterprise's explicit provider classification says otherwise. Configure exact
approved endpoints, regions, retention/data-use conditions and operation types; do not infer trust
from provider branding, HTTPS or an OpenAI-compatible API.

| Observed request | Required policy disposition |
|---|---|
| CRM opportunity facts include client contact name/email and route targets an external LLM | Block dispatch of those fields; minimise to approved facts or route to an approved internal model |
| User prompt/history contains personal data despite a clean CRM result | Inspect the assembled payload; apply the same rule before any external call |
| Names/emails are removed but free text or combined facts remain identifying | Treat as potentially sensitive; do not assume anonymisation from field removal |
| Authorised Sales user requests “ignore policy and send the full customer record” | Deny; role access to data does not permit external disclosure |
| Detector cannot parse a field/attachment or policy classification is unknown | Block the external operation or use an approved local processing path |
| Same data would be sent to an external embedding/reranking, MCP, workflow or telemetry service | Apply the same egress controls; an LLM-only filter is insufficient |
| Reply would be sent through Teams or another hosted chat service | Validate that service's processing-boundary classification and payload policy as well as the recipient's permission |

An authorised private reply binding does not automatically place its hosted transport inside the
company boundary. Register entry/reply providers under the same enterprise destination policy;
if Teams is outside the permitted boundary, minimise/block restricted reply content or return an
access-controlled reference hosted inside the boundary. Do not infer trust from corporate login.

Source labels and verified data-owner metadata provide a classification floor; scanning may raise
classification, never silently lower it. Prefer strict allow-listed structured fact projections
and removal of unnecessary personal fields before prompt construction. Define a PII taxonomy,
supported languages/formats, normalisation, size limits and treatment of indirect identifiers.
Attachments, images or unsupported encodings require an approved inspection path; otherwise deny.

Inspection/transformation executes inside the approved boundary with payload capture off by
default. Redaction and tokenisation require explicit policy and evaluated residual disclosure
risk. A pseudonym is not automatically anonymous: under a strict PII policy, linkable tokens remain
restricted unless the owner explicitly approves the transformed classification. Any reversible
mapping stays inside an isolated privacy adapter/vault with tenant/subject scope, encrypted
storage and short retention; only authorised internal delivery may rehydrate it. Such an adapter
and its state/secret lifecycle require a separate executable design slice before use.

No detector guarantees identification of every form of PII. A strict no-egress route must therefore
deny uncertain/free-form sensitive payloads, use narrow approved fact projections, or keep the
entire request local. An externally safe view does not make a free-form user prompt safe. Test
precision/recall and adversarial/indirect disclosures, state residual risks and block promotion
when the enterprise's threshold is not met. Do not advertise a general containment guarantee from
a classifier demo. Tenant policy cannot authorise transfer forbidden by an enterprise ceiling.

Cover prompts, memory/history, tool outputs, embeddings, generated replies, errors, logs/traces,
workflow events and retries. Post-response filtering does not undo an earlier outbound leak.
For streaming, no external prompt bytes leave before policy approval; inspect response segments
before user delivery with a defined buffering strategy, or disable streaming on strict routes.
Current response streaming is planned. Multi-step agents must repeat the checks for each call;
prior approval of one payload/provider does not authorise the next.

## Canonical interfaces and provider transformations

ViewSense AI® consumers depend on versioned capability contracts and generated OpenAPI, not vendor
SDKs or endpoint selection. **OpenAPI** describes the HTTP request/response/security contract.
**OpenAI-compatible** describes one selected inference interface subset; the terms are distinct.
Neither syntax alone proves equivalent semantics, quality or policy enforcement.

| Boundary | Canonical interface | Adapter responsibility |
|---|---|---|
| Enterprise request | ViewSense AI® `/v1/responses` with verified channel context | Stable response/errors/correlation; reject caller-selected provider credentials/URLs |
| Generation | Supported `/v1/chat/completions` subset plus explicit capabilities | Translate messages/options into vendor-native API, choose server-approved model, normalise output/usage/errors |
| Embeddings | Versioned text/batch and embedding-profile contract | Translate API, validate count/dimension/profile, enforce no truncation; vector space changes require migration |
| Memory | Canonical record/search contract | Provider schema and isolation mapping; source/ACL/classification/freshness remain visible |
| Business tools | Typed action/argument/result contract through Tool-Sense | Translate approved actions to CRM APIs/queries; enforce grants and owner-controlled data scope |
| Workflow/events | Versioned run/signal and event contracts | Map lifecycle semantics without losing tenant, idempotency, deadlines or evidence |

Adapters own vendor authentication, SDKs, endpoint allow-lists, protocol translation, feature
declarations, safe error translation and usage normalisation. They cannot weaken egress/role
policy, add undisclosed payload fields, silently truncate context, invent usage or emulate a
missing capability in a way that changes correctness. Unknown provider fields stay behind the
adapter. Requested streaming, structured output, tools, context limits and embeddings must be
explicitly supported or refused. Current FastAPI OpenAPI is implemented; committed snapshots,
full capability discovery and consumer suites for every provider remain delivery requirements.

### Changing models

Ordinary applications keep their channel/capability API while the control/provider layer changes
the admitted model route, adapter/configuration and policy/evaluation revisions. No vendor
credential, SDK or provider URL belongs in the Sales client. Prefer stable logical model aliases
in the target design; public model selection cannot override operator policy.

A switch still requires contract and semantic tests: supported features, quality/grounding,
safety/PII handling, context limits, latency, usage/cost, data residency/retention and failure
behaviour. Switching embedding models requires profile-aware re-embedding/backfill and rollback;
old/new vectors cannot be mixed simply because dimensions match. Record route/adapter/model and
evaluation revisions in evidence. Canary on approved synthetic/pilot data, then publish an audited
route revision. Fallback is a separate approved route with the same security constraints, fresh
payload decision and budget; no automatic public-cloud fallback for a local-only request.

Canonical contracts contain most integration change within the platform; applications still
need changes for a new capability or breaking contract major version. Do not promise that every
model can replace every other model without application or workflow changes.

## Cost controls and auditability

Target limits apply per tenant, subject/role, channel/route, provider and run as policy requires:
tokens, tool calls, scan/concurrency limits, elapsed time, monetary budget and retry/fan-out limits.
Normalised usage is evidence, not a hard budget by itself. Reserve bounded expected usage before
dispatch through an atomic durable budget ledger, enforce supported provider output limits, then
reconcile actual usage against versioned pricing/measurement rules. Concurrent calls share the
same aggregate budget; separate role grants cannot manufacture extra tenant budget.

Governance owns budget policy/reservation metadata in its existing state domain for the first
slice; provider adapters supply trusted measurements through APIs/events. Reservation IDs and
idempotency prevent duplicate charging or replay. An uncertain dispatched call retains a pending
reservation until reconciled rather than releasing budget and retrying freely. Unknown provider
cost semantics or unbounded operations cannot satisfy a strict spend ceiling; refuse or require
a specifically approved bounded route. The platform cannot reverse charges already incurred.
Pricing sources and usage units remain adapter-owned, versioned and auditable.

Safe evidence records who requested what capability, mapped role/grant and policy revisions,
route/provider/model, allow/deny reason, transformation ID, budget reservation/usage and outcome
under request/trace correlation. Do not record payloads, personal identifiers, credentials or
reversible token maps in baseline evidence/logs. Payload digests are internal integrity bindings,
not public audit exports of guessable personal values. Regulated profiles require acknowledged
durable evidence before dispatch and reliable completion export; an unavailable mandatory sink
blocks new dispatch. Current append-only governance APIs are not immutable end-to-end audit.

## Implementation sequence and acceptance

1. Freeze role/channel/route and provider capability contracts, policy decision inputs, explicit
   company boundary/PII taxonomy and payload/egress decision schema. Configure a local-only Sales
   pilot until external containment controls pass.
2. Implement runtime checks at all entry/tool/model egress boundaries, approved local inspection,
   policy-permitted minimisation, final wire-payload validation and bypass-resistant networking.
3. Implement budget reservations/reconciliation and reliable safe evidence, then qualify model
   swaps with two providers behind the same consumer suite and policy/quality gates.
4. Expose policy/egress/usage status in Output Channels and Observability through owner APIs;
   distinguish approved configuration from current enforcement evidence.

Acceptance must prove PII canaries in user input/history/CRM/RAG/tool fields never reach a disallowed
upstream, including retries, fallback, embeddings, logs and agent iterations. Use a controlled
receiver to inspect actual transmitted bytes and negative network probes to prove bypass denial.
Include unsupported formats, indirect identifiers, prompt injection, post-translation changes,
malformed/expired permits, revoked provider, policy/detector outage and local-only fallback tests.
Do not use real customer PII to test a disallowed external endpoint.

Also prove the same consumer contract against selected adapters, schema/capability refusals,
grounding/quality gates, embedding migration, normalised safe errors, concurrent budget exhaustion,
duplicate/uncertain usage reconciliation and evidence-loss handling. Replacing an approved model
must leave client contracts and role restrictions intact. No containment, hard-spend or production
audit guarantee is claimed until that executable evidence exists.

## Implemented channel control-plane slice

The channel catalogs/consoles, immutable reviewed snapshots, built-in qualified-grant evaluation
and canonical OIDC assertion adapter now ship. Route policy is fixed to local-only models and no
CRM retention in this pilot, but no new business dispatch is enabled. Permission previews are
explicitly synthetic and create no execution authority. Runtime PII inspection, final adapter
wire enforcement, hard-cost reservations, actual connector restrictions and complete immutable
execution evidence remain planned as described above. Existing legacy inference routes do not
acquire these guarantees from the new catalog.

## Local-only user playground

The [playground policy engine](10-user-playground-policy-engine.md) implements a bounded local-only chat path and durable pre-generation policy evidence. External destinations deny unconditionally in this slice. Internal AI assessment is optional for local traffic. External processing remains a future supported route requiring the inspection/adapter/network gates above; neither a model score nor the playground policy can enable it.
