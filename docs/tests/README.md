# ViewSense AI® Test and Validation Guide

Run commands from `aiops-fabric`. Keep `aiops-fabric-docs` beside it, or set `DOCS_REPO` for Make
and `VS_DOCS_DIR` for direct pytest. Current scope and gaps are in
[Implementation Conformance](../design/high-level/00-implementation-conformance.md).

## Static, contract and catalog checks

```bash
make unit
make lint
make catalog-check
make profile-check
kubectl kustomize deploy/kubernetes/base >/dev/null
make docs-build
```

These validate source, canonical contracts/catalog paths, every fabric Helm profile and current
documentation links/navigation. Render success does not prove live network or workload identity.
Fabric chart profiles configure retained capabilities; they do not install the independent hosted
TrueForge release or qualify production providers automatically.

## Native TrueForge GUI

```bash
make trueforge-ui
make trueforge-ui-status
curl --fail --silent --show-error http://localhost:8791/healthz
```

Open `http://localhost:8791` and verify the native Settings → Models screen. Inspect the native
Connectors/Skills/Sandbox/Web search screens without entering production credentials or customer
content. No model is configured automatically. The preview must publish only `127.0.0.1:8791`;
its image must match the pinned official digest and its container must remain non-root/read-only.
See [Open TrueForge](../deploy/trueforge-access.md) for lifecycle and troubleshooting.

Do not stop the preview merely to test cleanup after someone has started using it: its data is
disposable and stopping/restarting discards it. When finished intentionally, `make trueforge-ui-stop`
removes the owned preview resources. The hosted Kubernetes data and authentication remain separate.

## Kubernetes deployment and integration

```bash
kubectl config current-context
make k8s-deploy
make k8s-test
kubectl -n viewsense-dev get deploy,statefulset,pvc
kubectl -n trueforge-dev get deploy,statefulset,pvc
```

Select the explicit `k3d-cks` development context first. Expect eleven retained fabric Deployments,
three fabric StatefulSets (memory, registry, governance), one hosted runtime Deployment with its
fabric transport sidecar and two runtime StatefulSets (PostgreSQL/Redis). All selected containers
must be ready. The hosted controller and old manual agent database are absent.

`make k8s-test` creates a restricted temporary qualification pod and temporary bootstrap Secret,
then removes them in cleanup. It uses the current rendered profile's trust/credentials instead of
old `.viewsense/pki` files. Test data is synthetic; the script does not back up or reset namespaces.
The acceptance includes:

- ingestion/chunking, memory, MCP registry/mock invocation and governance/evidence API smoke;
- explicit HTTP 410 from the retired public response route;
- supported settings configuration and exactly one fixed hosted model turn;
- runtime JWT invalid/missing-token and missing-client-certificate denials;
- rejection of caller-supplied runtime-check payloads and unshared cross-subject session reads;
- qualification workload denied from fabric and runtime private databases;
- the same previously allowed workload relabeled untrusted and denied from identity/runtime;
- gateway → governance and ingestion → identity/memory allowed;
- gateway/governance → ingestion and ingestion → MCP denied on the enforcing CNI.

Success ends with `ViewSense AI® CNI policy probes passed`. DNS failure, failed TLS trust or an
absent listener is not policy-denial evidence; positive controls must pass against live services.
Capture only safe status/digest/count metadata, never tokens, keys, prompts or payloads.

## Retained local capability harness

```bash
make harness
# In another terminal:
make api-test
```

This checks the separate local decision/embedding/memory/ingestion APIs without a GUI. Optional
`make gui` attaches the fabric management client; it is not the native TrueForge GUI. The existing
`test-local-api.py`, `test-local-console.py`, `test-console-roles.py`, `test-channel-console.py` and
`test-playground.py` operate their documented local profiles. Use their supplied authenticated
session/CSRF and mTLS helpers rather than copying credentials into command arguments or chat.
See the [local console design](../design/high-level/10-overall/06-local-ai-console.md) and
[channel console guide](../fabric/governance/channel-console.md) for prerequisites and scope.

## Retained Compose foundation

```bash
make compose-up
make compose-test
```

Compose tests the retained fabric capability processes on private development networks. It does
not install hosted TrueForge, prove Kubernetes policies or supply native governed MCP. Its PKI and
volumes are separate from the namespace pair and the temporary standalone GUI. Inspect the current
Compose configuration before selecting optional profiles; do not copy its credentials into Kubernetes.

## Provider and production acceptance

Unit suites retain security/protocol checks for the OpenAI, Ollama and Mem0 adapters; runtime
real-model/tool compatibility is not implied. Configure optional products only through their
retained supported profile and owner-managed credentials after the applicable gates pass.
The obsolete single-namespace OpenAI overlay installers and networking POC installers are removed.
The namespace-pair topology-v2 renderer and CNI probes are the current development path; mesh-v2
and real provider protocol/identity/retention qualification remain future work.

Production acceptance still requires fresh per-dispatch authorization/admission, authoritative
entitlement refresh, PII wire inspection, hard budget reservation/reconciliation, durable safe
immutable evidence, no-retention deletion/storage, idempotent start/recovery, cancellation/drain,
HA/restore, rotation and full negative matrices. Follow the
[adoption gates](../design/high-level/03-trueforge-adoption-decommission.md) and
[enterprise controls](../design/high-level/60-enterprise/01-enterprise-integration-controls.md).

Historical curl walkthroughs for `/v1/responses`, manual agent checkpoints and old certificate paths
are removed. Use published versioned documentation when reviewing a historical release; those
snapshots are not instructions for the current development pair. See the
[cleanup record](../design/high-level/40-ops/04-cleanup-record.md).
