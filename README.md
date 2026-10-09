# ViewSense AI® Documentation

The dedicated documentation repository for ViewSense AI® and AIOps Fabric.

Expected site URL: <https://diaryfolio.github.io/aiops-fabric-docs/>

This repository reuses the Zensical theme, stylesheet, logo, Markdown extensions,
and GitHub Pages workflow from `aiops-fabric`. It currently contains a starter
homepage; product documentation will be migrated separately.

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

See the [publishing guide](docs/publishing.md) for details.
