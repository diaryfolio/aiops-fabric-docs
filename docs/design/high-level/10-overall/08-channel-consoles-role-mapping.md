# ViewSense AI® Channel Consoles and Role Mapping

## Decision and maturity

Provide separate **Input Channels** and **Output Channels** management workspaces, and extend
**Identity & access** with framework roles and external role mappings. All are detachable clients
of authenticated headless APIs. This is a **major, design-only uplift** to the
[channel model](07-input-output-channels.md); the pages, catalogs, grants, administration APIs and
enforcement described here are **planned**, not existing controls.

Attach roles at both channel boundaries with distinct semantics:

- **Input role binding:** permits entry into a business context such as Sales, with permitted
  purposes and entry surfaces. It does not confer CRM access.
- **Output role grant:** permits named capabilities and data scope on CRM-Logistics1, restricted
  to explicitly allowed Input Channels/routes. It is the canonical owner of CRM read/write limits.

The Input page displays effective CRM access by reading these same Output grants. Do not maintain
a second copy of CRM permissions on the Input Channel. A route and Output capability catalog are
ceilings, not permissions automatically inherited by everyone in Sales.

## Provider-neutral authentication and authorisation

Use capability names in the architecture and console, with products selected behind adapters:

| Capability | Responsibility | Example implementation, not a requirement |
|---|---|---|
| **Authentication and Identity Provider (AuthN Provider)** | Authenticate humans/machines; provide verified identity, tenant binding, authentication assurance and external role/group/entitlement assertions | An enterprise OIDC provider; Keycloak is the reference example |
| **Identity Entitlement Adapter** | Normalise approved identity/role sources and establish current entitlement/freshness/revocation; provide an authorised administration reference | Adapter for the selected identity provider or authoritative directory |
| **Authorisation Policy Provider (AuthZ Provider)** | Evaluate canonical subject/resource/action/context against framework grants and policy; return an allow/deny decision and narrowed obligations | Built-in evaluator or an external policy-engine adapter; OPA is an example |
| **Framework governance catalog** | Own framework roles, mappings, Input bindings, Output grants and reviewed policy revisions | Existing governance state domain; independent of the selected AuthN/AuthZ products |

AuthN answers who the caller is and which externally managed assertions are verified. AuthZ
answers what that caller may do to a particular channel/resource under current policy. A valid
identity assertion is input to a resource decision, not permission by itself. A product can supply
both capabilities, but must implement the separate contracts; choosing it for authentication does
not automatically make it the authority for framework policy or CRM capabilities.

OIDC is the current authentication protocol boundary. Other protocols require explicit evaluated
adapters and remain planned; direct product SDKs, management APIs, realm/client terminology and
claim layouts stay inside the relevant adapter/configuration. Framework role IDs, channel grants,
policy input and console forms cannot depend on a particular product's role representation.

Target adapter contracts are:

- **Verified identity assertion:** provider/trust-source revision, opaque issuer/subject,
  identity-derived tenant, authentication assurance, issuance/expiry and approved role-source
  references. Each role assertion includes its source namespace, exact value and observation time.
- **Current entitlements:** scoped identity reference, verified role values and source revision,
  observation time, freshness limit, revocation state and completeness. Unsupported or unavailable
  required freshness yields no execution authority.
- **Authorisation request/decision:** canonical subject/tenant, mapped framework roles and
  provenance, Input/Output/route/action, purpose, data/account/field policies and budgets; result
  includes allow/deny, reason, policy/grant revisions, expiry and enforceable narrowing obligations.
  Governance validates the result and enforcement points apply it. No product-specific policy
  response becomes a grant without validation.

These are planned versioned schemas/APIs. Each provider advertises supported assurance, role
sources, entitlement refresh/revocation and administration/discovery capabilities. No capability
is silently emulated. AuthZ adapters must evaluate the same reviewed framework policy semantics,
including deny precedence and complete-grant rules, and pass the same consumer conformance suite.
Policy-provider changes cannot redefine a grant, ignore an obligation or widen access.

Replace a provider through reviewed trust, adapter and mapping configuration plus conformance
and migration checks. Preserve framework role/channel IDs where semantics are unchanged. Identity
references are qualified by provider/issuer; equal usernames or subject strings across providers
do not establish the same person. Any stable enterprise identity linkage and CRM account mapping
must be explicit, verified and audited before cutover. Do not silently fall back to another IdP,
the development issuer or a more permissive policy engine on failure.

## The Sales CRM Logistics1 role

| Mapping layer | Pilot configuration |
|---|---|
| External identity role | Approved source assertion `sales-crm-logistics1-reader` from the selected AuthN Provider/entitlement adapter |
| Framework role | ID `sales-crm-logistics1`; display name **Sales CRM Logistics1** |
| Input binding | Role may use `sales` through approved chat/API surfaces for `sales.opportunities` |
| Output grant | Role may use `crm-logistics1`, only from `sales` and its approved opportunity route |
| Capability profile | `sales-opportunity-reader`, with explicit action `sales.opportunities.list` |
| Data scope | Accounts currently assigned/otherwise entitled to the verified subject; only approved opportunity fact fields |
| Prohibited by omission | CRM writes, lead creation, customer contact, bulk export, arbitrary SQL, unrelated reads and another CRM |

**Read-only** is a UI label for a reviewed, versioned set of read actions. It is not a wildcard for
every present or future read tool. Adding account-summary reads requires a declared capability,
tool binding and reviewed profile/grant revision. Read permission is still subject to field
masking, purpose, freshness, export, retention and model-egress policy.

```mermaid
flowchart LR
    User["Enterprise user"] --> Identity["AuthN Provider + Identity Entitlement Adapter"]
    Identity --> Token["Verified identity and scoped external roles"]
    Token --> Mapping["Exact external-to-framework role mapping"]
    Mapping --> Role["Sales CRM Logistics1 framework role"]
    Role --> Input["Sales Input binding: enter"]
    Role --> Grant["CRM-Logistics1 Output grant: named read actions"]
    Input --> Policy["AuthZ Provider: complete grant + route + data + egress"]
    Grant --> Policy
    Policy --> Tool["Tool-Sense and CRM connector enforce decision"]
```

This is the target authorisation chain. None of its new edges is implementation evidence.

## Resource and state ownership

| Resource | Required metadata | Authoritative owner |
|---|---|---|
| Framework role | Tenant-scoped immutable ID, label, purpose, owner, enabled state, revision | Governance authorisation catalog |
| External role mapping | Tenant, pinned provider/role-source reference, exact external role value, target framework role, lifecycle/revision | Governance; provider trust and claim extraction remain operator-configured at the edge |
| Input role binding | Role and Input IDs, accepted purposes/surfaces, revision/state | Governance |
| Output capability/profile | Output ID, explicit action IDs, tool/schema versions, side-effect class, data ceiling, revision/state | Governance channel catalog; MCP owns executable tool registration |
| Output role grant | Role, Output, allowed Input/route IDs, profile revision, account/field policies, purpose, conditions, budgets and expiry | Governance |
| User/group role assignment | Identity, memberships, effective external roles and credential lifecycle | Selected AuthN Provider / authoritative identity system |
| Access policy revision | Consistent references to mappings, bindings, profiles, grants and route versions; review and activation evidence | Governance |

Framework roles are portable business authorisation objects, not a duplicate user directory.
Assign users/groups to external roles in the IdP; map those roles into framework roles in ViewSense
AI®. No framework API assigns a human to a role in the first slice. Machine identities require
explicit machine-role mappings and grants; a bot's transport identity cannot impersonate a user.
Governance uses its existing state domain, with tenant-keyed resources and owner APIs. Peers never
query that database. Role labels and client names are not globally unique authorisation keys.

## External identity role mapping

Keep these separate in operator language: the selected identity system assigns roles/groups to
identities; its configured adapter verifies and normalises approved assertions; ViewSense AI® maps
them to framework roles; Output grants define resource capabilities. The identity product does
not need copies of every CRM tool/field permission. Role source selection is explicit provider
configuration, not a fixed client-role claim path in the framework.

Target mapping example; this is not a payload accepted by the existing provider schema:

```json
{
  "id": "identity-sales-logistics1",
  "provider_id": "enterprise-identity",
  "role_source_ref": "approved-application-roles",
  "external_role": "sales-crm-logistics1-reader",
  "framework_role_id": "sales-crm-logistics1",
  "state": "draft",
  "revision": 1
}
```

The pinned role source binds configured provider/trust source, intended audience, adapter extraction
configuration, assertion namespace and allowed tenant relationship. Tenant comes from verified
identity, not this request. Product-specific claim paths exist only in adapter configuration.
The tuple `(tenant, provider, role source, exact role value)` selects a mapping. The same role
string from another issuer, assertion namespace or application grants nothing. Reject malformed role claims,
unbounded lists, unregistered sources and duplicate/conflicting mappings. Do not use fuzzy matching,
case folding, display names or wildcard role values. Unknown roles map to no framework authority.
First-slice mappings have one target role; different external roles/providers can explicitly map
to the same framework role. Framework role inheritance is excluded from the first slice.

ViewSense AI® consumes only verified assertions from approved sources. Provider-specific group
trees, nested/composite roles and membership rules are resolved by the selected identity system/
adapter, not by CRM routing code. Review changes to effective external entitlement semantics and
test normalised assertions. The first release links operators to the configured provider's
administration surface. Optional role discovery uses an isolated read-only adapter, never provider
administrative credentials in a browser, LLM, generic gateway or governance record. Mutating the
external identity system requires a separate audited integration; no bidirectional role
synchronisation is implied.

### Example adapter: Keycloak

Keycloak is one replaceable AuthN Provider, not a framework dependency. An example configuration
uses API resource client `viewsense-api`, a separate browser client and external client role
`sales-crm-logistics1-reader`. Its adapter's approved source reads
`resource_access.viewsense-api.roles`; realm/client role namespaces remain qualified and separate.
The framework receives the same normalised identity/role assertions and **Sales CRM Logistics1**
mapping as any accepted provider. Product claim layouts and audience/role-mapper setup belong in
the [Keycloak example operating guide](../../../deploy/integrations/keycloak.md#planned-business-channel-role-mapping).
Using another conforming provider changes adapter/trust/source configuration, not the Input/
Output permission model. Keycloak is not a prerequisite in the acceptance gates below.

### Compatibility with the current verifier

Today `OIDCProvider.roles_claim` identifies one claim array; `role_scopes` allow-lists external
role names and maps them directly to platform API scopes. `/v1/auth/me` returns those recognised
external roles; `/v1/auth/roles` reports static configuration. These do not create framework roles,
channel bindings or resource grants. A new role omitted from `role_scopes` is currently excluded
from `principal.roles`, even when present in a valid token.

Implementation must extract approved role sources from **verified** claims independently of the
legacy scope mapper, then resolve framework roles through the authorisation catalog. Retain
legacy external role/scopes fields and add explicitly named `framework_roles`, mapping/policy
revisions and entitlement-freshness metadata. A new provider-role-source schema/configuration
version must preserve existing v1 provider configuration; v1 currently forbids unknown fields.
Existing broad scopes such as `api.invoke` are transport permission, not CRM permission. Neither
raw OAuth scopes nor `role_scopes` may bypass the new resource decision on a channel route.

## Effective authorisation and enforcement

Evaluate the request against one complete qualified Output grant at a time:

```text
ALLOW requires valid subject/tenant and approved external-to-framework mapping
  AND an enabled Input binding for that subject's mapped role and requested context
  AND an enabled Output grant matching that role, Input, Output, route, purpose and action
  AND route/profile/provider capability ceilings and required approval
  AND account/field, classification, residency, PII-egress and delivery policies
  AND current revisions/revocation state, freshness, expiry and remaining budget.
```

An explicit deny, missing required decision or unavailable mandatory policy source wins over any
allow. Several roles may supply alternative complete grants; do not combine a write action from
one grant with broader accounts from another, or entry rights from an unrelated role with a grant
whose Input constraint fails. First-slice execution selects one authorising grant; multi-grant
aggregation requires a separate reviewed rule. Result pagination binds subject, grant, route and
policy revision. UI visibility and capability discovery are filtered by this same backend policy.

Edge resolves current mapped roles and Input entry. Governance returns a short-lived,
audience-bound decision/grant tied to the subject, tenant, qualified resource tuple, policy
revisions, account/field-policy reference, permitted action, payload-policy result and budgets.
Orchestrator cannot widen it. Tool-Sense validates the decision and tool/arguments; the connector
enforces trusted account predicates and field allow-lists before query aggregation/model exposure.
The provider adapter checks the actual outbound payload against its egress decision. Recheck
revocation on execution, resume, approval and delivery. Direct calls to tool APIs require equivalent
authorisation; choosing a server name or holding `mcp.invoke` cannot bypass Output grants.

Signed role assertions are a snapshot. Removing an external identity assignment does not by itself rewrite an
already issued token. Target channel policy defines `max_role_age_seconds`; the pilot maximum is
60 seconds, with authoritative entitlement revalidation or a supported revocation feed required
once the assertion exceeds that age. Measure age from the verified assertion/revalidation time,
never from each request/cache read. Policy changes and emergency role/mapping/grant disables
invalidate decisions through a monotonic authorisation epoch before another protected operation.
IdP removal is bounded by the validated feed/refresh interval, not claimed instantaneous.

If current entitlement cannot be established within that bound, deny the protected action.
Introspection validity alone is not proof of updated role membership. Implement and test a
provider-specific entitlement adapter or freshness mechanism before enabling this strict route;
short token lifetime alone is insufficient if it exceeds the configured bound. Long-running
operations require refresh/recheck, including final delivery; in-flight external bytes cannot be
recalled. Emergency disable blocks subsequent dispatch/delivery and cancels work where supported.

## Console pages

Keep persistent verified tenant/environment context. Add shareable `?page=input-channels` and
`?page=output-channels` workspaces to the management console; add **Framework roles** and
**Identity mappings** tabs under `?page=identity`. IDs in URLs are selection only, not tenant overrides.
These pages manage configuration; ordinary employees select permitted channels in chat/API clients.

Identity & access also separates **Authentication providers** from **Authorisation providers**:
show selected adapter, protocol/capability support, trust/policy revision and independently observed
health. Product labels appear as configured implementations, not fixed workspace names. **Manage
identities** opens an approved provider administration reference. Provider selection is a reviewed
configuration plan, not an immediate trust switch; cutover requires identity linkage, fresh grants,
policy conformance and revocation/session handling. UI removal leaves both provider contracts usable.

| Workspace | List view | Detail tabs and actions |
|---|---|---|
| Input Channels | Name, owner, accepted surfaces, attached role count, route count, policy revision, enabled state | Overview; Entry roles; Output access; Routes; Delivery/retention; Audit |
| Output Channels | Name, application owner, connector, capability profile count, granted role count, catalog state, separately observed health | Overview; Capabilities; Role grants; Data/egress policy; Connector status; Audit |
| Framework roles | Role name/ID, owner, mapped IdP sources, Input bindings, Output grants, revision/state | Overview; External mappings; Channel access; Policy preview; Audit |
| Identity mappings | Provider/role source, external role, framework role, active revision and validation status | Select configured provider/source; exact role value; target role; validate, preview and draft lifecycle |

Input **Entry roles** attaches a framework role to Sales with purposes/surfaces. **Output access**
shows a derived matrix: `Sales CRM Logistics1 | CRM-Logistics1 | Read-only: opportunity list |
assigned accounts | sales.opportunities route | grant revision`. Edit links open the single
authoritative grant editor in the Output workspace; no duplicate permission checkbox is stored.

Output **Capabilities** lists exact actions, read/write/destructive class, tool/schema revision,
required fields and conditions. **Role grants** selects the framework role, allowed Inputs/routes,
explicit profile revision, dynamic account-policy and field-policy references, purpose, limits and
approval requirements. **Data/egress policy** shows model destinations, PII handling, allowed
regions and retention ceiling. A role grant can narrow, never relax, Output or enterprise ceilings.

Target grant example; all referenced resources must exist in the same identity-derived tenant,
with matching Output/action schemas and reviewed immutable revisions:

```json
{
  "id": "sales-logistics1-opportunity-read",
  "framework_role_id": "sales-crm-logistics1",
  "output_channel_id": "crm-logistics1",
  "allowed_input_channel_ids": ["sales"],
  "allowed_route_ids": ["sales-logistics1-opportunities"],
  "capability_profile_ref": {"id": "sales-opportunity-reader", "revision": 1},
  "account_policy_ref": "crm-assigned-accounts",
  "field_policy_ref": "crm-opportunity-facts",
  "purpose": "sales.opportunities",
  "state": "draft",
  "revision": 1
}
```

The referenced profile lists `sales.opportunities.list` explicitly. Dynamic account assignments
are enforced against current CRM-owner entitlements at query time, not copied into a role JWT.
Effective budgets/limits narrow to the strictest applicable enterprise, tenant, route and grant
ceiling; role union never adds budget. Cross-tenant references fail validation before publication.

For CRM-Logistics1 the grant editor shows **Sales CRM Logistics1**, Input **Sales**, profile
**Read-only — Sales opportunities**, action **List sales opportunities**, account scope
**Assigned accounts**, and the permitted fact fields. Creation/contact/export actions remain
outside this grant. Buttons use business labels; protocol/connector details sit in operator
detail panels. Saving a grant does not test Oracle, activate a provider or create external identity roles.

Every detail page distinguishes draft/active/disabled configuration, mapping validation, provider
admission and live connector health. An unavailable API has an unavailable state and no fabricated
data/success. API errors retain safe request IDs. Revision conflicts require refresh/review.
Keyboard-accessible forms, labelled controls and readable permission tables are acceptance gates.
URL filters and displayed role names must be escaped; restricted resource names are not exposed
to unauthorised users.

### Administration and publication

Separate metadata editing, capability/profile management, role/mapping/grant management, review/
activation and audit viewing. Proposed scopes are `channels.read`, `channels.admin`, `authz.read`,
`authz.admin`, `authz.review` and `authz.simulate`, each further constrained by tenant, resource and
operation policy. They are not existing scopes. Channel administration does not grant business
data access or permission to administer an external identity product; role admins cannot approve their own expansion.
Initial admin authority comes from explicitly provisioned operator identities, not from a role a
user creates in the console.

Edit a draft, validate references and safety ceilings, simulate effects, review the before/after
diff, then publish an immutable policy revision atomically. Privilege expansion requires an
independent authorised reviewer and recorded approval; editing the draft never affects execution.
Enable only when required schema/tool mappings, source validation and tests are satisfied. A
protected emergency disable is immediate and audited without waiting for a publication review.
Rollbacks create a new reviewed revision and cannot re-enable a revoked identity/provider.
Referenced profiles are immutable revisions; registering a new tool cannot expand a live profile.

**Policy preview** reports allowed/denied actions, reason codes and the exact mapping/binding/
grant/route/egress policy revisions. Synthetic subjects are available to authorised policy admins
only; actual-user lookup requires separate permission. Preview evaluates no CRM query, creates no
execution token and cannot impersonate the tested subject. Standard users can inspect only their
own safe effective permissions. Full token paste/upload and raw CRM payloads are excluded.

## Planned headless APIs and contracts

| Backend owner | Target surface | Contract requirement |
|---|---|---|
| Governance | `/v1/framework-roles`, `/v1/idp-role-mappings`, `/v1/input-role-bindings`, `/v1/output-capability-profiles`, `/v1/output-role-grants` | Filtered list/detail and draft create/update APIs; stable tenant-scoped IDs, authenticated tenancy, pagination and optimistic revisions |
| Governance | `/v1/access-policy-revisions`, `/{id}:validate`, `/{id}:activate`; resource `:disable` operations | Atomic activation of reviewed references; safe disable, revocation epoch, immutable history and audit |
| Governance | `POST /v1/authorization:simulate`, `POST /v1/authorization:decide` | Non-executing scoped preview versus authenticated narrowed execution decision; no caller-supplied roles treated as authority |
| Edge | `GET /v1/auth/channel-access`; additive `/v1/auth/me` fields | Own effective Input/Output/action summary and framework-role provenance; no administrator catalog leakage |
| Edge facade | Explicit authorised proxies for the above management APIs | Same owner contracts and delegated human identity; no generic URL/path proxy |

CRUD verbs and schemas must be frozen during the contract slice, including `If-Match`/revision
conflicts, idempotent draft creates, review evidence and disable semantics. Schema families cover
framework roles, qualified external mappings, Input bindings, capability profiles, Output grants,
policy snapshots, decisions and safe effective-access summaries. Machine-readable assets belong
in the implementation repository; none is shipped by this design. Console calls these backend
APIs and owns no grant database or policy algorithm. Existing `/v1/auth/roles` remains a legacy
scope-policy view; it is not silently renamed or treated as the new framework-role catalog.

## Delivery and acceptance gates

1. Implement versioned resource/decision schemas, governance APIs, atomic revisions, scoped
   administration and exact external-role extraction/mapping. Preserve old IdP/client behaviour.
2. Implement qualified-grant evaluation, current entitlement/freshness/revocation, narrowed
   delegation and connector enforcement; verify allow/deny headlessly before attaching a GUI.
3. Implement Input/Output pages and Identity role/mapping tabs on the same APIs, then pilot the
   Sales reader path with the existing CRM/channel delivery requirements.

Required evidence: an approved external role assertion permits Sales opportunity reads for assigned
accounts; assertion-source/application/issuer/tenant collisions, malformed claims and unknown roles grant
nothing. Missing Input binding or Output grant denies; Support cannot reuse a Sales-only grant;
another CRM, unlisted read, write, export and outreach deny. Multiple roles cannot manufacture
action/account combinations. Disabled mappings/grants, role removal, stale claims, feed outage,
mid-run revision changes and scoped cursors follow the documented bounds.

Test denied admin/self-approval/tenant changes, draft isolation, stale updates, atomic activation,
profile immutability, safe previews and disable/rollback. Prove direct MCP calls enforce the same
policy. Headless and console permission matrices must match; hiding a button cannot authorise a
backend operation. Test navigation, inaccessible deep links, empty/error/loading states, keyboard
operation, separate configuration/health and GUI removal. Demonstrate secret/PII-free logs and
safe lineage showing external source → framework role → Input binding → Output grant → decision.

Run the same identity/mapping/freshness suite against two distinct adapters: the selected reference
product and an independent standards-based fixture/provider. Verify that an AuthN/entitlement
adapter swap preserves qualified framework roles, subject isolation and channel permissions after
reviewed identity linkage, without changing console or CRM code. Run the same canonical decision
tests against built-in and selected external AuthZ evaluators; incompatible policy semantics,
missing capabilities and unavailable mandatory providers deny. These are target replaceability
gates, not claims that two production products are certified.

All runtime, identity-provider freshness, UI and CRM evidence remains pending implementation.
