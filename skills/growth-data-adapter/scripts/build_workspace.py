"""Map declared aggregate JSON rows into a validated FinGrowth dashboard workspace."""
import argparse
from datetime import date, datetime
from decimal import Decimal
import json
import math
from pathlib import Path
import re
import sys
import tempfile

STAGES = ("acquired", "registered", "kyc", "applied", "approved", "accepted",
          "disbursed", "repaid", "repeat")
MONEY = ("acquisition_cost", "revenue", "credit_loss", "funding_cost", "servicing_cost", "incentives")
ROW_FIELDS = {"cohort", "window", "outcome_as_of", "currency", "synthetic", "mature", "counts", *MONEY}
TARGETS = ROW_FIELDS - {"counts"} | {"counts." + stage for stage in STAGES}
WORKSPACE_FIELDS = {"schema_version", "name", "description", "data_mode", "provenance", "cohorts", "experiments", "initiatives"}
PROVENANCE_FIELDS = {"source", "extracted_at", "timezone", "cohort_definition", "approval_reference", "mappings"}
EXPERIMENT_FIELDS = {"id", "title", "status", "owner", "primary_metric", "hypothesis", "guardrails", "next_action"}
INITIATIVE_FIELDS = {"id", "title", "owner", "status", "acceptance", "dependency"}
MAX_SAFE_INTEGER = 9007199254740991
MAX_MONEY = Decimal("1000000000000")
MAX_TEXT_LENGTH = 10000
MAX_COHORTS = 200
MAX_COLLECTION = 1000
MAX_WORKSPACE_BYTES = 2000000


def _object(value, fields, label):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError(label + " must contain exactly the documented fields")


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + " must be a nonempty string")
    # Match JavaScript string.length, including supplementary Unicode symbols.
    if len(value.encode("utf-16-le", "surrogatepass")) // 2 > MAX_TEXT_LENGTH:
        raise ValueError(label + " must be at most 10000 characters")


def _date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("cohort dates must use YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError("invalid cohort calendar date") from None


def _timestamp(value):
    _text(value, "extracted_at")
    match = re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?(?:Z|[+-](\d{2}):(\d{2}))", value
    )
    if not match:
        raise ValueError("extracted_at must be an ISO timestamp with an explicit UTC offset")
    hour, minute, second, offset_hour, offset_minute = match.groups()
    if (int(hour) > 23 or int(minute) > 59 or int(second) > 59
            or (offset_hour is not None and (int(offset_hour) > 23 or int(offset_minute) > 59))):
        raise ValueError("invalid extracted_at timestamp clock or UTC offset")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.utcoffset() is None:
            raise ValueError
    except ValueError:
        raise ValueError("invalid extracted_at timestamp") from None


def validate_cohort(row, mode):
    _object(row, ROW_FIELDS, "cohort")
    _text(row["cohort"], "cohort label")
    if type(row["synthetic"]) is not bool or type(row["mature"]) is not bool:
        raise ValueError("synthetic and mature must be explicit booleans")
    if row["synthetic"] is not (mode == "synthetic"):
        raise ValueError("synthetic flag does not match the declared data mode")
    if not isinstance(row["currency"], str) or not re.fullmatch(r"[A-Z]{3}", row["currency"]):
        raise ValueError("currency must be three uppercase letters")
    window = row["window"]
    if not isinstance(window, str) or len(window.split("/")) != 2:
        raise ValueError("window must use YYYY-MM-DD/YYYY-MM-DD")
    start, end = map(_date, window.split("/"))
    observed = _date(row["outcome_as_of"])
    if start > end or observed < end:
        raise ValueError("cohort window must be ordered and end no later than observation")
    _object(row["counts"], STAGES, "counts")
    previous = None
    for stage in STAGES:
        count = row["counts"][stage]
        if type(count) is not int or count < 0 or count > MAX_SAFE_INTEGER:
            raise ValueError("stage counts must be nonnegative safe integers")
        if previous is not None and count > previous:
            raise ValueError("stage counts must be nested unique-person populations")
        previous = count
    for field in MONEY:
        value = row[field]
        if type(value) not in (int, float):
            raise ValueError("money must be a finite nonnegative JSON number: " + field)
        try:
            finite = math.isfinite(value)
        except OverflowError:
            finite = False
        if not finite:
            raise ValueError("money must be finite: " + field)
        amount = Decimal(str(value))
        if amount < 0 or amount > MAX_MONEY or amount != amount.quantize(Decimal("0.01")):
            raise ValueError("money must be 0..1e12 with at most two decimal places: " + field)


def _planning(items, fields, label):
    if not isinstance(items, list):
        raise ValueError(label + " must be an array")
    if len(items) > MAX_COLLECTION:
        raise ValueError(label + " must contain at most 1000 entries")
    seen = set()
    for item in items:
        _object(item, fields, label + " entry")
        for key in fields - {"guardrails"}:
            _text(item[key], label + "." + key)
        if item["id"] in seen:
            raise ValueError("duplicate " + label + " id")
        seen.add(item["id"])
        if "guardrails" in fields:
            if not isinstance(item["guardrails"], list):
                raise ValueError("guardrails must be an array of strings")
            if len(item["guardrails"]) > MAX_COLLECTION:
                raise ValueError("guardrails must contain at most 1000 entries")
            for text in item["guardrails"]:
                _text(text, "guardrail")


def validate_workspace(workspace):
    _object(workspace, WORKSPACE_FIELDS, "workspace")
    if workspace["schema_version"] != "1.0":
        raise ValueError("unsupported workspace schema_version")
    _text(workspace["name"], "name")
    _text(workspace["description"], "description")
    mode = workspace["data_mode"]
    if mode not in ("synthetic", "approved_aggregate"):
        raise ValueError("data_mode must be synthetic or approved_aggregate")
    provenance = workspace["provenance"]
    _object(provenance, PROVENANCE_FIELDS, "provenance")
    for field in ("source", "timezone", "cohort_definition"):
        _text(provenance[field], "provenance." + field)
    _timestamp(provenance["extracted_at"])
    approval = provenance["approval_reference"]
    if approval is not None:
        _text(approval, "approval_reference")
    if mode == "approved_aggregate" and approval is None:
        raise ValueError("approved_aggregate requires an approval_reference")
    mappings = provenance["mappings"]
    if not isinstance(mappings, list) or not mappings:
        raise ValueError("mappings must be a nonempty array")
    if len(mappings) > MAX_COLLECTION:
        raise ValueError("mappings must contain at most 1000 entries")
    targets = set()
    for mapping in mappings:
        _object(mapping, {"target", "source", "transform"}, "mapping")
        for field in ("target", "source", "transform"):
            _text(mapping[field], "mapping." + field)
        if mapping["target"] in targets:
            raise ValueError("duplicate mapping target")
        targets.add(mapping["target"])
    if targets != TARGETS:
        raise ValueError("mappings must cover exactly all canonical cohort fields")
    rows = workspace["cohorts"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("cohorts must be a nonempty array")
    if len(rows) > MAX_COHORTS:
        raise ValueError("cohorts must contain at most 200 entries")
    identities = set()
    for index, row in enumerate(rows):
        try:
            validate_cohort(row, mode)
            identity = (row["cohort"], row["window"])
            if identity in identities:
                raise ValueError("duplicate cohort and window")
            identities.add(identity)
        except ValueError as exc:
            raise ValueError(f"cohort[{index}]: {exc}") from None
    _planning(workspace["experiments"], EXPERIMENT_FIELDS, "experiments")
    _planning(workspace["initiatives"], INITIATIVE_FIELDS, "initiatives")
    serialize_workspace(workspace)
    return workspace


def serialize_workspace(workspace):
    """Return the exact UTF-8 JSON text emitted by the CLI, within import capacity."""
    output = json.dumps(workspace, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    try:
        payload = output.encode("utf-8")
    except UnicodeEncodeError:
        raise ValueError("workspace strings must be valid UTF-8") from None
    if len(payload) > MAX_WORKSPACE_BYTES:
        raise ValueError("serialized workspace must be at most 2000000 UTF-8 bytes")
    return output


def _lookup(row, path):
    _text(path, "source field path")
    if any(not part for part in path.split(".")):
        raise ValueError("source paths cannot contain empty segments")
    current = row
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise ValueError("a mapped source field is missing")
        current = current[part]
    return current


def build_workspace(rows, profile):
    required = {"name", "description", "data_mode", "provenance", "field_map"}
    optional = {"experiments", "initiatives"}
    if not isinstance(profile, dict) or not required <= set(profile) or set(profile) - required - optional:
        raise ValueError("profile must contain the documented metadata and field_map")
    _object(profile["provenance"], PROVENANCE_FIELDS - {"mappings"}, "profile provenance")
    mapping = profile["field_map"]
    _object(mapping, TARGETS, "field_map")
    if not isinstance(rows, list) or not rows:
        raise ValueError("source must be a nonempty JSON array of aggregate cohort objects")
    if len(rows) > MAX_COHORTS:
        raise ValueError("source must contain at most 200 aggregate cohorts")
    result_rows = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"source[{index}] must be an aggregate object")
        canonical = {"counts": {}}
        try:
            for target, source in mapping.items():
                value = _lookup(row, source)
                if target.startswith("counts."):
                    canonical["counts"][target.split(".")[1]] = value
                else:
                    canonical[target] = value
        except ValueError as exc:
            raise ValueError(f"source[{index}]: {exc}") from None
        result_rows.append(canonical)
    workspace = {
        "schema_version": "1.0", "name": profile["name"], "description": profile["description"],
        "data_mode": profile["data_mode"],
        "provenance": {**profile["provenance"], "mappings": [
            {"target": target, "source": mapping[target], "transform": "copy without coercion"}
            for target in sorted(mapping)
        ]},
        "cohorts": result_rows, "experiments": profile.get("experiments", []),
        "initiatives": profile.get("initiatives", []),
    }
    return validate_workspace(workspace)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def load_json(path):
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream, object_pairs_hook=_unique_object)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="authorized aggregate JSON array")
    parser.add_argument("--profile", type=Path, required=True, help="explicit mapping and provenance JSON")
    parser.add_argument("--output", type=Path, help="write workspace atomically instead of stdout")
    args = parser.parse_args(argv)
    try:
        if args.output and args.output.resolve() in (args.input.resolve(), args.profile.resolve()):
            raise ValueError("output must differ from input and profile")
        workspace = build_workspace(load_json(args.input), load_json(args.profile))
        output = serialize_workspace(workspace)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            temporary = None
            try:
                with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", dir=args.output.parent,
                                                 delete=False) as stream:
                    temporary = Path(stream.name)
                    stream.write(output)
                temporary.replace(args.output)
            finally:
                if temporary and temporary.exists():
                    temporary.unlink()
        else:
            print(output, end="")
    except (ValueError, OSError, UnicodeError) as exc:
        print("Invalid workspace input: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
