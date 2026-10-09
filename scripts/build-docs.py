#!/usr/bin/env python3
"""Fill the hosting placeholders without modifying tracked site configuration."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]


def repository_url():
    explicit = os.environ.get("DOCS_REPO_URL")
    if explicit:
        return explicit.rstrip("/")
    repository = os.environ.get("GITHUB_REPOSITORY")
    if repository:
        server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
        return f"{server.rstrip('/')}/{repository}"
    remote = subprocess.run(
        ["git", "remote", "get-url", "origin"], cwd=ROOT,
        text=True, capture_output=True, check=False,
    ).stdout.strip()
    if remote.startswith("git@") and ":" in remote:
        host, path = remote[4:].split(":", 1)
        remote = f"https://{host}/{path}"
    parsed = urlsplit(remote)
    if parsed.scheme not in {"http", "https", "ssh"} or not parsed.hostname:
        return ""
    scheme = "https" if parsed.scheme == "ssh" else parsed.scheme
    host = parsed.hostname
    if parsed.port and parsed.scheme != "ssh":
        host += f":{parsed.port}"
    return urlunsplit((scheme, host, parsed.path.removesuffix(".git"), "", "")).rstrip("/")


def site_base():
    site_url = os.environ.get("DOCS_SITE_URL") or "http://127.0.0.1:8765/"
    parsed = urlsplit(site_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.query or parsed.fragment:
        raise SystemExit("DOCS_SITE_URL must be an absolute HTTP(S) URL without a query or fragment")
    return site_url.rstrip("/") + "/"


def build(root=ROOT, *, version=None):
    site_url = site_base()
    repo_url = repository_url()
    repo_name = os.environ.get("DOCS_REPO_NAME") or urlsplit(repo_url).path.strip("/")
    # Keep the config at the root: Zensical requires site_dir within its project root.
    config = root / ".zensical-build.toml"
    source = (root / "zensical.toml").read_text(encoding="utf-8")
    values = {
        "DOCS_SITE_URL": site_url,
        "DOCS_REPO_URL": repo_url,
        "DOCS_REPO_NAME": repo_name,
    }
    for name, value in values.items():
        source = source.replace('"{{' + name + '}}"', json.dumps(value, ensure_ascii=False))
    # Override historical hosting identity too: snapshots must use the current Pages base.
    for key, value in {"site_url": site_url, "repo_url": repo_url, "repo_name": repo_name}.items():
        source = re.sub(rf"^{key} = .*?$", lambda _: f"{key} = {json.dumps(value, ensure_ascii=False)}", source, flags=re.MULTILINE)
    if version and "[project.extra.version]" not in source:
        source += '\n[project.extra.version]\nprovider = "mike"\ndefault = "latest"\n'
    config.write_text(source, encoding="utf-8")
    local = ROOT / ".venv-docs" / "bin" / "zensical"
    executable = str(local) if local.is_file() else shutil.which("zensical")
    if not executable:
        raise SystemExit("Install requirements-docs.txt in .venv-docs or put zensical on PATH")
    print(f"Building documentation for {site_url}", flush=True)
    env = os.environ.copy()
    env.pop("MIKE_DOCS_VERSION", None)
    if version:
        env["MIKE_DOCS_VERSION"] = version
    subprocess.run(
        [executable, "build", "--config-file", str(config), "--clean", "--strict"],
        cwd=root, check=True, env=env,
    )


if __name__ == "__main__":
    build()
