# ViewSense AI® Agent Runtime Integration

The retained fabric uses an official, unmodified TrueForge release in `trueforge-dev` beside
`viewsense-dev`. All customization stays in fabric-owned adapters and documented upstream
configuration. Source/chart patches, forks and customized upstream images are prohibited.

The owner-authorized clean-state rebuild removes the legacy manual state machine, its run schema,
database and lifecycle API. No manual checkpoint compatibility or business feature parity is claimed.

The implemented route `POST /v1/runtime-check` requires `runtime.verify` and accepts `{}` only.
It creates one fixed synthetic runtime session/turn using the mock model transport. No arbitrary
customer prompt, native MCP, sandbox, schedules, subagents or shared-session business execution
is enabled. The runtime owns sessions/turns; governed memory and evidence remain separate owners.

Use `make k8s-deploy` and `make k8s-test` for the namespace-pair profile and live qualification.
The standalone fabric chart and Compose retain fabric capabilities; selecting `trueforge` in the
catalog does not install an upstream runtime release automatically. See the
[operation record](../../design/high-level/40-ops/03-clean-state-rebuild.md) and
[remaining adoption gates](../../design/high-level/03-trueforge-adoption-decommission.md).
