#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"
if [[ -x "${repo_root}/.venv-docs/bin/zensical" ]]; then
  exec "${repo_root}/.venv-docs/bin/zensical" build --clean --strict
fi
zensical build --clean --strict
