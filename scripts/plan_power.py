"""Repository entrypoint; implementation belongs to the standalone experiment skill."""
from pathlib import Path
import runpy

_implementation = runpy.run_path(str(
    Path(__file__).resolve().parents[1]
    / "skills/growth-experiment-design/scripts/plan_power.py"
))
plan_power = _implementation["plan_power"]
render_markdown = _implementation["render_markdown"]

if __name__ == "__main__":
    raise SystemExit(_implementation["main"]())
