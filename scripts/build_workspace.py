"""Repository entrypoint for the standalone data-adapter skill."""
from pathlib import Path
import runpy

_implementation = runpy.run_path(str(
    Path(__file__).resolve().parents[1]
    / "skills/growth-data-adapter/scripts/build_workspace.py"
))
build_workspace = _implementation["build_workspace"]
validate_workspace = _implementation["validate_workspace"]
serialize_workspace = _implementation["serialize_workspace"]
validate_cohort = _implementation["validate_cohort"]
STAGES = _implementation["STAGES"]
MONEY = _implementation["MONEY"]
TARGETS = _implementation["TARGETS"]

if __name__ == "__main__":
    raise SystemExit(_implementation["main"]())
