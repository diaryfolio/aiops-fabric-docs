# ViewSense AI® Quick Start

Run commands from the `aiops-fabric` repository root. ViewSense management and the agent-runtime
backend have separate administration surfaces. The local runtime preview and secured hosted
runtime have independent configuration and session data.

## Open ViewSense management

Start Docker Desktop, run `make console` and open **[ViewSense management](http://127.0.0.1:8787)**.
Use the provisioned ViewSense Admin sign-in described in the
[management guide](#local-ai-management-console). The console shows enterprise controls and
runtime connection status; model/agent configuration uses the separate runtime interface below.

## Open runtime administration

Start Docker Desktop, then:

```bash
make trueforge-ui
```

Open **[http://localhost:8791](http://localhost:8791)**. No certificate or login is needed for this
localhost-only standalone preview. A fresh preview opens **Settings → Models**; configure a model
before chat can execute. Data and provider settings are temporary and disappear when stopped or
restarted. No Kubernetes credentials or sessions are imported. See
[Agent runtime access](deploy/trueforge-access.md) for the canonical access and troubleshooting guide.

```bash
make trueforge-ui-status
make trueforge-ui-stop
```

## Which command do I need?

| Goal | Command / guide |
|---|---|
| Open runtime administration preview | `make trueforge-ui`, then `http://localhost:8791` |
| Deploy the fabric/runtime namespace pair | `make k8s-deploy` |
| Verify fixed hosted turn, retained APIs and security denials | `make k8s-test` |
| Resume an existing stopped development cluster | `k3d cluster start cks` |
| Inspect hosted workloads | `kubectl -n viewsense-dev get pods` and `kubectl -n trueforge-dev get pods` |
| Open ViewSense management console | `make console`; separate from runtime administration |
| Run fabric local APIs without the console | `make harness`; attach the console with `make gui` |
| Expose retained fabric APIs to an authenticated local client | `make ports-start`; four mTLS forwards |
| Stop those forwards | `make ports-stop`; workloads keep running |

## Prerequisites

The GUI preview needs Python 3 and running Docker only. Kubernetes development additionally needs
kubectl, k3d, Helm, Python 3.12 and OpenSSL. Prepare the source-checkout environment:

```bash
make console-deps
.venv-console/bin/python -m pip install --requirement requirements-dev.txt
```

## First installation

Inspect existing clusters before creating one. For a new local development installation only:

```bash
k3d cluster list
# Only if cks does not exist:
k3d cluster create cks --agents 1
kubectl config use-context k3d-cks
make k8s-deploy
make k8s-test
```

The deployment selects the explicit `k3d-cks` context, installs namespace-qualified boundaries and
fresh resources when absent, builds/imports fabric images and installs the independent official
backend chart. Fabric lives in `viewsense-dev`; hosted runtime/SQL/Redis live in `trueforge-dev`.
Private generated material is ignored under `.viewsense/rebuild`. Routine deployment does not
reset namespaces, delete data or migrate an old agent database. The earlier authorized no-backup
reset is recorded separately in the [operation record](design/high-level/40-ops/03-clean-state-rebuild.md).

## Normal daily startup

```bash
k3d cluster list
kubectl config current-context
kubectl -n viewsense-dev get pods
kubectl -n trueforge-dev get pods
```

If the existing cluster is stopped, start it with `k3d cluster start cks` and select `k3d-cks`.
Existing workloads and persistent volumes resume. Do not create another cluster or redeploy solely
to open the GUI. `make k8s-deploy` is an implementation/configuration update, not a daily start step.

## Expose the development APIs

```bash
make ports-start
make ports-status
```

| Fabric API | Local address |
|---|---|
| Gateway | `https://127.0.0.1:9443` |
| Workload issuer | `https://127.0.0.1:9444` |
| Memory gateway | `https://127.0.0.1:9445` |
| Governance | `https://127.0.0.1:9446` |

These are mTLS API endpoints, not browser login pages. Use the deployment's matching trust and
workload identity. `make ports` keeps forwards in the foreground; Ctrl+C closes only the forwards.
The hosted runtime on 8790 also requires mTLS/OIDC. A normal browser gets `Client certificate required`;
use the native preview on 8791 until integrated browser identity is implemented. Do not disable
hosted authentication to work around that response.

## Local AI management console

The ViewSense console runs at `http://127.0.0.1:8787` with `make console`. Open the
[runtime connection page](http://127.0.0.1:8787/?page=ai) as ViewSense Admin to read back configuration from the
native preview. Configure runtime models/connectors in the administration preview. The fabric console owns no
agent execution loop or duplicate runtime model editor. Its isolated Ollama/memory/ingestion/identity harness has separate prerequisites,
credentials and persistent local memory; follow the
[local console design](design/high-level/10-overall/06-local-ai-console.md) and
[management/SSO guide](deploy/integrations/keycloak.md). The preview inventory does not connect its agent execution to ViewSense capabilities or establish
a production SSO deployment.

## Headless harness and detachable GUI

```bash
make harness  # local capability APIs
# In another terminal, if wanted:
make gui      # optional fabric management client
make api-test # direct API checks without a GUI
```

Stopping the detachable client leaves its APIs operating. The local API CLI uses its own
server-held development credentials; it is not a source of credentials for the hosted namespace pair.

## Test ViewSense AI®

```bash
make unit
make lint
make profile-check
make k8s-test
```

See the [current validation guide](tests/README.md). The integrated execution path is fixed synthetic
verification only. `/v1/responses` returns authenticated HTTP 410; the manual agent-run API and its
storage are retired. No user prompt, remember flag or model selector is accepted by `/v1/runtime-check`.

## Provider and networking extensions

OpenAI/Ollama/Mem0 adapters, identity, governance, memory, ingestion, certificate and networking
contracts remain in fabric. The old `openai-enable`, `openai-model-update`, `openai-disable` and
single-namespace `networking-up/deploy/test` commands were removed; they do not configure the
current namespace pair safely. Real model/native MCP enablement and mesh-v2 remain gated.
See the [LLM module](fabric/llm/README.md), [networking guide](deploy/integrations/networking.md)
and [cleanup record](design/high-level/40-ops/04-cleanup-record.md).

## Stop or pause

`make trueforge-ui-stop` removes only the disposable native preview and its temporary data.
`make ports-stop` removes only fabric port-forwards. Ctrl+C stops a local console/harness process;
its retained local memory volume is separate. `k3d cluster stop cks` pauses the existing development
cluster without deleting volumes. Namespace/cluster/PVC deletion is never a normal shutdown step.
