# Synthetic KYC experiment: plan power without claiming launch approval

Every number below is invented. It does not describe Shaoxiao's employer, actual traffic, an actual credit portfolio or observed uplift.

## Decision and population

Hypothesis: clearer document-upload guidance increases completion of KYC within seven days. Randomize consenting eligible new applicants once, before KYC, 1:1; persist assignment. The primary outcome is people completing KYC within seven days / all assigned eligible people (ITT). Underwriting, pricing and eligibility policies remain unchanged. A real deployment needs reviewed assignment, consent, logging, duplicate-event and missing-outcome handling.

Planning assumptions: baseline 0.60, positive absolute MDE 0.03 (three percentage points; target 0.63), two-sided alpha 0.05 and power 0.80. Assume 400 eligible assignments per day across both arms, and seven days to observe the last assigned person's primary outcome. These are inputs for the synthetic exercise, not a prediction or benchmark recommendation.

```sh
python3 scripts/plan_power.py --baseline 0.60 --mde-absolute 0.03 --alpha 0.05 --power 0.80 --eligible-per-day 400 --primary-followup-days 7 --format markdown
```

## Actual calculator output for this fixture

- Per arm: **4,129**; total: **8,258**.
- Approximate two-tail normal power: **0.800035179** at 4,129/arm; **0.799940156** at one fewer per arm (rounded as in the Markdown report).
- Recruitment: `ceil(8258 / 400) = 21` days at the assumed traffic.
- Earliest primary readout: `21 + 7 = 28` days after start, assuming complete outcomes and no operational delays.
- Delayed credit-risk review day: **unknown**. Seven-day KYC follow-up is not loan maturity.

The tool evaluates pooled-null / unpooled-alternative normal power and searches the smallest integer sample meeting the target. It is not exact binomial power. Power at an assumed three-point improvement tests the zero-difference null; it does not provide an 80% probability of proving that the true effect exceeds three points. A minimum-worthwhile-effect claim requires another reviewed hypothesis/design. Read the [method and applicability gates](../../skills/growth-experiment-design/references/power-planning.md) before applying it to another design.

## Decision gates remain unresolved

Status: **blocked before launch**. Numeric technical-failure, complaint/consent, fraud and mature-loss stop thresholds and named approvals have not been supplied. Their owners must also define denominators, exposure caps, monitoring horizons and rollback actions. Primary-metric sample size does not power those guardrails. Daily significance peeking is outside this fixed-horizon design.

Even if the primary outcome later improves, scaling still requires separately mature risk and economic outcomes, reconciled contribution, and risk/finance review. The calculation neither launches the experiment nor establishes business value.
