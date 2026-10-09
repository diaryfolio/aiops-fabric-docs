# ViewSense AI® Repository Instructions

These instructions apply to every human or AI-assisted change in `aiops-fabric`
and its companion documentation repository, `aiops-fabric-docs`.

## Documentation ownership

All maintained documentation belongs in **`aiops-fabric-docs/docs/`**: business and
technical guides, architecture/design, implementation conformance, module guides,
integration and operating guides, test instructions, governance prompts, diagrams,
and documentation screenshots. Do not create narrative documentation or module
READMEs inside `aiops-fabric`.

The implementation repository retains only a short root README and agent guidance
that point here. Executable code, deployment manifests, Helm templates, runtime
catalogs, and machine-readable API/event schemas remain in `aiops-fabric`.

Paths beginning with `docs/` in the design-sync rules below are relative to
`aiops-fabric-docs`. Implementation paths such as `src/`, `contracts/`, `deploy/`,
and `fabric/*.json` are relative to `aiops-fabric`. Keep sibling checkouts for local
design/code validation, or set `DOCS_REPO` when invoking implementation Make targets.
Coordinate related changes across both repositories and record the paired commits
or pull requests before merging a change that affects implementation claims.

Keep documentation free of calendar dates in headings, prose, and fixed examples. Use descriptive
section titles; identify documentation releases and evidence baselines by explicit versions or
commit references when needed. Timestamp examples use format placeholders or values generated
at runtime. Git history retains the chronology of documentation changes.

For each application release, review and commit its matching documentation, then create the same
`vMAJOR.MINOR.PATCH` tag in `aiops-fabric-docs`. Record the paired application/documentation commits
in release notes. Preserve published documentation tags; corrections belong in a new patch release.
See the [release publishing guide](../publishing.md#documentation-per-application-release).

## Mission

ViewSense AI® is a Kubernetes-native, API-first, zero-trust enterprise AI backbone. Preserve component replaceability, provider neutrality, tenant isolation, workload identity, and data ownership boundaries in every change.

## Mandatory design-sync workflow

Before editing code, APIs, deployment assets, policy, dependencies, or runtime configuration:

1. Read `docs/prompts/governance/major-change-policy.md` and classify the change as `minor` or `major`. If uncertain, use `major`.
2. Read the relevant documents under `docs/design/high-level/`, including the enterprise control matrix for changes affecting identity, telemetry, governance, security, operations, or integrations.
3. Record which contracts, trust boundaries, data owners, deployment resources, SLOs, and failure modes change.

In the same coordinated change across the two repositories:

1. Update affected design documents before declaring implementation complete.
2. Update `docs/design/high-level/00-implementation-conformance.md` whenever a service, route, runtime edge, state owner, provider maturity, trust boundary, or verification path changes.
3. Update OpenAPI/event/provider contracts and compatibility notes when behavior changes.
4. Update security controls, threat model, NetworkPolicy/RBAC/secret requirements, and audit events when data flow or access changes.
5. Update deployment manifests, probes, resources, upgrade/rollback, backup/restore, and observability requirements when runtime behavior changes.
6. Add or update unit, contract, integration, and negative security tests proportional to risk.
7. Keep all service logs as structured JSON Lines and preserve request/trace correlation. Never log tokens, credentials, prompts, memory content, or tool payloads by default.
8. When a published Markdown page is added, moved, or renamed, edit its source under
   `aiops-fabric-docs/docs/`, update navigation in `aiops-fabric-docs/zensical.toml`,
   and fix internal links. The build reads `docs/` directly; never edit generated `site/`.
9. Put each module's operator/developer guide under `aiops-fabric-docs/docs/fabric/`.
   Module `contractPaths` retain implementation-relative machine-readable schema paths
   and use `../aiops-fabric-docs/docs/...` sibling paths for Markdown design contracts.
   Validation resolves those paths through `VS_DOCS_DIR` when the checkout is elsewhere.

## Architecture rules

- Use `ViewSense AI®` for the human-facing product name in prose, generated documentation,
  API titles, and operator messages. Preserve established ASCII protocol and deployment identifiers
  such as `X-ViewSense-Tenant`, `viewsense-dev`, `VS_*`, package names, image names, and URLs.
- Communicate across components only through versioned APIs/events; never read another service's database.
- Keep provider SDKs and credentials inside provider adapters.
- Require encrypted transport plus explicit audience/scoped authorization at every internal hop.
- Derive tenant from verified identity; never trust caller-selected tenant headers.
- Use deny-by-default network and authorization policy, least privilege, bounded deadlines/retries, and fail-closed security behavior.
- Keep Kubernetes as the canonical packaging target and confine development resources to `viewsense-dev` unless an environment overlay explicitly defines another namespace.
- Mark mocks, local issuers, static development PKI, and deterministic embeddings as non-production.
- Avoid vendor lock-in in logging/metrics/traces. The production target is JSON stdout, propagated W3C trace context, OpenMetrics, and OTLP-compatible telemetry routed through collectors/exporters; record any implementation gap in the conformance map.

## Required validation

At minimum run:

```bash
make unit
make lint
kubectl kustomize deploy/kubernetes/base >/dev/null
```

For any change to published documentation or its navigation, also run:

```bash
make docs-build
```

The implementation repository delegates this target to `DOCS_REPO` (the sibling
`../aiops-fabric-docs` by default). Its Docker unit/catalog targets mount that repo's
`docs/` read-only using `VS_DOCS_DIR=/documentation`; documentation is not copied into
the application or test image. Direct local pytest runs use the sibling documentation
checkout unless `VS_DOCS_DIR` specifies a different documentation source directory.
Install the pinned docs toolchain in `aiops-fabric-docs/.venv-docs` before building.

For runtime, security, contract, or Kubernetes changes, also run:

```bash
make k8s-deploy
make k8s-test
```

Do not claim Kubernetes security enforcement from manifest validation alone; verify the cluster CNI enforces NetworkPolicy and include negative connectivity tests for production readiness.

## Required completion block

Every completed change must include:

```text
Design Sync Report
- Change Classification: <minor|major>
- Design Docs Updated: <list>
- Code Areas Updated: <list>
- Architecture Delta: <summary>
- Tests/Evidence: <list>
- Known Production Gaps: <list or none>
- Sync Status: <PASS|FAIL>
```

`Sync Status` is `FAIL` when implementation, contracts, security, deployment, observability, tests, or design documentation disagree. Do not merge a failed design sync.
