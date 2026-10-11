# Governance and Evidence Module

This module is the initial ViewSense AI® sovereign-control plane. It owns provider passports, evaluation records, explicit admission decisions, and payload-minimized execution evidence through an authenticated API and its own PostgreSQL database.

The bundled service is an executable reference. It does not yet claim production policy-engine integration, signed supply-chain verification, immutable/WORM export, legal hold, or automatic routing enforcement. Those controls remain explicit maturity gates in the design and roadmap.

Helm controls are `modules.governance` and `datastores.governance`. Applications never write its database directly.

## Planned enterprise authorisation and execution policy

The [channel-role design](../../design/high-level/10-overall/08-channel-consoles-role-mapping.md)
extends this owner with framework roles, qualified external mappings, Input bindings, Output
capability grants and immutable reviewed policy revisions. Separate Input/Output pages call its
headless APIs. Keycloak owns user/group role assignment; the framework owns resource permissions.

The [enterprise AI governance design](../../design/high-level/10-overall/09-enterprise-ai-governance-egress.md)
adds runtime payload/egress decisions, company-boundary/PII rules, cost policies/reservations and
complete safe evidence. Inspection and final wire checks belong to local processing and provider
adapters; governance does not hold their credentials or capture their payloads. These APIs,
enforcement and budget ledger remain planned. Current explicit provider admission and append-only
evidence endpoints do not enforce runtime privacy, resource grants or hard spending by themselves.
