"""Analyze synthetic nested cohorts with Python 3.10+ and no dependencies."""
import argparse
from datetime import date
from decimal import Decimal
import json
import math
from pathlib import Path
import re
import sys

STAGES = ("acquired", "registered", "kyc", "applied", "approved", "accepted",
          "disbursed", "repaid", "repeat")
COSTS = ("acquisition_cost", "credit_loss", "funding_cost", "servicing_cost", "incentives")
FIELDS = set(COSTS) | {"cohort", "window", "outcome_as_of", "currency", "synthetic",
                       "mature", "counts", "revenue"}


def _iso_date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("dates must use YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError("invalid calendar date") from None


def _money(value, field):
    if type(value) not in (int, float):
        raise ValueError("invalid monetary value: " + field)
    try:
        valid = math.isfinite(value) and value >= 0
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError("invalid monetary value: " + field)
    return Decimal(str(value))


def analyze(row):
    if not isinstance(row, dict) or set(row) != FIELDS:
        raise ValueError("cohort must contain exactly the documented fields")
    if row["synthetic"] is not True:
        raise ValueError("analyzer accepts explicitly synthetic fixtures only")
    if type(row["mature"]) is not bool:
        raise ValueError("mature must be an explicit boolean")
    if not isinstance(row["cohort"], str) or not row["cohort"].strip():
        raise ValueError("cohort must be a nonempty label")
    if not isinstance(row["currency"], str) or not re.fullmatch(r"[A-Z]{3}", row["currency"]):
        raise ValueError("currency must be a three-letter uppercase code")
    window = row["window"]
    if not isinstance(window, str) or len(window.split("/")) != 2:
        raise ValueError("window must use YYYY-MM-DD/YYYY-MM-DD")
    start, end = map(_iso_date, window.split("/"))
    observed = _iso_date(row["outcome_as_of"])
    if start > end or observed < end:
        raise ValueError("window must be ordered and end no later than outcome_as_of")

    counts = row["counts"]
    if not isinstance(counts, dict) or set(counts) != set(STAGES):
        raise ValueError("counts must contain exactly the documented stages")
    previous = None
    for stage in STAGES:
        count = counts[stage]
        if type(count) is not int or count < 0 or (previous is not None and count > previous):
            raise ValueError("counts must be nonnegative nested integer populations")
        previous = count
    money = {field: _money(row[field], field) for field in COSTS + ("revenue",)}
    contribution = float(money["revenue"] - sum(money[k] for k in COSTS))
    if not math.isfinite(contribution):
        raise ValueError("monetary totals exceed supported numeric range")

    steps = []
    for source, target in zip(STAGES, STAGES[1:]):
        conversion = counts[target] / counts[source] if counts[source] else None
        steps.append({"from": source, "to": target, "population": counts[source],
                      "converted": counts[target], "not_progressed": counts[source] - counts[target],
                      "conversion": conversion})
    # Repayment/repeat are delayed outcomes. Approval reflects policy as well
    # as behavior, so ranking never implies that approval should increase.
    journey = steps[:STAGES.index("disbursed")]
    by_volume = sorted((s for s in journey if s["not_progressed"] > 0),
                       key=lambda s: -s["not_progressed"])
    by_rate = sorted((s for s in journey if s["conversion"] is not None),
                     key=lambda s: s["conversion"])
    warnings = [
        "Synthetic descriptive cohorts do not establish causes or experiment uplift.",
        "Approval gaps include policy rejection; repayment/repeat are delayed outcomes, not UX drop-off.",
        "Maturity is declared by the fixture, not verified from exposure or repayment schedules.",
    ]
    if not row["mature"]:
        warnings.append("Immature cohort: contribution is unknown; do not select or scale a winner.")
    if not counts["disbursed"]:
        warnings.append("No funded people: funded CAC is unknown.")
    return {
        "cohort": row["cohort"], "currency": row["currency"], "window": window,
        "outcome_as_of": row["outcome_as_of"], "mature": row["mature"],
        "rates": {s["from"] + "->" + s["to"]: s["conversion"] for s in steps},
        "funded_cac": row["acquisition_cost"] / counts["disbursed"] if counts["disbursed"] else None,
        "contribution": contribution if row["mature"] else None,
        "steps": steps,
        "investigation_candidates": {
            "by_not_progressed": by_volume,
            "by_lowest_conversion": by_rate,
        },
        "warnings": warnings,
        "explanation": "contribution = revenue - acquisition - credit loss - funding - servicing - incentives; immature contribution is unknown",
    }


def analyze_document(rows):
    if not isinstance(rows, list) or not rows:
        raise ValueError("document must be a nonempty JSON array of cohorts")
    results = []
    identities = set()
    for index, row in enumerate(rows):
        try:
            result = analyze(row)
            identity = (result["cohort"], result["window"])
            if identity in identities:
                raise ValueError("duplicate cohort and window")
            identities.add(identity)
            results.append(result)
        except ValueError as exc:
            raise ValueError(f"cohort[{index}]: {exc}") from None
    # Do not combine currencies, dates or populations implicitly.
    return results


def _text(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(
        ">", "&gt;").replace("|", "&#124;").replace("\n", " ").replace("\r", " ")


def _number(value):
    return "unknown" if value is None else f"{value:,.2f}"


def render_markdown(results):
    lines = ["# FinGrowth synthetic cohort report", "",
             "Descriptive evidence only. No automatic launch or underwriting decision.", ""]
    for result in results:
        lines.extend([
            "## " + _text(result["cohort"]), "",
            f"Window: {_text(result['window'])}; outcomes as of {_text(result['outcome_as_of'])}.",
            f"Currency: {result['currency']}; declared mature: {str(result['mature']).lower()}.", "",
            f"Funded CAC: {_number(result['funded_cac'])}; contribution: {_number(result['contribution'])}.", "",
            "| Transition | Population | Progressed | Not progressed | Conversion |",
            "| --- | ---: | ---: | ---: | ---: |",
        ])
        for step in result["steps"]:
            rate = "unknown" if step["conversion"] is None else f"{step['conversion']:.2%}"
            lines.append(f"| {step['from']} → {step['to']} | {step['population']} | {step['converted']} | {step['not_progressed']} | {rate} |")
        candidates = result["investigation_candidates"]
        lines.extend(["", "### Investigation candidates", ""])
        for key, label in (("by_not_progressed", "Largest count not progressing"),
                           ("by_lowest_conversion", "Lowest observed conversion")):
            ranked = candidates[key]
            # Include ties instead of inventing a unique bottleneck.
            field = "not_progressed" if key == "by_not_progressed" else "conversion"
            top = [s for s in ranked if s[field] == ranked[0][field]] if ranked else []
            names = ", ".join(s["from"] + " → " + s["to"] for s in top) or "unknown / no observed gap"
            lines.append(f"- {label}: {names}.")
        lines.extend(["", "These rankings use acquired → disbursed only. Confirm event delivery, cohort mix and policy reasons before assigning a cause.",
                      "", "### Evidence needed before action", "",
                      "- Data owner: check unique-person joins, event delays and ledger reconciliation.",
                      "- Product/engineering: split technical errors, abandonment and policy decisions with approved aggregate reason codes.",
                      "- Risk/finance: check comparable risk mix and mature loss before any scale decision.", ""])
        lines.extend("- " + warning for warning in result["warnings"])
        lines.extend(["", result["explanation"], ""])
    return "\n".join(lines)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="synthetic cohort JSON array")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        with args.input.open(encoding="utf-8") as stream:
            rows = json.load(stream, object_pairs_hook=_unique_object)
        results = analyze_document(rows)
        output = (json.dumps(results, indent=2, allow_nan=False) if args.format == "json"
                  else render_markdown(results))
    except (ValueError, OSError, UnicodeError, OverflowError) as exc:
        # No partial report is written on invalid input.
        print("Invalid input: " + str(exc), file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
