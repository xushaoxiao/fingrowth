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


if __name__ == "__main__":
    unittest.main()
