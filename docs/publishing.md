# Publishing the ViewSense AI® Documentation

This repository uses the Zensical toolchain and ViewSense AI® presentation layer
from `aiops-fabric`.

## Presentation layer

- `assets/stylesheets/viewsense.css` provides the original navy-and-teal colours,
  typography, homepage cards, tables, navigation, and light/dark styling.
- `assets/images/viewsense-mark.svg` is the original logo and favicon.
- `zensical.toml` connects the assets, theme, Markdown extensions, and navigation.

The homepage cards originate as an ordinary ordered Markdown list under
**Explore ViewSense AI®**. The stylesheet turns that list into a responsive card grid.

## Local build and preview

From the repository root:

```sh
python3 -m venv .venv-docs
.venv-docs/bin/python -m pip install --requirement requirements-docs.txt
PATH="$(pwd)/.venv-docs/bin:${PATH}" make docs-build
PATH="$(pwd)/.venv-docs/bin:${PATH}" make docs-preview
```

Open <http://127.0.0.1:8765/>. Press `Ctrl-C` to stop the preview server.
The strict build writes the generated site into `site/`. Generated output, caches,
and the local virtual environment are ignored by Git.

## Source and navigation

Edit Markdown in `docs/`; never edit generated files in `site/`. When adding a page,
add its path relative to `docs/` to the navigation in `zensical.toml`, then run
`make docs-build` to verify the site.

This dedicated repository builds `docs/` directly, so it does not need the original
application repository's curated staging directory or document-copy allow-list.
The product documentation will be migrated in a separate step.

## GitHub Pages setup

1. Commit and push the repository changes.
2. Open the repository's **Settings → Pages**.
3. Under **Build and deployment → Source**, select **GitHub Actions**.
4. Run the **Documentation** workflow from the Actions tab, or push a change to `main`.
5. Check that the build and deployment jobs succeed.

The expected URL is <https://diaryfolio.github.io/aiops-fabric-docs/>.

The workflow validates documentation on pull requests and publishes the `site/`
artifact on pushes to `main`. It also supports manual runs. Deployment uses the
`github-pages` environment with Pages write and OIDC token permissions; the build
job only needs repository read permission. No personal access token is required.
