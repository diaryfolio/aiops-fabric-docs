# ViewSense AI® Networking Module

The current development namespace pair uses the fabric-owned topology-v2 schema/generator and
actual CNI enforcement. CNI packet reachability, mesh transport identity and application mTLS/JWT
remain separate replaceable controls. The selected cluster retains its existing CNI; legacy
single-namespace Cilium/Istio POC installers are removed.

Runtime topology generation lives in `viewsense_common.runtime_topology` and `scripts/runtime/render.py`.
`make k8s-test` verifies the allowed/denied paths. The retained v1 management API/planner, provider
catalog and pinned configuration assets remain foundations; they do not overwrite v2 or supply
namespace-pair mesh acceptance. Mesh-v2 deployment/recovery is planned. Operator plans and stale
historical evidence never imply live health or authorization.

See the [operator guide](../../deploy/integrations/networking.md),
[networking design](../../design/high-level/20-deployment/02-modular-networking-mesh.md), and
[Agent runtime access](../../deploy/trueforge-access.md) for the independent native GUI preview.
