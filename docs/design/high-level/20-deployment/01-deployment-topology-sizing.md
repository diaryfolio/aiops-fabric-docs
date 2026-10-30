# ViewSense AI® Kubernetes Deployment Design

## Canonical packaging

Kubernetes is the deployment contract. The portable base uses Deployments, StatefulSets, Services, Secrets, PVCs, probes, resource controls, service accounts, and NetworkPolicy. EKS, GKE, AKS, OpenShift, and bare-metal differences belong in overlays. Docker Compose mirrors process/network boundaries only and is not a production topology.

```mermaid
flowchart TB
    subgraph Namespace["viewsense-dev reference namespace"]
      subgraph Stateless["Deployments"]
        Edge["gateway"]
        Control["fabric gateways"]
        Providers["mock/provider adapters"]
        Admin["governance + ingestion"]
      end
      subgraph Stateful["Single-replica development StatefulSets"]
        MemoryDB[("memory-db")]
        RegistryDB[("registry-db")]
        GovernanceDB[("governance-db")]
      end
      Policy["default-deny + explicit NetworkPolicy"]
      Secrets["generated development PKI/credentials"]
    end
    Secrets --> Stateless
    Stateless --> Stateful
    Policy -. "constrains declared paths when CNI enforces policy" .-> Stateless
```

## Namespace and cluster patterns

The [TrueForge namespace integration design](03-trueforge-namespace-integration.md) is implemented
as the development namespace-pair profile: fresh fabric in `viewsense-dev`, official private
runtime/state in `trueforge-dev`. The owner explicitly authorized the old development/evaluation
reset without backups. Legacy orchestration/manual kernel source and agent storage are removed.
The [operation record](../40-ops/03-clean-state-rebuild.md) documents the boundaries and actual
qualification. Production multi-cell and offline paired packaging remain future work.

| Profile | Isolation | Suitable for |
|---|---|---|
| development | `viewsense-dev` + `trueforge-dev`, single replicas | synthetic runtime and retained fabric integration testing |
| standard | separate edge/control/provider/data namespaces | normal enterprise production |
| regulated | dedicated provider/data cluster or tenant cell | strict residency and blast-radius controls |
| GPU scale | control cluster plus one or more inference clusters | large model fleets and independent capacity |

The base development manifests touch only `viewsense-dev`. The versioned evaluation installer
uses an explicit `viewsense-release-*` namespace as its environment overlay, with separate
generated PKI/credentials and fixed-version offline images. Production overlays must not reuse
development keys, issuer, mock providers, `imagePullPolicy: Never`, or single-replica databases.

## Downloadable release contract

The manually dispatched release workflow builds both architectures from exact paired commits,
checks the existing reference/profile/docs contracts and uploads a checksummed GitHub draft.
The request job detects completed drafts through an authenticated release list before building;
the uploader verifies drafts by release ID rather than the published-release tag endpoint.
Its plain version controls staged chart/application/global-image metadata without changing the
source chart. It creates no cluster resources and does not replace live namespace/CNI acceptance.
Only an explicit manual `main` run can release; pushes and legacy trigger-file edits cannot. See the
[automation procedure](../../../releases/installation.md#manually-build-a-release).

The [release installation guide](../../../releases/installation.md) defines the 1.0.1
GitHub Release assets: a versioned Helm chart and per-architecture Linux image bundles with
checksums, matching documentation and paired source commits. The image archive includes
PostgreSQL and pgvector, so node installation does not require registry access. Images are
loaded into every node runtime before the chart is installed. The evaluation installer
requires an explicit context, refuses existing namespaces and installs one suite per namespace.
It creates only namespaced application resources; it does not install CRDs or cluster operators.
The Helm smoke workload has a dedicated ServiceAccount and exact HTTPS egress to its seven
reference targets, plus the common DNS rule. Ingestion is an explicit memory-gateway ingress
source, matching the implemented ingestion-to-memory request flow. No direct gateway-to-ingestion
or orchestrator-to-MCP path is allowed by these corrections.

Namespace deletion is available only for the matching release-owned disposable namespace and
uses a UID precondition. Reset waits for deletion, regenerates isolated material and repeats
installation/acceptance. All four database state owners remain unchanged; resetting destroys
their evaluation state, subject to the storage provisioner's reclaim policy. Data-preserving
replacement and production promotion require reviewed environment and migration evidence.

```mermaid
flowchart LR
    Commits["paired clean source commits"] --> Package["chart + images + docs + checksums"]
    Package --> Draft["GitHub Release draft"]
    Draft --> Review["operator publication"]
    Package --> Import["every node runtime"]
    Import --> Namespace["new release-specific namespace"]
    Namespace --> Acceptance["Helm smoke + CNI allowed/denied probes"]
    Acceptance --> Reset["owned namespace delete/recreate"]
```

## Workload rules

### Planned channel integration packaging

[Input/Output Channel resources](../10-overall/07-input-output-channels.md) are governance metadata,
not automatic deployments/namespaces. Package Teams entry and CRM-Logistics1 adapters independently
with unique workload identity, restricted pods, probes, bounded resources and external secret
references. Oracle remains CRM-owned outside the platform databases; only the CRM connector may
reach its approved encrypted endpoint or hold its read-only credentials. Add exact orchestrator →
governance/MCP and MCP → CRM paths, audience/scoped grants and adapter-only Oracle egress when
implementing the slice. Current manifests and their orchestrator-to-MCP denial remain unchanged.
Validate real allowed/denied connectivity, encrypted database transport, rotation and rollback
before admission; successful manifest rendering is not channel security acceptance.

The [role/console uplift](../10-overall/08-channel-consoles-role-mapping.md) adds governance-owned
policy resources and authorised edge facades, not a console-owned database. A provider-specific
entitlement-refresh adapter requires its own least-privilege IdP identity/egress; browser and generic
gateway pods must not receive IdP administrative credentials. Protect the existing governance
store for policy revisions and budget reservations with owner-only access and tested recovery.

[PII/egress enforcement](../10-overall/09-enterprise-ai-governance-egress.md) requires inspection
within an approved processing boundary and adapter-only constrained external egress. No generic
orchestrator/client path may reach external models directly. An optional reversible-token privacy
adapter needs a separate approved state/secret/retention design before deployment. Policy bundles,
inspection capabilities, route revisions and actual wire/negative connectivity evidence must agree
before an external route is admitted. This design changes no current manifest or secret grant.

### Common workload requirements

- one service account and workload identity per component;
- no automatic Kubernetes API token mounts unless a component genuinely calls the API;
- restricted Pod Security, non-root users, read-only roots, no added capabilities;
- default-deny ingress and egress, then explicit source/destination/port policies;
- provider credentials mounted only into the owning adapter;
- topology spread, anti-affinity, disruption budgets, and at least two replicas for stateless production services;
- stateful services use encrypted storage, topology-aware placement, backups, and tested restore.

## Installation sequence

1. Verify context, namespace, admission policies, storage class, ingress, DNS, and network-policy enforcement.
2. Install workload identity/certificate automation and external secret synchronization.
3. Create the ViewSense AI® namespaces and default-deny policies.
4. Install owned data services or bind to managed equivalents, including the isolated governance store.
5. Deploy identity/policy and governance dependencies, provider adapters, control services, then edge.
6. Run conformance and zero-trust negative tests before accepting traffic.
7. Register real providers through audited configuration and remove mocks.

## Product installation modes

- `bundled`: ViewSense AI® deploys and tests the component and owns its lifecycle, such as the bounded
  agent runtime and PostgreSQL/pgvector reference provider.
- `adapter`: ViewSense AI® deploys the contract/credential boundary while the product is separate, such
  as the Mem0 adapter.
- `managed-dependency`: a platform team installs the cluster service with its upstream lifecycle,
  such as SPIRE, an OpenTelemetry Collector, or external secrets.
- `external`: ViewSense AI® configures an authenticated endpoint, such as Keycloak/OIDC, a cloud LLM,
  or a workflow system.

The `enterprise-suite` profile describes integration intent. It does not create cluster-scoped
Keycloak, SPIRE, n8n, or OpenTelemetry operators. OPA can be embedded as a governance sidecar
because it is a stateless local policy decision point with a narrow loopback API. Every external or
managed selection requires credentials, CA trust, explicit egress, conformance tests, version
pinning, upgrade/rollback ownership, and a provider passport before production routing.

The retained OpenAI adapter takes an explicitly deployed server-controlled model from its Helm/environment configuration. The old single-namespace provider-switch launchers/default file are removed; hosted real-model enablement remains gated by protocol, identity, PII, budget, evidence and retention acceptance. Rollback uses a qualified profile or disables the affected route; it does not reapply the obsolete base.

```mermaid
flowchart LR
    Values["Helm values/profile"] --> Render["ViewSense AI® workloads"]
    Render --> Bundled["bundled services and databases"]
    Render --> Adapter["selected ViewSense AI® adapter"]
    Render -. "intent only" .-> Managed["Keycloak / SPIRE / Collector operator"]
    Render -. "planned adapter" .-> Workflow["n8n / Temporal / Argo"]
    Adapter --> External["enterprise-managed upstream product"]
```

The SPIRE socket/trust-domain and observability endpoint fields are reserved integration intent;
the current chart does not mount an SVID/SDS workload API or configure native application OTLP
export. External OpenAI and Mem0 adapters are the executable provider integrations. Generic
The Ollama adapter is packaged by the opt-in `profiles/local-ai.yaml` Helm profile; approved HTTPS
egress, TLS material, and identity grants are operator requirements. vLLM and workflow selections
still require adapters that have not shipped.

## Sizing method

Control-plane sizing is driven by concurrent requests and provider wait time. Inference sizing is driven by tokens, context length, batching, quantization, and model/GPU class:

$$
replicas = \left\lceil \frac{requests/sec \times average\ total\ tokens}{measured\ tokens/sec/replica \times target\ utilization} \right\rceil
$$

Use load tests from the actual model/runtime; nominal GPU specifications are insufficient. Reserve 25–35% failure/burst headroom for production. Memory-provider sizing includes corpus size, vector dimension, write rate, filter cardinality, index build overhead, and retention. MCP runtimes are sized per connector side effects and external rate limits rather than token load.

## Provider placement and routing

Provider descriptors include locality, residency, classification ceiling, capabilities, and cost class. Routing may cross clusters only through authenticated encrypted endpoints. It must never silently move restricted data from a local route to a public-cloud fallback. DNS names and provider URLs are configuration validated against egress policy.

## Development workflow in this repository

`scripts/k8s-deploy-dev.sh` delegates to `scripts/runtime/deploy.sh`: it checks context, renders
namespace-qualified boundaries/private resources, builds the fabric image and installs the pinned
official TrueForge release in the paired namespace. `make k8s-test` qualifies the retained APIs,
fixed runtime turn and real allowed/denied paths. Static base manifests remain fabric packaging
inputs; applying them directly is not the namespace-pair workflow. See [Quick start](../../../QUICKSTART.md)
and [Open TrueForge](../../../deploy/trueforge-access.md).

## Production gaps from the reference

Production requires an ingress/API gateway, enterprise OIDC, SPIFFE/mesh certificates, external secrets, signed immutable images, HA databases or managed data services, autoscaling, PDBs, telemetry collectors, backup schedules, policy engine integration, and GitOps overlays. These gaps are explicit rather than hidden behind the development manifest.

## Local AI profile and isolated console

`make console` runs host-side development APIs at loopback ports 8840–8844 and the GUI on 8787.
`deploy/local-ai/compose.yaml` supplies a dedicated persistent pgvector database on loopback 15432.
The launcher owns separate `.viewsense/local-ai` credentials/PKI and never rotates cluster material.
Stopping APIs retains the database volume; production HA/backup evidence is still required.

The opt-in Helm `profiles/local-ai.yaml` enables the Ollama adapter and real memory embeddings.
Before installing, provide `tls-ollama-adapter`, a `memory-postgres` workload secret/grant to identity
and `embedding.invoke` on `ollama-adapter`, approved upstream TLS/authentication and exact egress
CIDRs. Adapter administration is disabled in Helm. The profile's external egress is empty by default
and therefore denies upstream connectivity. Host `localhost:11434` is not a pod runtime address.
For chat routing additionally select `products.llm.product=ollama-adapter`, its internal endpoint and
audience, grant the LLM gateway `provider.invoke`, and set an approved chat model. No existing base
mock route is silently changed.

## Modular networking reference

The [CNI/mesh design](02-modular-networking-mesh.md) separates portable Service DNS/NetworkPolicy,
provider-owned packet forwarding, mesh transport identity and application JWT/tenant authorization.
The pinned Cilium/Istio ambient reference is a separate two-node cluster with an explicit private
kubeconfig. Upstream privileged node agents live in system namespaces; application pods retain
restricted security and dedicated ServiceAccounts, including four separate database identities.
The existing cks PVCs are not transferred or removed. Install CNI only on an approved empty cluster,
apply STRICT/default-deny mesh policies before enrollment, then verify actual traffic and recovery.
Installation alone is not security acceptance; current evidence and incomplete runtime gates are
recorded in the conformance map. Provider replacement requires a staged cluster/trust/data plan.

## Detachable release preview

The source checkout can attach its host-side GUI to an installed evaluation reference with
`scripts/release/console.py`. This creates only loopback debugging forwards; it adds no Kubernetes
resource, changes no namespace identity or data, and uses existing smoke grants. Twelve API health
checks, ingestion, memory writes and search are supported. These checks do not demonstrate CNI
enforcement and the GUI does not implement production traffic switching. The original 1.0.1
bundle remains a headless distribution; the preview is a follow-up source-checkout utility.

The preview can test the installed mock inference path through the gateway response API without
conversation writes. Real Tev1/Ollama models still require their separate adapter/upstream profile.

## Channel policy control-plane deployment

The existing governance service owns `channel_policy_state` in its database. No new Kubernetes
service or per-channel database is added. Base NetworkPolicy and Helm allow gateway → governance
on TLS port 8443. The unused orchestrator ingress permission on MCP is removed in base/Helm
so the tool path is denied at both declared boundaries. Other unused tool/CRM paths stay denied. The development issuer grants the
gateway only the explicit governance management/decision scopes needed by the facade.

The local harness adds governance at `https://127.0.0.1:8847` and a separate loopback PostgreSQL
instance at port 15433 with an independent user/password and retained volume. The GUI is optional.
Startup creates the additive table idempotently; old services ignore it on rollback. Back up the
governance database before upgrade, retain snapshots/disabled entries during rollback and restore
them as one consistent state. Do not roll back to a consumer that ignores channel decisions to
continue business execution. Full channel execution remains disabled in this slice.

## Local-only playground deployment

The edge-to-governance policy path requires `policy.evaluate`; governance is the sole decision
journal owner. New allow-listed flows permit governance to identity/Internal AI inspection and
edge to the approved Internal AI generation adapter. The local harness provisions private policy
and distinct scoped clients. Kubernetes defaults keep playground execution disabled without policy.

For Helm, enable `playground.enabled`, set `playground.policySecret` to an operator-provisioned
Secret containing `policy.json`, and set `playground.internalModel`. Enable the Ollama adapter with
an enterprise-approved internal runtime. Provision a `governance` workload credential with only
`ollama-adapter/provider.invoke` for optional inspection, and extend gateway grants with
`governance/policy.evaluate` and `ollama-adapter/playground.generate`. Human or fixed-tenant clients
need edge `playground.use` and a canonical approved console role. The policy model and adapter
model must agree. The source-checkout console attaches independently; it owns no database.

No external egress route is introduced by the playground. Future external AI needs adapter-level
final-wire inspection and receiver-observed containment tests before activation. See the
[playground design](../10-overall/10-user-playground-policy-engine.md).
