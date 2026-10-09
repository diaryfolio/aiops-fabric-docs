# ViewSense AI® documentation repository

This is the canonical home for all ViewSense AI® / AIOps Fabric documentation. Maintain
business/technical guides, design, implementation conformance, module/integration/operations
and test guides, governance prompts, diagrams, and screenshots under `docs/`.

Read `docs/engineering/repository-instructions.md` and `docs/prompts/governance/major-change-policy.md`.
Implementation, runtime manifests, catalogs, and machine-readable schemas belong in the separate
`aiops-fabric` repository. Document implementation changes here and record paired commits or PRs.

Update `zensical.toml` navigation and internal links whenever pages move or are added. Preserve
the ViewSense AI® theme and ordinary GitHub-readable Markdown. Edit sources, never `site/`.
Run `make docs-build` after documentation/navigation changes. Keep generated site/cache/environment
files untracked. Public documentation must not link users to the closed-source implementation repo.
