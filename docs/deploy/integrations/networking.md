# ViewSense AI® networking and mesh operating guide

The reference is a separate two-node `viewsense-network` k3d cluster. It uses supported pinned
Kubernetes, Cilium and Istio ambient versions from `deploy/networking/providers/versions.json`.
The existing `cks` cluster and its PVCs remain separate. The private kubeconfig is
`.viewsense/networking/kubeconfig`; tools never change the default context.

```bash
make networking-up       # independent CNI + mesh releases; system namespaces only
make networking-deploy   # application base, strict identity policies, ambient enrollment
make networking-test     # actual cross-node data transfer, denials, recovery and application smoke
```

The application namespace remains `viewsense-dev` with restricted Pod Security. Databases have
separate ServiceAccounts. Cilium enforces portable NetworkPolicy; Istio enforces STRICT peer identity
and exact ServiceAccount/port permissions from `deploy/networking/allowed-flows.json`. No application
JWT/tenant check is removed. The ambient CNI and ztunnel are privileged cluster tools; the application
pods have no new privileged init container or sidecar. Operator installation is explicit and is not
triggered by opening the GUI.

Cilium retains kube-proxy and uses `cni.exclusive:false` and `socketLB.hostNamespaceOnly:true` for
Istio coexistence. Docker nodes share a VM kernel but need independent BPF mounts and pin state. Do not bind a shared `/sys/fs/bpf` directory across nodes. Non-k3d clusters use an approved
CNI profile; do not copy Docker filesystem assumptions to production blindly.

## Headless management and detachable UI

Networking APIs at the gateway:

- `GET /v1/networking/providers`, `/v1/networking/topology`, `/v1/networking/status`: `platform.inspect`.
- `POST /v1/networking/plans`: `platform.plan`, body `{"cni":"cilium","mesh":"istio-ambient"}`.

The optional console adds `?page=networking` and forwards these APIs. It never runs kubectl or holds
cluster-admin credentials. A plan returns `applied:false`; reviewed provider deployment remains
operator/GitOps-owned. To view the independent cluster's evidence in the local SSO gateway, restart
`make sso-harness` with:

```bash
VS_NETWORKING_CONTEXT=k3d-viewsense-network \
VS_NETWORKING_CNI=cilium VS_NETWORKING_MESH=istio-ambient make sso-harness
```

The gateway's operator-owned default evidence file is `.viewsense/networking/verification.json`.
The enrollment tool mounts a public `networking-evidence` ConfigMap read-only at the application
gateway and configures `VS_NETWORKING_EVIDENCE_FILE`. The acceptance tool updates that ConfigMap;
projected-volume refresh is asynchronous. Helm uses `products.networking.context` and
`products.networking.evidenceConfigMap` for the same boundary. Evidence identifies
its actual cluster, versions, topology/provider-profile hashes and check time. Ten minutes later it is stale, not live
health. Missing/mismatched/failed evidence is never presented as an enforced cluster. Native provider
APIs remain available via Kubernetes; Hubble exposes TLS-protected flow metadata and ztunnel exposes transport telemetry.
Cilium plaintext Prometheus exposure is disabled in the provider profile pending an authenticated collector. Production collectors, durable dashboards and on-call alerting are separately owned.

## Verification and operations

Acceptance fixtures contain synthetic echo traffic only and remain in `viewsense-dev`. Unmeshed
fixtures prove CNI filtering separately from STRICT mesh authentication. Checks distinguish DNS,
trust and infrastructure failures from denied data transfer. They pair denied paths with an allowed
control path, test both Services and pod IPs across nodes, reject an unapproved mesh identity and an
unencrypted peer, then recover a workload and the ztunnel DaemonSet. The application smoke still uses
its own TLS and JWTs; its connectivity probes transfer HTTP health bytes instead of assuming a TCP
handshake proves authorization. Review the JSON result; a failed check or incomplete run is failed
acceptance. Latency numbers include kubectl orchestration and are not production p95/p99 SLOs.

For diagnosis (explicit private kubeconfig):

```bash
kubectl --kubeconfig .viewsense/networking/kubeconfig -n kube-system get pods
kubectl --kubeconfig .viewsense/networking/kubeconfig -n istio-system get pods
kubectl --kubeconfig .viewsense/networking/kubeconfig -n viewsense-dev get peerauthentication,authorizationpolicy
```

`make k8s-deploy` updates application images and the portable base. On the networking cluster rerun
`apply-networking-mesh.py` to restore gateway evidence configuration and mesh policies after base updates. Database accounts
are already distinct in the portable base, so redeployment preserves their identities.
Upstream CNI/mesh upgrades are separate Helm operations; stage a supported pinned profile and rerun
acceptance. The installer refuses a mismatched existing Kubernetes version. Installers have bounded
waits and preserve failed resources for inspection; they do not silently delete a cluster or CA.

## Replacement and production gates

For an approved replacement CNI, create a new cluster, validate its NetworkPolicy/DNS/Service behavior,
restore databases through their documented backups, and cut over after tenant/security acceptance.
Never uninstall the active CNI or hot-swap it under existing PVC workloads. The external-networkpolicy
plan is a compatibility contract, not an installer for every CNI. Other meshes need a topology policy
adapter and the same strict peer/identity/recovery acceptance; none is claimed automatically validated.

To detach Istio after reviewing application TLS coverage, remove namespace/pod ambient enrollment,
verify application smoke and CNI denies, then remove only the mesh policy/release resources. Keep CNI
policy and application authorization. Do not uninstall ztunnel while enrolled workloads depend on it.
Persistent data migration from `cks`, production ingress/egress gateways, multi-zone HA, capacity/load
benchmarks, approved mesh CA, trust rotation and durable telemetry remain deployment acceptance work.
No L7 model/tool retries are enabled: app TLS is opaque and replaying writes or inference can duplicate
side effects. Mesh transport identity is Istio-issued; SPIRE integration remains a separate provider.

Primary references: [Cilium/Istio coexistence](https://docs.cilium.io/en/stable/network/servicemesh/istio/),
[Cilium k3s install](https://docs.cilium.io/en/stable/installation/k3s/),
[Istio ambient install](https://istio.io/latest/docs/ambient/install/helm/),
[ambient policy](https://istio.io/latest/docs/ambient/usage/networkpolicy/),
[Istio releases](https://istio.io/latest/docs/releases/supported-releases/).

The neutral flow graph covers the canonical base suite. Additional Ollama/OpenAI/Mem0, identity
provider and policy integrations require extending the graph with their exact ServiceAccount/port
permissions and approved external egress, then rerunning acceptance. Choosing a product suite
does not implicitly grant those network paths. Do not weaken default-deny to enable a new provider.
Mesh-issued ephemeral certificates remain Istio-owned and are not yet included in the certificate
inventory. The current source/profile changes need live acceptance and running API/GUI processes
must restart to load their networking routes. See the conformance record for the execution blocker.

Provider values are JSON Helm values files under `deploy/networking/providers`, read without a
vendor SDK or extra YAML dependency. Acceptance compares installed Helm values and actual image/
node versions with the selected profile. Changing the profile invalidates prior evidence even if
the allowed-flow graph stays unchanged. `make networking-up` must reconcile updated provider
values before deployment/acceptance. This checks the declared Helm configuration and observed
traffic; production must additionally detect direct controller/resource drift continuously.
