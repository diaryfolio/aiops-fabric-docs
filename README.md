# ViewSense AI® Documentation

The dedicated documentation repository for ViewSense AI® and AIOps Fabric.

Start with the [documentation homepage](docs/index.md). The deployed URL comes from
the repository’s GitHub Pages settings during the build.

The [Business section](docs/BUSINESS_README.md) covers executive context, product compatibility,
use cases and value measures, and adoption responsibilities with simplified management diagrams.

All maintained product documentation lives under `docs/`: business and technical guides,
architecture/design, implementation conformance, module and integration guides, operations
and test instructions, governance prompts, diagrams, and documentation screenshots.
The Zensical site retains the ViewSense AI® stylesheet, logo, and light/dark theme.

Implementation code, runtime catalogs, schemas, and deployment resources remain in the
separate `aiops-fabric` repository. Coordinate related changes across both repositories;
see the [repository instructions](docs/engineering/repository-instructions.md).

## Build and preview

```sh
python3 -m venv .venv-docs
.venv-docs/bin/python -m pip install --requirement requirements-docs.txt
PATH="$(pwd)/.venv-docs/bin:${PATH}" make docs-build
PATH="$(pwd)/.venv-docs/bin:${PATH}" make docs-preview
```

Open <http://127.0.0.1:8765/>. Edit site content in `docs/` and navigation in
`zensical.toml`; generated `site/` output is ignored.

## GitHub Pages

After committing and pushing, select **Settings → Pages → Source → GitHub Actions**.
The **Documentation** workflow builds on pull requests and deploys on relevant
pushes to `main`. It can also be run manually from the Actions tab.
The header's release dropdown offers Latest and documentation tags matching application releases
(for example `v1.2.3`). Pushing a release tag publishes its snapshot alongside existing versions.

See the [publishing guide](docs/publishing.md) for details.
