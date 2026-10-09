# ViewSense AI® Helm Chart

The chart is the modular installation interface. All components are independently toggled under `modules.*.enabled`; provider products are selected under `products.*`. Curated combinations live under `profiles/`; render them before installation and supply the Secrets named by the selected profile.

Examples:

```bash
# Default full reference: durable agents + mock LLM + PostgreSQL/pgvector + mock MCP
helm upgrade --install viewsense ./fabric/charts/viewsense -n viewsense-dev

# OpenAI through the bundled credential-isolation adapter; mock is omitted.
# Create openai-credentials and a CNI FQDN/egress-proxy policy (or explicit CIDRs) first.
helm upgrade --install viewsense ./fabric/charts/viewsense -n viewsense-dev \
  -f ./fabric/charts/viewsense/profiles/openai.yaml

# Mem0 OSS through the bundled zero-trust adapter
helm upgrade --install viewsense ./fabric/charts/viewsense -n viewsense-dev \
  -f ./fabric/charts/viewsense/profiles/mem0-oss.yaml

# Enterprise integration intent: Keycloak OIDC + OPA + SPIRE + n8n + OTel
helm template viewsense ./fabric/charts/viewsense \
  -f ./fabric/charts/viewsense/profiles/enterprise-suite.yaml
```

External endpoints require matching identity grants, CA trust, egress policy, and Secrets from the enterprise overlay. With the built-in NetworkPolicies, each external provider also needs an explicit `externalEgress` CIDR/port rule; an empty list fails closed. The Mem0 OSS profile instead uses an exact namespace/pod-label/port selector for its managed in-cluster server. Use a CNI FQDN policy extension when endpoint addresses are dynamic. `values.schema.json` rejects unknown product names, non-HTTPS endpoints, and malformed egress entries. For production, use immutable image digests and external secret/workload-identity integrations.

For OpenAI, only `openai-adapter` receives the `api-key` field from the configured Secret. The
adapter pins `https://api.openai.com/v1`, controls the model server-side, and needs outbound HTTPS;
production should use an egress proxy or CNI FQDN policy rather than a broad Internet CIDR.

The enterprise profile declares desired integrations; it does not install cluster-scoped Keycloak,
SPIRE, n8n, or OpenTelemetry operators. Platform teams install those upstream products with pinned
versions and then run the conformance checks in `tests/README.md`. OPA is different: when selected as
`opa-sidecar`, the chart installs a local fail-closed policy decision point beside governance.

The SPIRE socket/trust-domain, workflow product, and `otlpEndpoint` values are reserved intent: no
SVID consumer, workflow adapter, or native application OTLP exporter is rendered today. JSON stdout
can be collected independently. `vllm` and generic external LLM values likewise require a future
ViewSense AI®-compatible authentication adapter and must not be treated as a working vanilla endpoint.

## Ollama and real embeddings

The opt-in `profiles/local-ai.yaml` packages the Ollama adapter and memory embedding client. It
requires operator-provided TLS/identity grants and approved upstream HTTPS egress; it does not
install Ollama or model weights. Adapter config mutation is disabled in this chart. The loopback
browser console is launched separately with `make console` and is development-only. See the
[local console design](../../../design/high-level/10-overall/06-local-ai-console.md).

## Management and certificate APIs

The detachable management console consumes the gateway APIs. Suite selection produces a reviewable
plan; it does not deploy upstream products. `products.identity.providersSecret` mounts an operator-owned
OIDC registry and `providerCaSecret` mounts its CA. Public edge TLS requires a registry; internal hops
still require mTLS. `products.certificates.enabled` installs the separate certificate metadata service.
Provide its TLS Secret, broker grants and public inventory ConfigMap. Enable `certManagerEnabled` only
after installing the operator and supplying exact `apiServerEgress` CIDRs/ports. `renewableNames` limits
both the application and Kubernetes status-patch RBAC. No Secret-read permission is granted. See the
[Keycloak and certificates operating guide](../../../deploy/integrations/keycloak.md).

## Networking and mesh profile

`profiles/networking-ambient.yaml` is an application profile for independently installed Cilium
and Istio ambient controllers. It renders STRICT peer authentication, default-deny authorization,
exact source ServiceAccount/port rules from the neutral flow graph, scoped HBONE access and
distinct database accounts. The gateway's optional public-evidence ConfigMap is read-only.
Install provider releases and validate traffic before treating this profile as accepted. The graph
covers the base suite; optional providers require explicit graph/egress extensions and acceptance.
See the [networking guide](../../../deploy/integrations/networking.md) and conformance record.
