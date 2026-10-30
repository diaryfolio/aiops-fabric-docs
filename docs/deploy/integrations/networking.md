# ViewSense AI® Networking Operations

The current development profile connects `viewsense-dev` and `trueforge-dev` through fabric-owned
namespace-qualified topology-v2 policies. The selected cluster keeps its existing enforcing CNI.
No installer swaps the CNI, installs a mesh or changes unrelated system namespaces.
For native GUI access use [Open TrueForge](../trueforge-access.md); opening the GUI does not deploy
networking or grant cluster access.

## Current deployment and verification

```bash
kubectl config current-context
make k8s-deploy
make k8s-test
kubectl -n viewsense-dev get networkpolicy
kubectl -n trueforge-dev get networkpolicy
```

Use the explicit `k3d-cks` profile. `scripts/runtime/render.py` and
`viewsense_common.runtime_topology` generate default deny, scoped DNS and both ingress/egress
rules from namespace/workload endpoints and directed ports. The private rendered graph is under
`.viewsense/rebuild/topology.json`. Expected service accounts are recorded, but CNI pod selectors
alone do not authenticate a service account; application mTLS/JWT remain required.

Qualification must show allowed traffic and denial against known live listeners. The runtime test
checks database access denial and relabels the same previously allowed pod as untrusted. The fabric
policy script also checks allowed gateway → governance and ingestion → identity/memory, with
forbidden ingress/tool paths denied. DNS failure or wrong TLS trust is a failed probe, not success.
See the [test guide](../../tests/README.md) for exact acceptance.

## Retained provider and management contracts

The neutral provider catalog, pinned values, v1 single-namespace topology/mesh planner and
headless networking API remain. They support inspection, digest-bound evidence, reviewable plans
and future provider replacement. They do not apply cluster-admin operations or overwrite topology-v2.
The optional console Networking page is a client of those APIs; a plan is not enforcement evidence.

Cilium and Istio ambient remain external, independently operated choices. The fabric chart retains
single-namespace mesh configuration for separately qualified foundation profiles. Namespace-pair
mesh-v2 identity, enrollment, recovery and live acceptance are planned; v1 rules cannot certify the
TrueForge pair. Provider replacement needs exact namespace/workload/operation authority, live
positive/negative tests, approved rollback and evidence matched to topology/configuration digests.
Never expose arbitrary URL fetch or privileged installer execution through management APIs.

## Retired POC tools

The old `networking-up`, `networking-deploy` and `networking-test` targets and their single-namespace
bootstrap/application-mesh/test scripts are removed. They targeted a separate `viewsense-network`
POC and did not implement the current namespace pair. Historical evidence and published versioned
docs remain historical; they are not current deployment instructions.
The cleanup deletes repository assets only; it does not delete any separate cluster or its data.

Keep the [networking design](../../design/high-level/20-deployment/02-modular-networking-mesh.md),
[namespace contract](../../design/high-level/20-deployment/03-trueforge-namespace-integration.md)
and [cleanup record](../../design/high-level/40-ops/04-cleanup-record.md) alongside provider changes.
