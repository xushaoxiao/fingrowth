"""Calculate the registration-to-credit funnel from a confirmed aggregate intake."""
import argparse
from datetime import datetime
from fractions import Fraction
import json
from pathlib import Path
import re
import sys
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

if __package__:
    from .analyze import _iso_date, _text, _unique_object
else:
    from analyze import _iso_date, _text, _unique_object

STAGES = {
    "registered": "注册",
    "profile_completed": "填资完成",
    "kyc_passed": "KYC 通过",
    "bank_details_completed": "银行资料完成",
    "credit_approved": "授信通过",
}
CHECKS = (
    "same_cohort", "unique_people_deduplicated", "ordered_nested_path",
    "equal_followup_or_censoring_handled", "same_journey_linkage",
)
UNIT = "unique first-registered person"


def fields(value, names, label):
    if not isinstance(value, dict) or value.keys() != set(names.split()):
        raise ValueError(f"{label} must contain exactly these fields: {names}")
    return value


def require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonempty text")
    value.encode("utf-8")


def exact_conversion(step):
    return Fraction(step["converted"], step["population"])


def analyze_intake(intake):
    fields(intake, "document_type version status provenance cohort stages quality_checks interpretation privacy_note",
           "intake")
    if intake["document_type"] != "fingrowth.registration-credit-intake" or intake["version"] != "0.1":
        raise ValueError("unsupported intake type or version")
    if intake["status"] != "ready_for_analysis":
        raise ValueError("intake status must be ready_for_analysis after review")
    fields(intake["interpretation"], "bottleneck root_cause experiment rates_computed", "interpretation")
    require_text(intake["privacy_note"], "privacy_note")

    provenance = fields(intake["provenance"], "data_kind source authorization_reference extracted_at", "provenance")
    kind = provenance["data_kind"]
    if kind not in ("synthetic", "approved_aggregate"):
        raise ValueError("data_kind must be synthetic or approved_aggregate")
    require_text(provenance["source"], "provenance.source")
    if kind == "approved_aggregate" or provenance["authorization_reference"] is not None:
        require_text(provenance["authorization_reference"], "provenance.authorization_reference")

    cohort = fields(intake["cohort"],
                    "product market timezone registration_start registration_end observation_cutoff "
                    "completion_window_days unit definition_confirmed journey_selection", "cohort")
    if cohort["unit"] != UNIT or cohort["definition_confirmed"] is not True:
        raise ValueError("confirm the unique first-registered-person cohort definition")
    for name in ("product", "market", "journey_selection", "timezone"):
        require_text(cohort[name], f"cohort.{name}")
    try:
        timezone = ZoneInfo(cohort["timezone"])
    except (ValueError, ZoneInfoNotFoundError):
        raise ValueError("cohort.timezone must be an available IANA time zone") from None
    start, end, cutoff = (_iso_date(cohort[name]) for name in
                          ("registration_start", "registration_end", "observation_cutoff"))
    days = cohort["completion_window_days"]
    if type(days) is not int or days <= 0 or start > end or (cutoff - end).days < days:
        raise ValueError("registration dates must be ordered and the full fixed follow-up window must have elapsed")
    extracted_at = provenance["extracted_at"]
    if not isinstance(extracted_at, str) or not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?"
            r"(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])", extracted_at):
        raise ValueError("provenance.extracted_at must be an ISO timestamp with an explicit UTC offset")
    extraction = datetime.fromisoformat(extracted_at.replace("Z", "+00:00"))
    if extraction.astimezone(timezone).date() <= cutoff:
        raise ValueError("extraction must be after the end of the local observation cutoff date")

    checks = fields(intake["quality_checks"], " ".join(CHECKS), "quality_checks")
    for name in CHECKS:
        if checks[name] is not True:
            raise ValueError(f"quality_checks.{name} must be confirmed")

    stages = intake["stages"]
    if not isinstance(stages, list) or len(stages) != len(STAGES):
        raise ValueError("stages must contain the five documented entries in order")
    counts = {}
    previous = None
    for expected, stage in zip(STAGES, stages):
        fields(stage, "id proposed_definition definition_confirmed source_event_or_rule unique_people", expected)
        if stage["id"] != expected or stage["definition_confirmed"] is not True:
            raise ValueError(f"expected confirmed stage {expected}")
        for name in ("proposed_definition", "source_event_or_rule"):
            require_text(stage[name], f"{expected}.{name}")
        count = stage["unique_people"]
        if type(count) is not int or count < 0 or (previous is not None and count > previous):
            raise ValueError(f"{expected}.unique_people must be a nonnegative nested integer count")
        counts[expected] = count
        previous = count

    steps = []
    for source, target in zip(STAGES, tuple(STAGES)[1:]):
        population, progressed = counts[source], counts[target]
        steps.append({
            "from": source, "to": target, "population": population, "converted": progressed,
            "not_progressed": population - progressed,
            "conversion": progressed / population if population else None,
        })
    registered = counts["registered"]
    return {
        "data_kind": kind,
        "cohort": {name: cohort[name] for name in (
            "product", "market", "timezone", "registration_start", "registration_end",
            "observation_cutoff", "completion_window_days", "unit")},
        "counts": counts,
        "steps": steps,
        "cumulative_conversion": {
            stage: counts[stage] / registered if registered else None for stage in tuple(STAGES)[1:]
        },
        "investigation_candidates": {
            "by_not_progressed": sorted(
                (step for step in steps if step["not_progressed"]), key=lambda step: -step["not_progressed"]),
            "by_lowest_conversion": sorted(
                (step for step in steps if step["population"]),
                key=exact_conversion),
        },
    }


def percent(rate):
    return "未知" if rate is None else f"{rate:.2%}"


def render_markdown(result):
    cohort = result["cohort"]
    lines = [
        "# 注册到授信漏斗", "",
        f"数据声明：{result['data_kind']}。产品 {_text(cohort['product'])} · 市场 {_text(cohort['market'])}。",
        f"注册窗口 {cohort['registration_start']} 至 {cohort['registration_end']}，"
        f"观察截止 {cohort['observation_cutoff']}（{_text(cohort['timezone'])}），"
        f"固定随访 {cohort['completion_window_days']} 天。", "",
        "| 阶段 | 上一步人数 | 继续人数 | 未继续人数 | 相邻转化率 | 相对注册累计转化率 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for step in result["steps"]:
        source, target = STAGES[step["from"]], STAGES[step["to"]]
        cumulative = result["cumulative_conversion"][step["to"]]
        lines.append(f"| {source} → {target} | {step['population']} | {step['converted']} | "
                     f"{step['not_progressed']} | {percent(step['conversion'])} | {percent(cumulative)} |")
    lines.extend(["", "## 调查优先级", ""])
    candidates = result["investigation_candidates"]
    for key, label, score in (
        ("by_not_progressed", "未继续人数最多", lambda step: step["not_progressed"]),
        ("by_lowest_conversion", "相邻转化率最低", exact_conversion),
    ):
        ranked = candidates[key]
        leaders = [step for step in ranked if score(step) == score(ranked[0])]
        names = "、".join(STAGES[step["from"]] + " → " + STAGES[step["to"]] for step in leaders)
        lines.append(f"- {label}：{names or '无可报告结果'}")
    lines.extend(["", "排名用于确定调查顺序。授权、旅程关联和随访口径由数据负责人确认。"
                  "涉及授信的差距需要进一步区分未提交、处理中、技术失败和政策拒绝。"])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="confirmed registration-credit intake JSON")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        with args.input.open(encoding="utf-8") as stream:
            result = analyze_intake(json.load(stream, object_pairs_hook=_unique_object))
        output = json.dumps(result, indent=2, ensure_ascii=False) if args.format == "json" else render_markdown(result)
    except (ValueError, OSError, OverflowError) as exc:
        print(f"Invalid intake: {exc}", file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
