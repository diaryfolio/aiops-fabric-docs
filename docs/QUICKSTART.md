# ViewSense AI® Quick Start

This guide covers the development lifecycle: install once, start an existing cluster, enable an
OpenAI provider without rebuilding everything, expose APIs locally, test the suite, and stop it
without losing data.

Run implementation commands from the `aiops-fabric` repository root. This guide is
maintained in `aiops-fabric-docs`; documentation builds run from that repository.

## Prerequisites

Install Docker, `kubectl`, `k3d`, Helm, `curl`, and `jq`. Docker must be running.

```bash
docker info >/dev/null
kubectl version --client
k3d version
helm version --short
```

## Which command do I need?

| Situation | Command | Effect |
|---|---|---|
| first installation | `make k8s-deploy` | builds/imports images and installs `viewsense-dev` |
| normal daily use | no deployment command | Kubernetes workloads remain running |
| cluster exists but is stopped | `k3d cluster start cks` | starts the existing cluster and retained data |
| application or manifests changed | `make k8s-deploy` | rebuilds and rolls out the development suite |
| run automated integration test | `make k8s-test` | runs the namespaced smoke Job |
| enable OpenAI on an installed suite | `make openai-enable` | prompts for the key and switches the LLM route |
| rebuild and then enable OpenAI | `make openai-enable-fresh` | full deployment followed by secure configuration |
| expose APIs on localhost | `make ports-start` | starts the five managed port-forwards |
| stop local API access | `make ports-stop` | stops only the port-forwards; workloads keep running |

## First installation

Create the development cluster only if `cks` is not already listed:

```bash
k3d cluster list
k3d cluster create cks --agents 1
kubectl config use-context k3d-cks
make k8s-deploy
make k8s-test
```

`make k8s-deploy` is intentionally a full installation/update. Messages about pulling PostgreSQL
images, creating `k3d-cks-tools`, and importing images are expected. The tools node is temporary and
lets k3d copy local Docker images into the Kubernetes nodes. This is not an OpenAI model download.

Do not run `k3d cluster create` when `cks` already exists. Use the daily startup procedure instead.

## Normal daily startup

Docker and the k3d cluster may already be running. Check before starting anything:

```bash
k3d cluster list
kubectl config current-context
kubectl -n viewsense-dev get pods
```

Expected: cluster `cks` shows its server/agent running, the context is `k3d-cks`, and application
pods show `Running` with ready containers. A completed `viewsense-smoke` pod is normal.

If `cks` exists but is stopped:

```bash
k3d cluster start cks
kubectl config use-context k3d-cks
kubectl -n viewsense-dev wait --for=condition=Available deployment --all --timeout=180s
```

Kubernetes restarts the existing workloads. You do not need `make k8s-deploy`, and database volumes
remain attached to the existing cluster.

## Local AI management console

With Python 3.12, OpenSSL, Docker Desktop and your local Ollama running, start:

```bash
make console
```

The launcher opens `http://127.0.0.1:8787` with a development session and runs isolated identity,
Ollama adapter, memory and ingestion APIs. It uses the installed `tev1:0.8b` decision model and
`embeddinggemma-2:270m` embedder by default; no model downloads occur. Use Components to inspect
health and edit installed model selections; use Test lab for decision, embedding, ingestion and
RAG tests. Backfill processes old owner records after an embedding profile change.

The dedicated pgvector database is bound to `127.0.0.1:15432` and retains its volume when stopped.
Ctrl+C stops console APIs. Existing cluster credentials and cluster memory are separate. If a model
or the database is missing, the GUI reports unavailable. Restart with `make console` to open a fresh
authenticated session; the launch credential is never printed or stored in browser storage.

The [console design](design/high-level/10-overall/06-local-ai-console.md) describes trust
boundaries and the remaining production GUI controls. The development console is not enterprise SSO.

## Headless harness and detachable GUI

Run APIs in terminal 1:

```bash
make harness
```

Optional GUI in terminal 2:

```bash
make gui
```

Stopping terminal 2 leaves the APIs and RAG data running. APIs can restart while the GUI
remains attached; valid development credentials/certificates are preserved. `make console` remains the combined
convenience launcher; stop that launcher before switching modes. GUI-only attach does not change
certificates, model defaults, database credentials or vectors.

Independent APIs use HTTPS: identity `8840`, model adapter `8841`, memory provider `8842`,
memory gateway `8843`, ingestion `8844`. Every component publishes `/openapi.json` and `/docs`
under its base URL, protected by client-certificate transport. Browser port `8787` is optional.
Models share the adapter's decision/embedding/chat routes. Full-suite tools/agents/governance
remain separate Kubernetes services; this development launcher covers local AI and knowledge.

Run a direct decision/embedding/RAG smoke test without the GUI:

```bash
make api-test
```

This stores synthetic data. For an individual request, save its JSON to `decision.json` and run:

```bash
.venv-console/bin/python scripts/local_api.py ollama-adapter /v1/decisions \
  --scope provider.invoke --body-file decision.json
```

The CLI reads private development client material, obtains an audience/scoped JWT in memory and
calls the component directly over mTLS. It never prints credentials or requires a console session.
Use `--method GET --scope provider.inspect` with `/v1/provider-status` for installed models.
A complete capability/API/gap matrix is in the
[headless design](design/high-level/design_01.md#platform-wide-headless-api-requirement).

## Enable OpenAI securely

On an already installed suite, run:

```bash
make openai-enable
```

Enter the API key at the hidden prompt. Do not put it in the command, an environment file, Helm
values, documentation, chat, or Git. The setup script pipes it directly to the namespaced
`openai-credentials` Secret. Only `openai-adapter` references that Secret.

The non-secret local default is maintained in `config/models.env`:

```bash
VS_OPENAI_MODEL=gpt-5.6-luna
```

Use `make openai-enable-fresh` only when the ViewSense AI® image or Kubernetes resources also need to be
rebuilt. Normal key or model configuration does not need an image import.

To change the model later, edit that one value and update the running adapter without reading or
replacing its API key:

```bash
make openai-model-update
```

An exported `VS_OPENAI_MODEL` overrides the file for a one-off `openai-enable` or
`openai-model-update`. Helm installations use the equivalent
`products.llm.openai.model` value so each environment can pin and promote its own model.

Confirm configuration without displaying the Secret value:

```bash
kubectl -n viewsense-dev get deployment openai-adapter
kubectl -n viewsense-dev get secret openai-credentials \
  -o jsonpath='{.metadata.name}{" configured\n"}'
kubectl -n viewsense-dev get deployment llm-gateway \
  -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="VS_LLM_PROVIDER_AUDIENCE")].value}{"\n"}'
```

Expected provider audience: `openai-adapter`. Do not print the Secret with `-o yaml` or decode its
data fields.

## Expose the development APIs

Start all forwards in the background:

```bash
make ports-start
make ports-status
```

| API | Local endpoint |
|---|---|
| public gateway | `https://127.0.0.1:9443` |
| development identity | `https://127.0.0.1:9444` |
| memory gateway | `https://127.0.0.1:9445` |
| governance | `https://127.0.0.1:9446` |
| agent runtime | `https://127.0.0.1:9447` |

For a foreground session where `Ctrl+C` stops every forward:

```bash
make ports
```

## Test ViewSense AI®

Run the automated Kubernetes smoke test:

```bash
make k8s-test
```

Expected final output:

```text
ViewSense AI® end-to-end smoke tests passed
```

With the default route, the smoke test uses the deterministic mock LLM. With the OpenAI route
enabled, inference steps use the configured OpenAI account and may incur API charges.

For the canonical two-terminal, VS Code-safe API test that writes uniquely owned synthetic public
memory and then asks OpenAI a curl prompt whose answer must use that memory, follow
[Real OpenAI memory-grounding validation](tests/README.md#5-real-openai-memory-grounding-validation).
The same test guide contains direct memory, durable-agent, governance, negative-authorization, and
observability checks.

## Stop or pause

Stop only the localhost forwards while leaving ViewSense AI® live:

```bash
make ports-stop
```

Return to the mock LLM and delete the development OpenAI Secret:

```bash
make openai-disable
```

Pause the whole development cluster while retaining its workloads and volumes:

```bash
k3d cluster stop cks
```

Resume it later with `k3d cluster start cks`. Do not delete the cluster unless you intentionally
want to remove its Kubernetes resources and cluster-managed data.

## Troubleshooting

```bash
kubectl config current-context
k3d cluster list
kubectl -n viewsense-dev get pods
kubectl -n viewsense-dev get events --sort-by=.lastTimestamp
kubectl -n viewsense-dev logs deployment/llm-gateway --tail=50
kubectl -n viewsense-dev logs deployment/openai-adapter --tail=50
scripts/port-forward-dev.sh logs
```

- Wrong context: run `kubectl config use-context k3d-cks`.
- `viewsense-dev` missing: perform the first installation.
- Local port already in use: stop older manual `kubectl port-forward` processes before starting the
  managed forwarder.
- OpenAI `401`/`403`: rotate or correct the provider key, then rerun `make openai-enable`.
- OpenAI `429`: check project quota, rate limits, and spend controls; ViewSense AI® will not silently
  fall back to a different provider.

This development setup uses local PKI, a development issuer, single replicas, and Kubernetes
Secrets. Production requires enterprise identity, external secret management, constrained egress,
high availability, backups, policy admission, and the controls in the
[technical guide](TECHNICAL_README.md).

## Platform management with Keycloak SSO and certificates

Use the [SSO/certificate POC operating guide](deploy/integrations/keycloak.md). It starts a separate
Keycloak Kubernetes pod/PVC, certificate API and cert-manager operator, then attaches the headless
local AI gateway and optional GUI. The GUI has Overview/suite planning, AI/models, Identity,
Certificates and Observability pages. Suite plans do not apply deployments. POC passwords stay in
private generated files; production gates remain explicit in the guide.

## Separate networking and mesh reference

See the [networking operating guide](deploy/integrations/networking.md). The implemented reference
uses an independent `viewsense-network` cluster and keeps the existing cks data/context intact:

```bash
make networking-up
make networking-deploy
make networking-test
```

The detachable console adds Networking at `?page=networking`; headless clients use
`/v1/networking/providers`, `/v1/networking/topology`, `/v1/networking/status` and
`/v1/networking/plans`. A plan does not apply resources. Runtime acceptance is currently pending;
see the [conformance record](design/high-level/00-implementation-conformance.md).
