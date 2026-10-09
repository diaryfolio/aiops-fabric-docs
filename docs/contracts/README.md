# ViewSense AI® Machine-Readable Contracts

These schemas are the portable boundary between independently replaceable components. Runtime models and contract tests must evolve with them. Provider payloads stay behind adapters; callers exchange ViewSense AI®-owned envelopes only.

- `trust-envelope-v1.schema.json` describes identity-signed tenant, purpose, subject, and classification context.
- `provider-passport-v1.schema.json` describes admission input for a model, memory, MCP, workflow, agent, or ingestion provider.
- `evidence-event-v1.schema.json` describes payload-minimized execution evidence input. The API derives producer and tenant from authenticated identity.
- `agent-run-v1.schema.json` describes durable run creation, bounded budgets, lifecycle state,
  optimistic versioning, and ordered safe events.
- `decision-request-v1.schema.json` describes state and named `noul`/`choice`/`score` questions.
  Models are selected server-side; question criteria and probabilities are validated at runtime.
- `embedding-request-v1.schema.json` describes text or text-batch input. The adapter returns ordered
  vectors, model/revision, profile, dimensions, input token metadata and duration. Runtime validation
  bounds batches, forbids truncation and rejects zero/non-finite or dimension-incompatible vectors.

Schemas are versioned rather than silently changed. Breaking field or semantic changes require a new major contract and migration plan.

`model-test-request-v1.schema.json` is an additive opt-in administrative contract for installed-model
decision, embedding and text-chat previews. It accepts a selected model only at `/v1/model-tests`,
requires `provider.admin`, and never changes saved configuration or memory profiles. Conditional
input validation and capability checks run server-side. Ordinary inference remains server-pinned.

Ollama text chat uses native `POST /api/chat` with `stream: false` behind the existing internal
`choices[].message.content` completion envelope. Final assistant content is required; model mismatch
and incomplete or malformed replies fail with a sanitized error. Additive `usage` and
`provider_timing` metadata contain non-negative token counts and durations in milliseconds; vendor
`thinking` and diagnostics are excluded. The local chat preview allows a 240-second total upstream
deadline and a 260-second console hop. These do not extend public gateway/orchestrator budgets.

`decision-response-v1.schema.json` adds explicit binary probabilities, `question_id` and
`favored_answer` for `noul` answers. Legacy `noul` values and request question keys are preserved.
No Boolean authorization is inferred. Consumers must tolerate additive fields. Typed OpenAPI
exposes the same contract at the model adapter independently of the GUI.

`oidc-provider-v1.schema.json` is operator-owned provider configuration: pinned issuer/audience,
HTTPS endpoints, claim paths, explicit role-to-scope mappings and optional server-side browser client
credentials. Redirect validation permits HTTP only for explicit development loopback. Duplicate
issuers/IDs, incomplete browser configuration and unknown scopes are rejected. No API accepts a
caller-selected issuer, JWKS URL, tenant or role mapping.

`certificate-inventory-v1.schema.json` covers public metadata and inventory completeness. It forbids
extra metadata fields; PEM and private keys are never exposed. Certificate renewal accepts
`{"resource_version":"123"}` and returns HTTP 202 with `status: accepted`, `id`,
`previous_revision` and `workload_reload: operator_required`. Only approved non-CA resources in
configured namespaces may be renewed. Stale versions or active issuance return 409; insufficient
scope or missing renewal label returns 403; a disabled/unavailable controller returns 503.

The edge OpenAPI advertises bearer JWT security and model/certificate schemas. Internal certificate
API access additionally requires workload mTLS. Provider inventory is public login metadata;
verified context, role policy, suite plans and component operations require their documented scopes.
Suite plans have `applied:false` and report integration blockers; they never perform deployment.

Networking contracts are additive: `network-topology-v1.schema.json` declares unique workload
ServiceAccounts and exact allowed source/destination/port edges; no wildcard principal is accepted.
`network-evidence-v1.schema.json` contains only operator-produced public test metadata, pinned
versions, topology digest, timestamp and pass/fail results. Evidence must match the selected cluster
and topology, contain the complete required checks and be less than ten minutes old to represent
a verified observation. It never reports continuous health. Missing, malformed, incomplete, stale,
mismatched and failed evidence have distinct visible states. Networking plans are typed, scoped,
headless and `applied:false`; no API takes a kubeconfig, executes kubectl or hot-swaps a CNI.
