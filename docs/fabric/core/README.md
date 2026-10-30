# Core API and Runtime Integration Module

The core module retains the authenticated edge and fabric-owned runtime adapter. The agent backend runs
as an independent official release; no upstream customization is permitted. Identity, governance,
provider credentials and long-term memory remain separate fabric boundaries.

- Runtime: `viewsense_gateway` and `viewsense_runtime.gateway`.
- `POST /v1/responses`: retired, authenticated HTTP 410.
- `POST /v1/runtime-check`: fixed synthetic fixture only, `runtime.verify`, empty request body.
- Helm control: `modules.gateway`; upstream release deployment is independent.

The legacy bounded orchestrator and manual agent kernel are removed. Business execution, public
session contracts, idempotent creation, native governed tools and retention guarantees remain gated.
See the [clean-state rebuild](../../design/high-level/40-ops/03-clean-state-rebuild.md).
