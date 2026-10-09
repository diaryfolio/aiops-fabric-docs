"""Exercise real tagged snapshots, portable URLs, and repeat deployments."""

import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release_docs", ROOT / "scripts/build-release-docs.py")
releases = importlib.util.module_from_spec(spec)
spec.loader.exec_module(releases)


class ReleasePublishingTest(unittest.TestCase):
    def test_snapshots_preserve_release_content_across_rebuilds(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)

            git("init")
            git("config", "user.name", "Documentation test")
            git("config", "user.email", "docs-test@example.invalid")
            docs = root / "docs"
            docs.mkdir()
            (root / "zensical.toml").write_text('''[project]
site_name = "Test documentation"
site_url = "{{DOCS_SITE_URL}}"
repo_url = "{{DOCS_REPO_URL}}"
repo_name = "{{DOCS_REPO_NAME}}"
docs_dir = "docs"
site_dir = "site"
nav = [{"Home" = "index.md"}]
''')
            (docs / "index.md").write_text("# Home\n\nRelease one content.\n")
            git("add", ".")
            git("commit", "-m", "First snapshot")
            git("tag", "v1.0.0")
            git("tag", "v1.2.0")
            (docs / "index.md").write_text("# Home\n\nRelease ten content.\n")
            git("add", ".")
            git("commit", "-m", "Next snapshot")
            git("tag", "v1.10.0")
            git("tag", "unrelated-tag")
            (docs / "index.md").write_text("# Home\n\nLatest working content.\n")
            env = {"DOCS_SITE_URL": "https://docs.example.org/nested/product/", "DOCS_REPO_URL": "https://github.com/example/docs"}
            with patch.dict(os.environ, env):
                releases.publish(root)
                (docs / "index.md").write_text("# Home\n\nUpdated latest content.\n")
                releases.publish(root)

            site = root / "site"
            versions = json.loads((site / "versions.json").read_text())
            self.assertEqual([v["version"] for v in versions], ["latest", "v1.10.0", "v1.2.0", "v1.0.0"])
            for version, content in {"latest": "Updated latest content.", "v1.0.0": "Release one content.", "v1.10.0": "Release ten content."}.items():
                page = (site / version / "index.html").read_text()
                self.assertIn(content, page)
                self.assertIn(f'https://docs.example.org/nested/product/{version}/', page)
                config = json.loads(re.search(r'<script id="__config" type="application/json">(.*?)</script>', page).group(1))
                self.assertEqual(config["version"]["provider"], "mike")
                self.assertTrue((site / version / "search.json").is_file())
            self.assertIn("location.hash", (site / "index.html").read_text())
            self.assertIn('"latest/"', (site / "index.html").read_text())
            urls = [node.text for node in ET.parse(site / "sitemap.xml").iter() if node.tag.endswith("}loc")]
            self.assertEqual(len(urls), 4)
            self.assertTrue(all(url.startswith(env["DOCS_SITE_URL"]) for url in urls))
            self.assertEqual((docs / "index.md").read_text(), "# Home\n\nUpdated latest content.\n")
            self.assertIn("{{DOCS_SITE_URL}}", (root / "zensical.toml").read_text())
            self.assertIn(env["DOCS_SITE_URL"] + "latest/", (site / "404.html").read_text())
            # A broken new publication must leave the previously built releases available.
            (docs / "index.md").unlink()
            with patch.dict(os.environ, env), self.assertRaises(ValueError):
                releases.publish(root)
            self.assertIn("Updated latest content.", (site / "latest/index.html").read_text())
            self.assertIn("Release one content.", (site / "v1.0.0/index.html").read_text())


if __name__ == "__main__":
    unittest.main()
