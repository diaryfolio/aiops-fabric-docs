# ViewSense AI® API and Integration Standards

## Contract families

| Capability | Canonical interface | Notes |
|---|---|---|
| public AI response | `/v1/responses` HTTP/JSON | SSE is planned |
| model inference | OpenAI-compatible `/v1/chat/completions` subset | one configured adapter; capability discovery is planned |
| local decisions | `/v1/decisions` | authenticated Ollama adapter; state + named questions; model probabilities are not authorization |
| embeddings | `/v1/embeddings` | authenticated adapter; ordered vectors with model-digest profile and dimension validation |
| memory | `/v1/memories` and `/v1/memories/search` | vendor-neutral record envelope |
| embedding backfill | `/v1/memories:reembed` | `memory.admin` at gateway; bounded tenant/owner batches; legacy vectors retained |
| MCP/tool governance | `PUT /v1/servers/{name}` and `POST /v1/tools/call` | current provider call is ViewSense AI®-owned; native MCP transport is planned |
| provider governance | `PUT/GET /v1/provider-passports/{name}`, evaluations, and `:admit` | admission is evaluated server-side |
| execution evidence | `/v1/evidence-events` | append-only API; identity derives tenant and producer |
| durable agent runs | `/v1/agent-runs`, `:resume`, `:cancel`, `/events` | idempotent create, optimistic version and ordered safe events |
| synchronous ingestion | `POST /v1/documents:ingest` | paragraph chunking and memory writes; no durable job resource yet |
| development identity | `POST /oauth2/token` | development-only client credentials and Trust Envelope minting |
| framework/channel authorisation | Governance role/mapping/binding/grant and policy decision APIs | Planned; [headless contracts](08-channel-consoles-role-mapping.md#planned-headless-apis-and-contracts) preserve legacy external-role scope fields |
| identity and policy provider adapters | Canonical verified-identity, current-entitlement and authorisation decision contracts | Planned [AuthN/AuthZ contracts](08-channel-consoles-role-mapping.md#provider-neutral-authentication-and-authorisation); provider-specific protocols/claims remain behind adapters |
| payload/egress and cost decisions | Versioned inspection, payload-bound permit and budget reservation/reconciliation contracts | Planned; see [governance requirements](09-enterprise-ai-governance-egress.md) |
| long operations | operation resources plus CloudEvents | planned |
| health | `/healthz` | must reveal no tenant/provider secrets |

FastAPI exposes runtime OpenAPI for implemented HTTP routes. Committed OpenAPI snapshots,
consumer-driven tests for every service, SSE, and CloudEvents are target gates, not current evidence.
The exact current route inventory is in
[Implementation Conformance](../00-implementation-conformance.md#implemented-http-surface).

The bundled OpenAI adapter implements the internal non-streaming chat-completions subset used by
the orchestrator. It accepts only text `system`, `user`, and `assistant` messages, discards
unrecognized outbound fields, selects the configured model server-side, and pins the upstream base
URL to `https://api.openai.com/v1`. This is an additive provider implementation; the public
`/v1/responses` contract is unchanged. The OpenAI profile defaults to server-controlled
`gpt-5.6-luna` from `config/models.env`; model changes are audited deployment configuration and
require representative quality, latency, safety, and cost evaluation rather than a caller-selected
field.

## Request context: implemented versus target

```mermaid
flowchart LR
    Request["Incoming request"] --> TLS["Required client certificate"]
    TLS --> Token["JWT issuer + audience + scope"]
    Token --> Envelope["Signed Trust Envelope tenant"]
    Envelope --> RequestID["X-Request-ID propagated"]
    RequestID --> Handler["Service handler"]
    Trace["W3C traceparent"] -. "captured inbound; full propagation planned" .-> Handler
    Deadline["End-to-end deadline"] -. "planned standard" .-> Handler
    Idempotency["Idempotency-Key"] -. "implemented for agent create only" .-> Handler
```

- `Authorization: Bearer …` with exact audience and least-required scope;
- mTLS workload identity on internal calls;
- identity-signed ViewSense AI® Trust Envelope v1 containing tenant, delegated caller, subject,
  purpose, classification, and request correlation;
- stable `X-Request-ID`; inbound `traceparent` is logged, while complete W3C propagation is planned;
- target use of `Idempotency-Key` for retriable creates and tool calls with declared idempotency;
- absolute deadline or remaining timeout budget.

The current slice implements token audience/scope, certificate-required TLS, signed tenant delegation, request ID,
provider passport/evaluation admission, optional OPA decisions, safe evidence APIs, and persistent
idempotency/version checks for agent runs. The agent events resource currently returns ordered JSON;
SSE and CloudEvents export are later compatible transports. SPIFFE identity binding, full trace propagation, and standardized
idempotency across every API remain next steps. The unsigned
`X-ViewSense-Tenant` header is rejected; it is not a compatibility mechanism.

External OIDC is terminated only at the edge. The verifier pins HTTPS issuer, JWKS, audience,
algorithms, required scopes, subject, and configured tenant claim. The edge then exchanges that
identity for an audience-specific internal token; internal services never accept the external human
token directly.

## Compatibility

The planned [channel contracts](07-input-output-channels.md#proposed-headless-contracts) add
governance-owned Input/Output Channel and route APIs plus opt-in response/tool context. Public
channel IDs are untrusted selection hints. Internal grants bind verified tenant/subject, purpose,
route/revision, action, account/field policy, expiry and budgets using a versioned authenticated
delegation extension; unsigned metadata is not authorisation. Trust Envelope v1 does not enforce
these fields today. Typed opportunities include rule/source versions, supporting facts, missing
inputs, freshness and complete/partial/unavailable coverage. Machine-readable schemas and runtime
validation must ship in the implementation repository before these APIs are marked implemented.
Old clients retain their existing path; an explicitly denied/unavailable channel cannot silently
fall back to memory or a different CRM. Route grants never broaden across a downstream hop.

- Additive optional fields are backward compatible.
- Removing/renaming fields, changing defaults, or narrowing accepted values requires a new major version.
- Unknown response fields must be ignored by consumers.
- Errors use a stable code, safe message, request ID, retryability, and optional field violations.
- Provider errors are normalized; raw vendor errors and credentials are never returned to clients.
- A deprecated major version has a published support window and telemetry-backed migration plan.

## Provider capability discovery

[Canonical adapter and model-switch requirements](09-enterprise-ai-governance-egress.md#canonical-interfaces-and-provider-transformations)
distinguish OpenAPI (HTTP contract description) from the supported OpenAI-compatible inference
subset. Provider transformations preserve approved data/identity boundaries, capabilities, safe
errors and usage semantics. Inspect the assembled context and the final translated wire payload;
an adapter transformation must not invalidate a privacy/egress decision. A provider switch must
pass the same consumer contract plus semantic/quality/residency/cost gates. Embedding changes
require profile migration. These full guarantees are planned; syntax compatibility alone is not
replaceability or governance enforcement.

Each adapter must declare model/context limits, streaming, tool calling, structured output, embedding dimensions, memory filters, export/import, and residency attributes. Routing evaluates required capabilities before cost or latency. Silent feature emulation is prohibited when it changes safety or correctness.

## Security and data minimization

Schemas distinguish data from instructions. Retrieved memory is delimited as untrusted data. Logs default to metadata only; prompt, completion, memory, and tool payload capture requires an explicit classified policy. URLs supplied through administration APIs are HTTPS-only and exact-host allow-listed to prevent SSRF.

## GUI independence

Every inference, state, identity/role, policy, lifecycle, evidence and observability capability
requires an authenticated API owned by its backend/provider. A GUI is an optional API client;
it must not be the only path to an operation or own core state. JSON/REST is used for current
ViewSense AI® contracts; selected providers can expose documented OIDC, SCIM, gRPC, OTLP or
OpenMetrics interfaces behind replaceable adapters. Current role-management and telemetry
query/export gaps remain unimplemented until API conformance is demonstrated. See the
[full headless API inventory](../design_01.md#platform-wide-headless-api-requirement).

Binary decision responses preserve `noul` and client question keys while adding `question_id`,
`probabilities` and `favored_answer`. These describe model output only. Typed OpenAPI and the
versioned response schema declare both true and false probabilities; callers never need GUI
logic to interpret a result. No permission, factual guarantee or calibration is implied.
