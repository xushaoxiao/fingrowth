import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release", ROOT / "scripts/build_release.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ReleaseTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fingrowth-release-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        self.root.mkdir()
        # An isolated git source proves packages use committed files only.
        for name in ("skills", "examples"):
            shutil.copytree(ROOT / name, self.root / name,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for name in ("LICENSE", "VERSION"):
            shutil.copyfile(ROOT / name, self.root / name)
        (self.root / ".gitignore").write_text("__pycache__/\n*.pyc\n")
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Release Test", "-c", "user.email=release@example.invalid",
                 "commit", "-qm", "Synthetic release fixture")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True).strip()

    def test_reproducible_checksums_licenses_and_packaged_execution(self):
        one = Path(self.temp.name) / "one"
        two = Path(self.temp.name) / "two"
        manifest = m.build(self.root, one)
        m.build(self.root, two)
        self.assertEqual({p.name: p.read_bytes() for p in one.iterdir()},
                         {p.name: p.read_bytes() for p in two.iterdir()})
        self.assertEqual(manifest["source_commit"], self.git("rev-parse", "HEAD"))
        self.assertEqual(len(manifest["artifacts"]), 6)
        for item in manifest["artifacts"]:
            payload = (one / item["filename"]).read_bytes()
            self.assertEqual(hashlib.sha256(payload).hexdigest(), item["sha256"])
            self.assertEqual(len(payload), item["bytes"])
        for line in (one / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ")
            self.assertEqual(hashlib.sha256((one / name).read_bytes()).hexdigest(), digest)
        extract = Path(self.temp.name) / "extracted"
        for skill in m.SKILLS:
            with zipfile.ZipFile(one / f"{skill}-0.1.0.zip") as archive:
                self.assertIn(skill + "/SKILL.md", archive.namelist())
                self.assertEqual(archive.read(skill + "/LICENSE"), (ROOT / "LICENSE").read_bytes())
                self.assertFalse(any("__pycache__" in p for p in archive.namelist()))
                archive.extractall(extract)
        result = subprocess.run([sys.executable, "-I", str(extract / "growth-funnel-diagnosis/scripts/analyze.py"),
                                 str(self.root / "examples/lending/cohorts.json")],
                                cwd=extract, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["contribution"], 4000)

    def test_dirty_tree_is_rejected(self):
        (self.root / "VERSION").write_text("0.2.0\n")
        with self.assertRaisesRegex(ValueError, "clean committed"):
            m.build(self.root, Path(self.temp.name) / "out")

    def test_untracked_source_is_rejected(self):
        (self.root / "unexpected.txt").write_text("synthetic")
        with self.assertRaisesRegex(ValueError, "clean committed"):
            m.build(self.root, Path(self.temp.name) / "out")

    def test_existing_artifacts_are_not_overwritten(self):
        output = Path(self.temp.name) / "out"
        m.build(self.root, output)
        with self.assertRaisesRegex(ValueError, "not overwritten"):
            m.build(self.root, output)


class DashboardArchiveTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fingrowth-dashboard-release-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.dashboard = self.base / "out"
        self.dashboard.mkdir()
        self.license_text = (ROOT / "LICENSE").read_bytes()

    def test_static_export_keeps_assets_notices_and_project_license(self):
        html = b"<!doctype html><title>Synthetic FinGrowth fixture</title>"
        notice = b"Synthetic third-party notice fixture; retain this text.\n"
        (self.dashboard / "index.html").write_bytes(html)
        notices = self.dashboard / "_next" / "static" / "notices"
        notices.mkdir(parents=True)
        (notices / "THIRD-PARTY-NOTICES.txt").write_bytes(notice)
        one, two = self.base / "one.zip", self.base / "two.zip"
        m.write_dashboard_zip(one, self.dashboard, self.license_text)
        m.write_dashboard_zip(two, self.dashboard, self.license_text)
        self.assertEqual(one.read_bytes(), two.read_bytes())
        with zipfile.ZipFile(one) as archive:
            self.assertEqual(archive.read("index.html"), html)
            self.assertEqual(archive.read("LICENSE"), self.license_text)
            self.assertEqual(archive.read("_next/static/notices/THIRD-PARTY-NOTICES.txt"), notice)
        self.assertFalse((self.dashboard / "LICENSE").exists())
        self.assertEqual((notices / "THIRD-PARTY-NOTICES.txt").read_bytes(), notice)

    def test_missing_index_does_not_create_an_archive(self):
        output = self.base / "dashboard.zip"
        with self.assertRaisesRegex(ValueError, "missing index.html"):
            m.write_dashboard_zip(output, self.dashboard, self.license_text)
        self.assertFalse(output.exists())

    def test_conflicting_export_license_is_not_silently_overwritten(self):
        (self.dashboard / "index.html").write_text("Synthetic fixture")
        other_license = b"Synthetic exported dependency license fixture\n"
        (self.dashboard / "LICENSE").write_bytes(other_license)
        output = self.base / "dashboard.zip"
        with self.assertRaisesRegex(ValueError, "conflicting LICENSE"):
            m.write_dashboard_zip(output, self.dashboard, self.license_text)
        self.assertFalse(output.exists())
        self.assertEqual((self.dashboard / "LICENSE").read_bytes(), other_license)

    def test_dependency_notice_inventory_is_ordered_relative_and_packaged(self):
        dependencies = self.base / "node_modules"
        fixtures = {
            "z-build-only/NOTICE.txt": "Synthetic build-only notice.\n",
            "next/dist/compiled/example/LICENSE": "Synthetic bundled dependency license.\n",
            "a-package/COPYING.md": "Synthetic package copying terms.\n",
            "a-package/README.md": "Not a notice; excluded.\n",
        }
        for name, text in fixtures.items():
            file = dependencies / name
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(text, encoding="utf-8")
        inventory = m.collect_dependency_notices(dependencies)
        self.assertEqual(inventory, m.collect_dependency_notices(dependencies))
        text = inventory.decode("utf-8")
        self.assertIn("does not claim every listed package is bundled", text)
        self.assertNotIn(str(self.base), text)
        self.assertNotIn("Not a notice; excluded", text)
        expected = ("a-package/COPYING.md", "next/dist/compiled/example/LICENSE", "z-build-only/NOTICE.txt")
        positions = [text.index("===== " + name + " =====") for name in expected]
        self.assertEqual(positions, sorted(positions))
        for name in expected:
            self.assertIn(fixtures[name].strip(), text)
        (self.dashboard / "index.html").write_text("Synthetic fixture")
        (self.dashboard / "THIRD-PARTY-NOTICES.txt").write_text("Retain export notice.\n")
        output = self.base / "dashboard.zip"
        m.write_dashboard_zip(output, self.dashboard, self.license_text, inventory)
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(archive.read("LICENSE"), self.license_text)
            packaged = archive.read("THIRD-PARTY-NOTICES.txt")
            self.assertTrue(packaged.startswith(inventory))
            self.assertIn(b"Retain export notice.", packaged)
        self.assertEqual((self.dashboard / "THIRD-PARTY-NOTICES.txt").read_text(), "Retain export notice.\n")


if __name__ == "__main__":
    unittest.main()
