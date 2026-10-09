#!/usr/bin/env python3
"""Build latest and release-tag snapshots into one portable Pages artifact."""

import html
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
RELEASE_TAG = re.compile(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?")
spec = importlib.util.spec_from_file_location("docs_build", ROOT / "scripts/build-docs.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def release_tags(root):
    tags = git(root, "-c", "versionsort.suffix=-", "tag", "--list", "--sort=-version:refname").decode().splitlines()
    return [tag for tag in tags if RELEASE_TAG.fullmatch(tag)]


def snapshot(root, ref, destination):
    archive = git(root, "archive", "--format=tar", ref, "docs", "zensical.toml")
    destination.mkdir()
    with tarfile.open(fileobj=io.BytesIO(archive)) as files:
        files.extractall(destination, filter="data")


def redirect(path, target):
    if target.name == "index.html":
        relative = os.path.relpath(target.parent, path.parent).replace(os.sep, "/") + "/"
    else:
        relative = os.path.relpath(target, path.parent).replace(os.sep, "/")
    escaped = html.escape(relative, quote=True)
    # Preserve bookmarked headings and query strings on pre-versioned documentation URLs.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<title>ViewSense AI® Documentation</title>'
        f'<noscript><meta http-equiv="refresh" content="0; url={escaped}"></noscript>'
        f'<script>location.replace(new URL({json.dumps(relative)}, location.href).href'
        ' + location.search + location.hash);</script>'
        f'<p><a href="{escaped}">Read the latest documentation</a></p></html>\n',
        encoding="utf-8",
    )


def publish(root=ROOT):
    root = root.resolve()
    cache = root / ".cache"
    cache.mkdir(exist_ok=True)
    versions = [{"version": "latest", "title": "Latest (main)", "aliases": []}]
    versions.extend({"version": tag, "title": tag, "aliases": []} for tag in release_tags(root))
    with tempfile.TemporaryDirectory(prefix="release-build-", dir=cache) as workspace:
        workspace = Path(workspace)
        publication = workspace / "publication"
        publication.mkdir()
        sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for version in versions:
            name = version["version"]
            checkout = workspace / name
            if name == "latest":
                checkout.mkdir()
                shutil.copytree(root / "docs", checkout / "docs")
                shutil.copyfile(root / "zensical.toml", checkout / "zensical.toml")
            else:
                snapshot(root, f"refs/tags/{name}", checkout)
            print(f"Building documentation version {name}", flush=True)
            builder.build(checkout, version=name)
            if not (checkout / "site" / "index.html").is_file():
                raise ValueError(f"Documentation version {name} has no homepage")
            shutil.move(str(checkout / "site"), publication / name)
            for entry in ET.parse(publication / name / "sitemap.xml").getroot():
                sitemap.append(entry)
        (publication / "versions.json").write_text(json.dumps(versions, indent=2) + "\n")
        ET.ElementTree(sitemap).write(publication / "sitemap.xml", encoding="utf-8", xml_declaration=True)
        for page in (publication / "latest").rglob("*.html"):
            if page.name != "404.html":
                redirect(publication / page.relative_to(publication / "latest"), page)
        homepage = html.escape(builder.site_base() + "latest/", quote=True)
        (publication / "404.html").write_text(
            '<!doctype html><html lang="en"><meta charset="utf-8">'
            '<title>Page not found — ViewSense AI® Documentation</title>'
            '<h1>Page not found</h1>'
            f'<p><a href="{homepage}">Read the latest documentation</a></p></html>\n',
            encoding="utf-8",
        )
        (publication / ".nojekyll").touch()
        # Replace the previous artifact only after every snapshot has built successfully.
        output = root / "site"
        if output.exists():
            shutil.rmtree(output)
        shutil.move(str(publication), output)
    print(f"Built {len(versions)} documentation version(s)", flush=True)


if __name__ == "__main__":
    publish()
