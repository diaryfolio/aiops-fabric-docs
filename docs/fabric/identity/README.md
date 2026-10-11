# Identity Module

The identity module defines external enterprise federation and internal workload-token boundaries. The bundled RSA client-credentials issuer and development CA exist only for repeatable local tests.

- Runtime: `viewsense_identity`
- Contract: OAuth client credentials with exact audience and scopes
- Helm selection: `products.identity.product`
- Edge federation: `external-oidc` or `keycloak-oidc` validates issuer, JWKS, audience, scopes,
  subject, and a configured tenant claim before ViewSense AI® creates an internal Trust Envelope.
- Workload identity: `static-development-pki` is executable for tests. SPIRE/mesh is planned;
  current Helm values record intent but do not mount or consume SVIDs.
- Production choice: enterprise OIDC plus renewable workload identity and external secrets.

Keycloak is an optional OIDC provider, not part of the ViewSense AI® trust core. A future SPIRE
integration is a cluster-scoped managed dependency, not an application sidecar bundled into every pod. See
`deploy/integrations/keycloak.md` and `deploy/integrations/spire.md`.

## Planned framework role mapping

[Channel consoles and role mapping](../../design/high-level/10-overall/08-channel-consoles-role-mapping.md)
distinguishes IdP user/group assignment from governance-owned framework roles and channel grants.
Verify a pinned issuer/audience/tenant/client-role source, map exact external roles to framework
roles, then require Input entry and qualified Output action/account/field grants. Existing
`role_scopes` maps external names to broad API scopes; it is not this resource policy. New verified
role extraction, provenance, bounded entitlement freshness and emergency revocation remain planned.
Keycloak remains replaceable through OIDC/explicit mapping, and its administrative credentials
never enter the console, LLM or generic control services.
