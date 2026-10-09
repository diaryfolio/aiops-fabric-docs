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

Keep documentation free of calendar dates in headings, prose, and fixed examples. Use descriptive
section titles and, when identifying a release or evidence baseline, explicit versions or commit
references. Timestamp examples should use format placeholders or values generated at runtime.
Match documentation release tags to application versions and preserve published tags. Keep the
publishing toolchain compatible with every retained snapshot and run the release publishing tests
when modifying versioned builds or navigation.
