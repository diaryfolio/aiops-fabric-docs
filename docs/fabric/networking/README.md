# ViewSense AI® networking module

Networking is an operator-owned provider boundary. Kubernetes CNI/NetworkPolicy controls packet
reachability; the optional mesh controls workload transport identity; application TLS/JWT and tenant
checks remain in the APIs. The reference installs Cilium and Istio ambient independently. Replace a
provider by satisfying the same topology and runtime acceptance contract, not by editing application
code. Suite/network plans are reviewable API output and do not apply cluster-admin operations.

The source of truth is `deploy/networking/allowed-flows.json`. Strict Istio policy generation and the
Helm profile use the same graph; tests reject drift. The independent `viewsense-network` cluster
keeps existing POC PVCs separate. Timestamped acceptance evidence is exposed through the headless
networking API and the detachable Networking page; stale or missing evidence is never live health.

See the [networking design](../../design/high-level/20-deployment/02-modular-networking-mesh.md)
and [operator guide](../../deploy/integrations/networking.md) for install, acceptance and replacement.
