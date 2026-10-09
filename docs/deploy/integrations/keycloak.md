# ViewSense AI® modular SSO and certificate POC

The framework runs headless. The gateway exposes provider metadata, verified user/role context,
component APIs, product catalogs, suite plans and certificate administration. The optional
management console forwards user access tokens; the API derives tenant and enforces scopes.
Keycloak runs in a separate Kubernetes pod/service/PVC. The certificate API is a separate workload,
and cert-manager is a separately installed upstream operator.

## Start the Kubernetes POC and detachable console

From the repository root (Docker and the local k3d context must be available):

```bash
make k8s-deploy
make keycloak-poc-deploy
# Existing cks Kubernetes 1.31 only: explicitly opt into the compatible, upstream-EOL POC release.
VS_CERT_MANAGER_LEGACY_POC=true make certificates-enable
# On supported Kubernetes >=1.33 use: make certificates-enable
```

Keep these commands running in three separate terminals:

```bash
.venv-console/bin/python scripts/forward-security-poc.py
make sso-harness
make sso-gui
```

After the forwards are ready, ensure an existing imported realm has Keycloak's basic subject scope:

```bash
.venv-console/bin/python scripts/configure-keycloak-poc.py
```

Open `http://127.0.0.1:8787/?page=overview`, choose **Keycloak POC** and sign in.
POC users are `poc-operator` (management/tests/renewal), `poc-viewer` (inspection/inference/read-only
certificates), and `poc-other` (read-only user in tenant-b). Random passwords are in the private,
ignored `.viewsense/local-ai/sso/poc-credentials.json`; do not put them in source control or tickets.
`bootstrap-admin` administers Keycloak using its separate `admin_password`. The provider's console
is `https://127.0.0.1:8848/admin/`. The development CA is private; trust the public CA explicitly in
your browser rather than disabling certificate checks for an enterprise deployment.

Stop older `make harness`, `make console` or `make gui` launchers before using the SSO launchers;
they use the same local ports. Ctrl+C closes only a launcher's processes. Keycloak and pgvector PVC/
volumes retain data. Realm import never resets existing users or passwords. Applying the base with
`make k8s-deploy` resets certificate-controller integration to disabled; rerun `certificates-enable`.
The forwards reconnect when a pod rolls. Keycloak POC restart preserves its embedded database;
production requires the upstream Operator and an approved HA database.

## Management workspaces

- Overview and suites: select Development, Local AI, Enterprise or Sovereign, inspect readiness and
  download a reproducible plan. `applied:false` means no deployment or provider switch occurred.
- AI/models: installed-model dropdowns, explicit preview/save, decision, embedding, chat and RAG tests.
- Identity/access: verified subject, signed tenant, mapped roles/scopes and provider management link.
- Certificates: local and Kubernetes public inventory, expiry, cert-manager readiness/revision,
  scheduled renewal and approved renewal requests. Private keys are never returned.
- Observability: live API reachability, telemetry capabilities and session test history. Native OTLP,
  central log query and durable audit export are explicitly planned.

Each area has a shareable `?page=` URL. Removing the GUI leaves the APIs operating.

## Headless API and provider configuration

Local SSO gateway: `https://127.0.0.1:8845`; OpenAPI: `/openapi.json` and `/docs`.
External callers use verified OIDC bearer tokens over TLS. The internal component APIs still require
workload mTLS and broker-issued audience/scoped JWTs. Direct certificate APIs are
`https://127.0.0.1:8846` (local) and forwarded `https://127.0.0.1:8849` (Kubernetes).
The optional development bridge uses a separate certificate-only broker client at forwarded
identity port 8850; it combines inventories through APIs and preserves signed user/tenant context.
A stopped forward or unavailable source is an operational failure, never authorization fallback.

| API | Required privilege |
| --- | --- |
| `GET /v1/auth/providers` | Public login metadata |
| `GET /v1/auth/me` | Valid tenant-bound identity |
| `GET /v1/auth/roles` | `security.inspect` |
| `GET /v1/platform/catalog`, `/v1/platform/suites`, `/v1/platform/status` | `platform.inspect` |
| `POST /v1/platform/suite-plans` | `platform.plan` |
| `GET /v1/models`, `/v1/provider-status` | `provider.inspect` |
| `POST /v1/decisions`, `/v1/chat/completions` | `provider.invoke` |
| `POST /v1/embeddings` | `embedding.invoke` |
| `POST /v1/model-tests`, `PUT /v1/configuration` | `provider.admin` |
| Memory/ingestion facades | `memory.read/write/admin`, `ingest.write` |
| Certificate inventory/detail | `certificates.read` |
| `POST /v1/certificates/{namespace}/{name}:renew` | `certificates.renew` |
| Certificate service `GET /metrics` | Workload mTLS + `certificates.read` |

The POC machine client `viewsense-poc-cli` can obtain a client-credentials token from Keycloak's
`/realms/viewsense/protocol/openid-connect/token`; its private secret is in the same credential file.
Never print bearer tokens into logs or use browser launch credentials for API integration.

Reproduce the headless acceptance checks without printing secrets:

```bash
.venv-console/bin/python scripts/test-enterprise-poc.py
# Explicitly request renewal of the dedicated canary only:
.venv-console/bin/python scripts/test-enterprise-poc.py --renew-canary
```

The renewal check expects a new ready revision, rejects stale requests with 409, and rejects
root-CA requests with 403. It leaves service certificates and the development CA unchanged.

`VS_SSO_PROVIDERS_FILE` points to an operator-owned JSON array conforming to
`contracts/schemas/oidc-provider-v1.schema.json`. Providers pin issuer, API audience, JWKS URL,
claim paths, allowed scopes, role-to-scope allowlists, optional HTTPS code/token endpoints, client ID,
server-side secret file and registered callback. Keycloak and Okta/generic OIDC share this contract.
For Keycloak use `realm_access.roles`; for Okta configure an API authorization server, explicit API
audience and custom tenant/groups claims (`scope_claim: scp`, `roles_claim: groups` where applicable).
Okta live acceptance requires an actual provider tenant and remains pending.

The edge validates issuer/audience/algorithm/expiry/tenant and bounds JWKS caching to 60 seconds.
Browser login uses code + PKCE S256 + state + nonce and verifies the ID-token authorized party.
The loopback HTTP callback is permitted only in explicit development. HTTPS console callbacks
require `VS_CONSOLE_SERVER_CERT_FILE`/`VS_CONSOLE_SERVER_KEY_FILE`, secure cookies and a matching
public origin. Enabling SSO disables launch-key login. No refresh token is retained: sessions expire
with the five-minute POC access token and require reauthentication. HA sessions, provider revocation/
backchannel logout and audited configuration promotion remain production work.

Helm supports `products.identity.providersSecret`, `providerCaSecret` and `publicEdgeTls`.
The secret supplies `providers.json`; its provider CA path should reference the separately mounted
`/run/viewsense/sso-ca` bundle. Public-edge TLS is allowed only with explicit OIDC registry config;
internal listeners retain mandatory client certificates. IdP egress must be explicitly approved.

## Certificate operations and limits

The certificate service reads public files and namespaced Certificate CRD metadata; its Kubernetes
Role cannot read Secrets. Renewal additionally requires a configured renewable resource name,
`viewsense.ai/renewal-api: enabled`, non-CA status and matching `resource_version`. RBAC status-patch
resourceNames must match the API allowlist. The POC only permits `viewsense-managed-canary`.
The root CA cannot be renewed through this API.

```json
{"resource_version":"123"}
```

Renewal returns 202 accepted. Poll detail until revision increases and readiness is true; issuance
is distinct from a running workload loading the new certificate. Workload reload remains an
operator-controlled rollout. Do not delete TLS Secrets or silently replace the development CA.
Static service certificates remain externally managed and cannot be renewed through cert-manager
until a controlled migration assigns issuer, trust distribution and workload restart ownership.

Expiry states: expired at zero remaining lifetime, critical within 24 hours, warning within seven
days, otherwise healthy. A 60-second metadata scan emits structured expiry-state changes and
inventory failures; authenticated OpenMetrics includes expiry timestamps and completeness.
External alerting/SIEM can consume these without the GUI. Logs never include PEM, private keys,
JWTs, client secrets, prompts or memory content. Audit persistence/export still requires a collector.

Helm's optional `products.certificates` service requires TLS/public material, renewable names and
explicit API-server egress for cert-manager. Issuance is managed by the upstream cert-manager API;
the harness does not expose private-key import/export or unrestricted CA/issuer editing.

Production gates remain: supported Kubernetes/cert-manager versions, enforced NetworkPolicy,
approved CA/issuer and backup, staged trust rotation/workload reload, HA IdP/database/sessions,
Okta acceptance, external secret lifecycle and durable audit export. The existing cks CNI denial
regression is a known blocker. Uninstalling cert-manager deletes its CRDs/resources; rollback this
POC by disabling integration while retaining Certificates and Secrets until migration is planned.

Upstream references: [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers),
[Keycloak basic subject scope](https://www.keycloak.org/docs/26.3.5/upgrading/index.html),
[cert-manager installation](https://cert-manager.io/docs/installation/kubectl/),
[supported versions](https://cert-manager.io/docs/releases/),
[cmctl renewal semantics](https://github.com/cert-manager/cmctl/blob/master/pkg/renew/renew.go).
