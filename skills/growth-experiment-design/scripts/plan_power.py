"""Plan one fixed-horizon, equal-allocation binary experiment; no dependencies."""
import argparse
import json
import math
from statistics import NormalDist
import sys

MAX_PER_ARM = 1_000_000_000
MIN_EXPECTED_CELL = 10
METHOD_URL = "https://www.statsmodels.org/v0.14.6/generated/statsmodels.stats.proportion.power_proportions_2indep.html"


def _finite_number(value, name):
    if type(value) not in (int, float):
        raise ValueError(name + " must be a finite number")
    try:
        value = float(value)
    except (OverflowError, ValueError):
        raise ValueError(name + " must be a finite number") from None
    if not math.isfinite(value):
        raise ValueError(name + " must be a finite number")
    return value


def _power(n, delta, critical, sd_alt):
    """Both rejection tails under the normal alternative, not exact binomial power."""
    shift = delta * math.sqrt(n)
    upper = 0.5 * math.erfc((critical - shift) / (sd_alt * math.sqrt(2)))
    lower = 0.5 * math.erfc((critical + shift) / (sd_alt * math.sqrt(2)))
    return min(1.0, upper + lower)


def plan_power(baseline, mde_absolute, alpha=0.05, target_power=0.8,
               eligible_per_day=None, primary_followup_days=None):
    """Return an approximate sample-size plan, preserving unassessed risk gates.

    baseline and MDE are fractions, not percentages. Only positive improvements
    are supported; the test still allocates alpha to both rejection tails.
    """
    baseline = _finite_number(baseline, "baseline")
    mde_absolute = _finite_number(mde_absolute, "mde_absolute")
    alpha = _finite_number(alpha, "alpha")
    target_power = _finite_number(target_power, "target_power")
    if not 0 < baseline < 1:
        raise ValueError("baseline must be between 0 and 1, exclusive")
    treatment = baseline + mde_absolute
    if mde_absolute <= 0 or not baseline < treatment < 1:
        raise ValueError("positive absolute MDE must give baseline < treatment rate < 1")
    if not 0 < alpha < 0.5:
        raise ValueError("alpha must be between 0 and 0.5, exclusive")
    if not 0.5 < target_power < 1:
        raise ValueError("target_power must be between 0.5 and 1, exclusive")
    if eligible_per_day is not None:
        eligible_per_day = _finite_number(eligible_per_day, "eligible_per_day")
        if eligible_per_day <= 0:
            raise ValueError("eligible_per_day must be positive total assignments across both arms")
    if primary_followup_days is not None:
        if type(primary_followup_days) is not int or primary_followup_days < 0:
            raise ValueError("primary_followup_days must be a nonnegative integer")
        _finite_number(primary_followup_days, "primary_followup_days")

    pooled = (baseline + treatment) / 2
    sd_null = math.sqrt(2 * pooled * (1 - pooled))
    sd_alt = math.sqrt(baseline * (1 - baseline) + treatment * (1 - treatment))
    # Use the lower-tail quantile to avoid rounding 1 - tiny alpha/2 to 1.
    if alpha / 2 == 0:
        raise ValueError("alpha is too small for supported floating-point precision")
    z_critical = -NormalDist().inv_cdf(alpha / 2)
    critical = z_critical * sd_null
    delta = treatment - baseline
    power_at = lambda n: _power(n, delta, critical, sd_alt)

    high = 1
    while high < MAX_PER_ARM and power_at(high) < target_power:
        high = min(2 * high, MAX_PER_ARM)
    if power_at(high) < target_power:
        raise ValueError("required sample exceeds supported maximum of 1000000000 per arm")
    low = 1
    while low < high:
        middle = (low + high) // 2
        if power_at(middle) >= target_power:
            high = middle
        else:
            low = middle + 1
    per_arm = low
    minimum_cell = per_arm * min(baseline, 1 - baseline, treatment, 1 - treatment)
    if minimum_cell < MIN_EXPECTED_CELL:
        raise ValueError("normal approximation guard failed: each expected success/failure cell "
                         "must be at least 10 at the power-derived sample; use a reviewed exact/simulation design")

    total = 2 * per_arm
    recruitment_days = None
    if eligible_per_day is not None:
        recruitment = total / eligible_per_day
        if not math.isfinite(recruitment):
            raise ValueError("eligible_per_day is too small for a finite recruitment duration")
        recruitment_days = math.ceil(recruitment)
    readout_day = (recruitment_days + primary_followup_days
                   if recruitment_days is not None and primary_followup_days is not None else None)
    return {
        "method": "two-independent-proportions-normal-z-pooled-null-unpooled-alternative",
        "method_reference": METHOD_URL,
        "design": {"allocation": "1:1", "alternative": "two-sided", "stopping": "fixed horizon",
                   "primary_outcomes": 1, "randomization_unit": "independent assigned eligible person"},
        "inputs": {"baseline": baseline, "mde_absolute": mde_absolute,
                   "treatment_rate_at_mde": treatment, "alpha": alpha, "target_power": target_power},
        "sample": {"per_arm": per_arm, "total": total, "approximate_power": power_at(per_arm),
                   "approximate_power_one_fewer_per_arm": power_at(per_arm - 1),
                   "minimum_expected_success_or_failure": minimum_cell},
        "calculation": {"pooled_rate": pooled, "z_critical": z_critical,
                        "sd_null_without_sqrt_n": sd_null, "sd_alternative_without_sqrt_n": sd_alt,
                        "search": "smallest integer n with both-tail approximate power >= target",
                        "power_formula": "SF((zcrit*sd_null-delta*sqrt(n))/sd_alt) + "
                                         "CDF((-zcrit*sd_null-delta*sqrt(n))/sd_alt)"},
        "timing": {"eligible_assignments_per_day_total": eligible_per_day,
                   "recruitment_days_at_assumed_rate": recruitment_days,
                   "primary_followup_days_after_last_assignment": primary_followup_days,
                   "earliest_primary_readout_day_after_start": readout_day,
                   "delayed_risk_review_day": None},
        "decision": {"launch_readiness": "not assessed", "risk_thresholds_and_approvals": "unknown",
                     "scale_up": "requires separately reviewed mature risk and economic outcomes"},
        "limits": [
            "Planning approximation, not exact binomial power or a guarantee of observed uplift.",
            "Power at the assumed MDE tests zero difference; it does not prove the true effect exceeds the MDE.",
            "Independent binary ITT outcomes, one primary metric, equal allocation, no interim peeking.",
            "No clustered/repeated units, sequential or multiple-outcome designs, or loss/amount-mean power.",
            "At least 10 expected successes and failures per arm is a conservative scope gate, not proof of accuracy.",
            "Traffic and follow-up are supplied assumptions; operational delays and missing outcomes can extend timing.",
            "Primary-metric power does not power fraud, complaints, credit loss or contribution guardrails.",
            "Missing approved numeric guardrails or owner approvals still block launch; immature risk blocks scale-up.",
        ],
    }


def render_markdown(plan):
    inputs, sample, timing = plan["inputs"], plan["sample"], plan["timing"]
    number = lambda value: "unknown" if value is None else str(value)
    return "\n".join([
        "# FinGrowth binary experiment power plan", "",
        "Planning estimate only. Launch readiness is not assessed; risk thresholds and approvals are unknown.", "",
        "Design: independent assigned eligible people, 1:1 allocation, two-sided, fixed horizon, one binary ITT primary metric.", "",
        f"Baseline: {inputs['baseline']:.6g}; absolute MDE: {inputs['mde_absolute']:.6g} "
        f"({100 * inputs['mde_absolute']:.6g} percentage points); treatment at MDE: {inputs['treatment_rate_at_mde']:.6g}.",
        f"Alpha: {inputs['alpha']:.6g}; target power: {inputs['target_power']:.6g}.", "",
        f"Required sample: **{sample['per_arm']:,} per arm; {sample['total']:,} total**.",
        f"Approximate power at n: {sample['approximate_power']:.9f}; "
        f"at n − 1 per arm: {sample['approximate_power_one_fewer_per_arm']:.9f}.",
        f"Smallest expected success/failure cell: {sample['minimum_expected_success_or_failure']:.6g} (scope gate: ≥ 10).", "",
        "## Timing assumptions", "",
        f"Eligible assignments/day across both arms: {number(timing['eligible_assignments_per_day_total'])}.",
        f"Recruitment days at assumed traffic: {number(timing['recruitment_days_at_assumed_rate'])}.",
        f"Primary follow-up days after the last assignment: {number(timing['primary_followup_days_after_last_assignment'])}.",
        f"Earliest primary readout day after start: {number(timing['earliest_primary_readout_day_after_start'])}.",
        "Delayed-risk review day: unknown; determine separately from loan schedules and observation maturity.", "",
        "## Explainable method", "",
        "Null variance uses the pooled probability; alternative variance uses the two separate probabilities. "
        "Integer bisection finds the smallest per-arm sample meeting the target under the two-tail normal approximation.",
        "`" + plan["calculation"]["power_formula"] + "`", "",
        "Method reference: " + plan["method_reference"], "",
        "## Limits and decision gates", "",
        *["- " + item for item in plan["limits"]], "",
    ])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=float, required=True, help="control probability as a fraction")
    parser.add_argument("--mde-absolute", type=float, required=True,
                        help="positive absolute change as a fraction, e.g. 0.03 for 3 percentage points")
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--power", type=float, default=0.8, dest="target_power")
    parser.add_argument("--eligible-per-day", type=float,
                        help="assumed total unique eligible assignments/day across both arms")
    parser.add_argument("--primary-followup-days", type=int,
                        help="outcome follow-up after the last assignment; excludes delayed-risk review")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        plan = plan_power(args.baseline, args.mde_absolute, args.alpha, args.target_power,
                          args.eligible_per_day, args.primary_followup_days)
    except ValueError as exc:
        print("Invalid input: " + str(exc), file=sys.stderr)
        return 2
    if args.format == "markdown":
        print(render_markdown(plan), end="")
    else:
        print(json.dumps(plan, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
