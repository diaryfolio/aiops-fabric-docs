#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"
if [[ -x "${repo_root}/.venv-docs/bin/python" ]]; then
  exec "${repo_root}/.venv-docs/bin/python" scripts/build-docs.py
fi
exec python3 scripts/build-docs.py
