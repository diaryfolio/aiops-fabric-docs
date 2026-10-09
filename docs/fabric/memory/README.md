# Memory Module

The `memory-gateway` owns the stable API and policy boundary. Products implement that API behind it.

- `postgres-pgvector`: bundled reference provider and owned PostgreSQL database.
- `mem0-oss-adapter`: bundled ViewSense AI® adapter to an authenticated self-hosted Mem0 REST server.
- `mem0-platform-adapter`: the same boundary adapted to Mem0 Platform `/v1` paths.

The PostgreSQL base reference uses deterministic 64-dimensional test embeddings. Setting
`VS_EMBEDDING_PROVIDER_URL` enables real embeddings through an authenticated adapter. A separate
`memory_embeddings` table stores profile/model/revision/dimensions and retains legacy vectors.
Search refuses partly migrated owner data; `POST /v1/memories:reembed` requires `memory.admin` at
the gateway and backfills bounded batches. The
[local AI integration plan](../../design/high-level/01-project-status-and-local-ai-plan.md#embedding-compatibility-and-migration)
defines the next adapter/client boundary, compatible document/query profiles, and migration of
existing vectors. Selecting or connecting an LLM does not replace these test embeddings.

Choose with `products.memory.product`, `products.memory.endpoint`, and `products.memory.audience` in the ViewSense AI® Helm chart. A new product must pass the memory conformance suite and document export/import, filters, retention, embedding compatibility, residency, backup, and failure semantics.

The adapter hashes tenant/owner identifiers before they leave ViewSense AI®, requires HTTPS, keeps the
Mem0 API key in its own Secret, and normalizes provider responses. The upstream Mem0 product remains
a managed dependency so its model/embedder configuration and lifecycle stay explicit.

`module.json` binds this catalog entry to the gateway/provider source, design contract, Helm paths, data ownership, and supported products.
