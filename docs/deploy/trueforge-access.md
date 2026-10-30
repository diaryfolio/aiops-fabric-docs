# Agent runtime access

ViewSense has a management console and a separate agent-runtime administration interface.
The current backend is **TrueForge**, an independently maintained, unmodified upstream dependency.
Its native interface retains its upstream identity. ViewSense supplies the launcher, integrations
and enterprise controls; never edit the backend source, generated files, chart templates or image.
Run commands below from the **`aiops-fabric` repository root**.

## Open the native GUI

Start Docker Desktop, then run:

```bash
make trueforge-ui
```

Open **[http://localhost:8791](http://localhost:8791)**. Use HTTP for this local preview.
No client certificate, username or password is needed. The launcher waits for a healthy server
before printing the URL. Python 3 and Docker are sufficient; no Node installation, frontend build
or fabric/Kubernetes deployment is required to view the GUI.

This is the official bundled upstream interface, served directly by the pinned official image
in its supported standalone mode. With no model configured, it opens **Settings → Models**.
The Connectors, Skills, Sandbox providers and Web search tabs are also native upstream screens.
A model must be configured before chat can execute; the launcher neither downloads models nor
imports provider credentials. Use synthetic data for this personal preview.

## Start, inspect and stop

```bash
make trueforge-ui         # start, or show the existing healthy preview
make trueforge-ui-status  # show state and URL
make trueforge-ui-stop    # remove the preview and its temporary data
```

Keep Docker running while using the GUI. The image runs as a non-root user, with a read-only
root filesystem, dropped capabilities and bounded CPU, memory, process count and temporary space.
Only `127.0.0.1:8791` is published. The launcher checks ownership labels before changing Docker
resources named `viewsense-trueforge-preview` and does not touch unrelated containers or networks.

**All preview data is temporary.** SQLite sessions, agent/configuration changes and any provider
keys entered into this preview live in container tmpfs. Stopping, removing or restarting the
container discards them. This is independent demonstration state, with no backup or migration.
The Docker bridge permits ordinary outbound traffic; it does not implement fabric egress policy.
Do not expose the no-login preview remotely or treat it as an enterprise execution route.

## Which interface am I opening?

| Interface | Address / access | Purpose |
|---|---|---|
| Runtime administration preview | `http://localhost:8791`, `make trueforge-ui` | Official GUI with separate temporary SQLite data |
| Optional fabric management console | `http://127.0.0.1:8787`, `make console` or `make gui` with its API harness | Fabric policy/identity/memory controls and read-only runtime preview inventory |
| Integrated Kubernetes runtime | `https://trueforge-server.trueforge-dev.svc.cluster.local:8790` | Private hosted runtime called by the fabric through mTLS and native OIDC |

The preview cannot show Kubernetes sessions or fabric memory/governance data. Fabric management can observe safe preview configuration metadata. The optional fabric
console is retained for fabric capabilities; it is not a second agent runtime or a replacement
for the native runtime interface. Its local AI/SSO examples have separate prerequisites and credentials.

## Observe runtime configuration in ViewSense

Run `make console` (or `make gui` with an existing local harness), sign in as ViewSense Admin and
open [TrueForge integration](http://127.0.0.1:8787/?page=ai). The page reads the native preview's
configured model names, connectors, skills, sandbox and web-search types through supported APIs.
Configure an item in the runtime preview on 8791, then select **Refresh integration** in fabric; the page
also refreshes every 15 seconds while visible. There is no duplicate model editor or direct chat
model test lab. API keys, manifests, endpoint URLs and skill content are not returned to the browser.

Reachable means the preview API responded; configured means it reports an item. Neither proves
provider health, admission or customer execution. Hosted Kubernetes settings remain separately
**not observed**. The reader is disabled for SSO/release/production profiles and does not use the
hosted bootstrap identity. See the [ownership and API contract](../design/high-level/10-overall/06-local-ai-console.md).

## Why port 8790 reports a certificate error

Directly forwarding the integrated service is useful for an appropriately authenticated API client:

```bash
kubectl --context k3d-cks -n trueforge-dev \
  port-forward --address 127.0.0.1 svc/trueforge-server 8790:8790
```

A normal browser at `https://localhost:8790` receives:

```json
{"error":{"message":"Client certificate required"}}
```

That is expected mTLS enforcement. Port-forwarding does not create browser identity or interactive
login. The current fabric issuer supports workload tokens; an integrated browser gateway and
interactive AuthN/SSO remain unimplemented. Do not disable mTLS/OIDC, copy private workload keys
into the browser, expose the private service or customize the backend to bypass the error.
Use the separate localhost preview above when the aim is to explore the GUI.

## Deploy and verify the integrated runtime

For the existing development namespace pair, select `k3d-cks` and use the fabric deployment tools.
If the source-checkout Python environment is not prepared:

```bash
make console-deps
.venv-console/bin/python -m pip install --requirement requirements-dev.txt
```

Then:

```bash
kubectl config current-context
make k8s-deploy
make k8s-test
kubectl -n viewsense-dev get pods
kubectl -n trueforge-dev get pods
```

`viewsense-dev` owns retained fabric capabilities; `trueforge-dev` owns the official hosted runtime
and its separate PostgreSQL/Redis stores. The runtime controller is disabled in this profile.
The only integrated execution route is the authenticated fixed synthetic `/v1/runtime-check`.
General customer execution, native governed MCP, real-model tool protocols and production
policy/PII/budget/evidence/retention acceptance remain gated. Preview success does not close them.

## Pinned API compatibility

Inspect the running release's `/api/v1/openapi.json` before planning settings lifecycle actions.
The pinned 0.3.0 preview reports model-provider GET/POST/PUT but no provider-delete endpoint;
a newer source checkout's DELETE route is not evidence that this image supports deletion.
Avoid disposable provider experiments in a preview containing valuable state. Removing the
preview container discards all its temporary state; obtain the operator's choice before using
that reset as cleanup. Never edit the upstream database or patch the backend to add a missing API.

## Troubleshooting

| Symptom | Action |
|---|---|
| Browser cannot connect to port 8791 | Start Docker Desktop, run `make trueforge-ui`, and wait for its printed healthy URL |
| `Client certificate required` | You opened the hosted endpoint on 8790; use the preview URL on 8791 for the current native GUI |
| HTTPS error on 8791 | Use `http://localhost:8791` for the standalone preview |
| First launch takes time | The launcher may pull the official image; the pinned amd64 image may use host emulation |
| Port already occupied | Inspect `make trueforge-ui-status`; stop only the conflicting process you own; do not kill unrelated services |
| Ownership conflict | Inspect the named Docker resource; the launcher deliberately refuses to replace resources it does not own |
| Models screen is empty of configured providers | This is a fresh preview; no Kubernetes provider settings or credentials are imported |
| Settings or sessions disappear after stopping | Preview data is deliberately temporary; see the lifecycle above |

For startup diagnostics, use `docker logs viewsense-trueforge-preview`; avoid sharing logs after
entering real credentials or content. The native standalone logger uses upstream's local format.

See the [clean-state operation record](../design/high-level/40-ops/03-clean-state-rebuild.md),
[namespace design](../design/high-level/20-deployment/03-trueforge-namespace-integration.md),
[adoption gates](../design/high-level/03-trueforge-adoption-decommission.md),
[cleanup record](../design/high-level/40-ops/04-cleanup-record.md), and the
[official TrueForge introduction](https://trueforge.dev/introduction).
