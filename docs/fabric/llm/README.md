# LLM Gateway Module

For native GUI access, run `make trueforge-ui` and open `http://localhost:8791`. This is a separate temporary standalone preview; see [Open TrueForge](../../deploy/trueforge-access.md) for lifecycle, certificate errors and hosted-runtime limits.

The LLM gateway provides the stable OpenAI-compatible inference boundary. Callers never receive
provider URLs or credentials. The deterministic mock and credential-isolated OpenAI adapter are
executable. The Ollama adapter adds local decisions, real embeddings and optional text chat; vLLM
and other external providers still require planned adapters.

- Runtime: `viewsense_llm_gateway`
- Bundled test provider: `viewsense_mock_llm`
- Bundled credential-isolation adapter: `viewsense_openai_adapter` (OpenAI API)
- Local provider: `viewsense_ollama_adapter`; isolated browser console: `make console`
- Helm selection: `products.llm`; opt-in embedding profile: `profiles/local-ai.yaml`
- Planned external endpoints require a ViewSense AI®-compatible mTLS/JWT adapter, explicit HTTPS trust,
  audience grants, and fail-closed egress rules. A vanilla OpenAI-compatible endpoint is not enough.

The OpenAI adapter is selected with `profiles/openai.yaml`. Only that pod receives the
`openai-credentials` Secret; it accepts the internal mTLS/scoped-token contract, fixes the configured
model server-side, minimizes outbound fields, and normalizes upstream errors without returning
credential-bearing diagnostics.

## Planned canonical routing and egress governance

[Enterprise AI governance](../../design/high-level/10-overall/09-enterprise-ai-governance-egress.md)
requires policy checks on assembled prompts/history/CRM/RAG data before external dispatch, then
validation of the actual translated wire payload and approved provider/model endpoint inside the
adapter. Unknown/uncertain PII disposition blocks external transfer or uses an approved local route.
Existing adapter field minimisation is not a PII detector or a payload-bound egress decision.

OpenAPI describes the canonical HTTP interface; the OpenAI-compatible subset is one inference
protocol. Provider adapters translate native APIs and normalise safe responses/errors/usage.
Model swaps keep ordinary client contracts but require capability, semantic/quality, residency,
privacy and cost acceptance. Embedding changes require profile migration. Full dynamic admission/
routing, inspection/egress permits, atomic budgets and complete audit evidence remain planned.

The old development OpenAI overlay, provider-switch Make targets and duplicated model-default file
are removed. Keep vendor credential isolation and the retained Helm adapter profile; real
model/streaming/tool use in the namespace-pair runtime requires separate qualification. Do not
change the fixed synthetic route by applying a historical single-namespace base or overlay.
