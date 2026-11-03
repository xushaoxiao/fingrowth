"""Repository entrypoint; the implementation ships inside the standalone skill."""
from pathlib import Path
import runpy

_implementation = runpy.run_path(str(
    Path(__file__).resolve().parents[1]
    / "skills/growth-funnel-diagnosis/scripts/analyze.py"
))
STAGES = _implementation["STAGES"]
COSTS = _implementation["COSTS"]
analyze = _implementation["analyze"]
analyze_document = _implementation["analyze_document"]
render_markdown = _implementation["render_markdown"]

if __name__ == "__main__":
    raise SystemExit(_implementation["main"]())
