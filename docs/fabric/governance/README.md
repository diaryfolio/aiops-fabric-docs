# Governance and Evidence Module

This module is the initial ViewSense AI® sovereign-control plane. It owns provider passports, evaluation records, explicit admission decisions, and payload-minimized execution evidence through an authenticated API and its own PostgreSQL database.

The bundled service is an executable reference. It does not yet claim production policy-engine integration, signed supply-chain verification, immutable/WORM export, legal hold, or automatic routing enforcement. Those controls remain explicit maturity gates in the design and roadmap.

Helm controls are `modules.governance` and `datastores.governance`. Applications never write its database directly.

## Enterprise authorisation control-plane pilot

The [channel-role design](../../design/high-level/10-overall/08-channel-consoles-role-mapping.md)
now extends this owner with framework roles, qualified external mappings, Input bindings, Output
capability grants and immutable reviewed policy revisions. Separate Input/Output pages call its
headless APIs. The selected identity system owns user/group role assignment; the framework owns
resource permissions. A replaceable AuthZ Provider evaluates canonical decisions against reviewed
framework policy; governance validates decisions and retains policy/catalog ownership. Selecting
a combined AuthN/AuthZ product cannot bypass these separate contracts. Keycloak and OPA are examples.

The [enterprise AI governance design](../../design/high-level/10-overall/09-enterprise-ai-governance-egress.md)
adds runtime payload/egress decisions, company-boundary/PII rules, cost policies/reservations and
complete safe evidence. Inspection and final wire checks belong to local processing and provider
adapters; governance does not hold their credentials or capture their payloads. These APIs,
enforcement and budget ledger remain planned. Current explicit provider admission and append-only
evidence endpoints do not enforce runtime privacy, resource grants or hard spending by themselves.

See the [channel console operator guide](channel-console.md) for implemented resources, scopes,
revision handling, review/publication and the synthetic Sales acceptance flow. Runtime dispatch,
external policy adapters and authoritative entitlement refresh remain planned.
