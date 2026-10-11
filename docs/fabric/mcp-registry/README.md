# MCP Gateway Module

This module is the stable tool-provider catalog and invocation boundary. The current provider
contract is ViewSense AI®-owned `POST /v1/tools/call`; native MCP Streamable HTTP translation and MCP
server hosting are planned. Provider workloads remain separately deployable and do not receive
registry/database access.

The chart enables the gateway, its owned registry database, and an optional safe mock provider
independently. Registration uses an authenticated API and exact HTTPS host allow-list, but no
immutable invocation audit or certification controller ships yet.

`module.json` binds the gateway, registry ownership, design contract, chart controls, and provider maturity into the validated catalog.

## Planned Tool-Sense and Output Channel integration

Tool-Sense names the governed business-tool capability at this boundary. The
[Input/Output Channel design](../../design/high-level/10-overall/07-input-output-channels.md)
maps the Sales Input Channel to the CRM-Logistics1 Output Channel through an approved route and
`sales.opportunities.list` action. The gateway resolves a registered connector, enforces
authenticated channel/route/action/data context, and passes bounded typed parameters; only that
connector owns Oracle credentials and approved query mappings. Channel/route metadata belongs
to governance, tool/provider bindings to this registry, and CRM facts to the CRM owner.

This path is planned. Current registration/invocation does not enforce channel membership,
per-account rules or reply policy, and the chat orchestrator does not invoke this gateway. No
native MCP, Oracle connector, Teams bot or additional Tool-Sense service is implied by the name.
