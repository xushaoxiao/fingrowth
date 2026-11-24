"""Public, read-only FinGrowth demo using the same calculator as the CLI."""
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
from importlib import import_module
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

analyze = import_module("skills.growth-funnel-diagnosis.scripts.analyze_registration_credit").analyze_intake
FIXTURES = Path(__file__).resolve().parents[1] / "examples" / "weekly-cohorts"
CASES = {"mature": "A", "window-open": "B", "missing-definition": "A", "invalid-count": "A"}


CASE_ERRORS = {
    "window-open": "Cohort B registered Nov 16–22. The Nov 23 cutoff leaves some people with less than 7 days of follow-up. Use data through Nov 29 (UTC) or later.",
    "missing-definition": "The KYC stage has no definition. Confirm what counts as a pass before calculating conversion.",
    "invalid-count": "701 people passed KYC, but only 700 completed their profile. These counts cannot describe a nested funnel.",
}


def calculate(case):
    if case not in CASES:
        return 400, {"snapshot": None, "error": "Unknown demo case."}
    intake = json.loads((FIXTURES / f"cohort-{CASES[case]}.json").read_text())
    if case == "missing-definition":
        del intake["stages"][2]["proposed_definition"]
    elif case == "invalid-count":
        intake["stages"][2]["unique_people"] = 701
    try:
        report = analyze(intake)
    except ValueError as exc:
        return 422, {"snapshot": None, "error": CASE_ERRORS.get(case, str(exc)), "detail": str(exc)}
    return 200, {"error": None, "snapshot": {
        "report": report,
        "stages": [{"id": s["id"], "definition": s["proposed_definition"]} for s in intake["stages"]],
        "source": intake["provenance"]["source"],
        "extracted_at": intake["provenance"]["extracted_at"],
        "refreshed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }}


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        case = parse_qs(urlsplit(self.path).query).get("case", ["mature"])[0]
        status, result = calculate(case)
        body = json.dumps(result, allow_nan=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
