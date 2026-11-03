"""Build reproducible, licensed skill ZIPs from a clean committed checkout."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import zipfile

SKILLS = ("fintech-growth-architect", "growth-metric-tree",
          "growth-funnel-diagnosis", "growth-experiment-design", "growth-data-adapter")
ZIP_TIME = (2026, 1, 1, 0, 0, 0)


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def write_zip(path, files):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, content)


def collect_dependency_notices(node_modules):
    """Read an ordered inventory without importing or executing dependencies."""
    node_modules = Path(node_modules)
    if not node_modules.is_dir():
        raise ValueError("dependency notices require an installed node_modules directory")
    sections = [
        "Installed build dependency notices inventory\n"
        "Collected from LICENSE*, LICENCE*, COPYING* and NOTICE* files in node_modules.\n"
        "Includes build-only dependencies; this does not claim every listed package is bundled.\n"
    ]
    notices = [file for file in node_modules.rglob("*")
               if file.is_file() and not file.is_symlink()
               and file.name.upper().startswith(("LICENSE", "LICENCE", "COPYING", "NOTICE"))]
    for file in sorted(notices, key=lambda item: item.relative_to(node_modules).as_posix()):
        relative = file.relative_to(node_modules).as_posix()
        text = file.read_bytes().decode("utf-8", errors="replace")
        sections.append(f"\n===== {relative} =====\n{text.rstrip()}\n")
    return "".join(sections).encode("utf-8")


def write_dashboard_zip(path, dashboard, license_text, dependency_notices=None):
    """Package the static export with its project license and existing notices."""
    dashboard = Path(dashboard)
    if not (dashboard / "index.html").is_file():
        raise ValueError("dashboard export is missing index.html")
    files = {file.relative_to(dashboard).as_posix(): file.read_bytes()
             for file in dashboard.rglob("*") if file.is_file()}
    if "LICENSE" in files and files["LICENSE"] != license_text:
        raise ValueError("dashboard export has a conflicting LICENSE; preserve it under a distinct notice filename")
    files["LICENSE"] = license_text
    if dependency_notices is not None:
        existing = files.get("THIRD-PARTY-NOTICES.txt")
        files["THIRD-PARTY-NOTICES.txt"] = dependency_notices
        if existing is not None:
            files["THIRD-PARTY-NOTICES.txt"] += b"\n===== Static export supplied notices =====\n" + existing
    write_zip(path, files)


def build(root, output, include_dashboard=False):
    root, output = Path(root).resolve(), Path(output).resolve()
    if git(root, "status", "--porcelain", "--untracked-files=all"):
        raise ValueError("release builds require a clean committed checkout")
    if output.exists() and any(output.iterdir()):
        raise ValueError("output directory must be new or empty; existing artifacts are not overwritten")
    # Read committed objects, not working-tree transformations or local files.
    commit = git(root, "rev-parse", "HEAD")
    if include_dashboard:
        environment = {**os.environ, "FINGROWTH_BUILD_ID": commit}
        for command in (["npm", "ci"], ["npm", "run", "typecheck"],
                        ["npm", "test"], ["npm", "run", "build"]):
            subprocess.run(command, cwd=root / "dashboard", env=environment, check=True)
        if git(root, "rev-parse", "HEAD") != commit or git(root, "status", "--porcelain", "--untracked-files=all"):
            raise ValueError("source changed during the dashboard build; review and rebuild")
    paths = subprocess.check_output(["git", "-C", str(root), "ls-tree", "-r", "--name-only", "-z", commit]).decode().rstrip("\0").split("\0")
    contents = {path: subprocess.check_output(["git", "-C", str(root), "show", commit + ":" + path]) for path in paths}
    version = contents["VERSION"].decode().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("VERSION must be a stable semantic version such as 0.1.0")
    license_text = contents["LICENSE"]
    for skill in SKILLS:
        if f"skills/{skill}/SKILL.md" not in contents:
            raise ValueError("missing skill: " + skill)
    output.mkdir(parents=True, exist_ok=True)
    artifacts = []
    source_name = f"fingrowth-{version}"
    write_zip(output / (source_name + ".zip"),
              {f"{source_name}/{path}": value for path, value in contents.items()})
    artifacts.append(source_name + ".zip")
    for skill in SKILLS:
        prefix = "skills/" + skill + "/"
        files = {skill + "/" + path[len(prefix):]: value
                 for path, value in contents.items() if path.startswith(prefix)}
        files[skill + "/LICENSE"] = license_text
        name = f"{skill}-{version}.zip"
        write_zip(output / name, files)
        artifacts.append(name)
    if include_dashboard:
        dashboard = root / "dashboard/out"
        name = f"fingrowth-dashboard-{version}.zip"
        write_dashboard_zip(output / name, dashboard, license_text,
                            collect_dependency_notices(root / "dashboard/node_modules"))
        artifacts.append(name)
    manifest = {
        "version": version,
        "source_commit": commit,
        "source_tree": git(root, "rev-parse", commit + "^{tree}"),
        "artifacts": [{"filename": name,
                       "sha256": hashlib.sha256((output / name).read_bytes()).hexdigest(),
                       "bytes": (output / name).stat().st_size}
                      for name in sorted(artifacts)],
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    checksum_names = sorted(artifacts + ["manifest.json"])
    (output / "SHA256SUMS").write_text("".join(
        f"{hashlib.sha256((output / name).read_bytes()).hexdigest()}  {name}\n"
        for name in checksum_names), encoding="utf-8")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("dist"))
    parser.add_argument("--include-dashboard", action="store_true",
                        help="install locked dashboard dependencies, check/build and package its static export")
    args = parser.parse_args(argv)
    try:
        manifest = build(Path(__file__).resolve().parents[1], args.output, args.include_dashboard)
    except (OSError, ValueError, subprocess.CalledProcessError, KeyError) as exc:
        print("Release build failed: " + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
