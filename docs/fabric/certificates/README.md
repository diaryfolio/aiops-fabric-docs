# ViewSense AI® Certificates

Independent mTLS/scoped-token API for public certificate inventory, expiry telemetry and approved
cert-manager renewal. CA issuance and private keys stay with cert-manager or an external PKI owner.
The GUI is an optional client. Static development certificates are inventoried, not silently migrated.

The base deploy includes this service; the Helm chart enables it explicitly through
`products.certificates.enabled`. Configure public inventory, namespaces, renewable resource names,
matching Role resourceNames and API-server egress. The POC operator is separately installed.
See the security/operations design and the Keycloak/certificate POC guide for acceptance and gaps.
