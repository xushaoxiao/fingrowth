# Binary experiment power planning

Use this tool only for one independent binary intention-to-treat primary outcome, equal 1:1 assignment, a two-sided equality test and a predeclared fixed horizon. It estimates sample size; it does not analyze observed test results. Do not use it for clustered units, repeated people, multiple outcomes, unequal allocation, sequential stopping, noninferiority, or revenue/loss means. Those need another reviewed method.

## Inputs and command

```sh
python3 <skill-directory>/scripts/plan_power.py --baseline 0.60 --mde-absolute 0.03 --alpha 0.05 --power 0.80 --eligible-per-day 400 --primary-followup-days 7 --format markdown
```

In the repository, `python3 scripts/plan_power.py` delegates to the same bundled implementation. Omit `--format markdown` for JSON. All report content is emitted only after validation; exit 2 means unsupported or invalid inputs, not a partial usable plan.

Probabilities are fractions. Baseline is strictly between 0 and 1; MDE is a positive **absolute** fraction, and the target treatment probability must remain strictly below 1. `0.03` means three percentage points, not a 3% relative increase. Alpha is in `(0, 0.5)` and target power in `(0.5, 1)`; defaults are 0.05 and 0.8 and are shown in output. Decreases are outside this narrow planner even though the test has two rejection tails. The implementation rejects nonfinite/bool values and designs needing over 1,000,000,000 observations per arm.

Optional daily traffic means the assumed total unique eligible assignments across both arms, not visitors or successful KYC completions. Recruitment days are `ceil(total sample / eligible assignments per day)`. Optional primary follow-up is a nonnegative whole number of days **after the last assignment**. The earliest primary readout is their sum, only when both inputs are supplied. It assumes stable traffic and complete outcome collection; operational delays, missing outcomes or assignment imbalance require review. Delayed credit-risk maturity remains unknown and is not inferred from these days.

## Explainable calculation

Let `p0` be baseline, `p1 = p0 + delta`, and `pbar = (p0 + p1)/2`. For per-arm sample `n`:

```text
sd_null = sqrt(2 * pbar * (1 - pbar))
sd_alt  = sqrt(p0 * (1 - p0) + p1 * (1 - p1))
zcrit   = inverse_normal_cdf(1 - alpha/2)
power(n) = SF((zcrit*sd_null - delta*sqrt(n))/sd_alt)
         + CDF((-zcrit*sd_null - delta*sqrt(n))/sd_alt)
```

The pooled-null / unpooled-alternative variance model follows the official [Statsmodels two-independent-proportion power documentation](https://www.statsmodels.org/v0.14.6/generated/statsmodels.stats.proportion.power_proportions_2indep.html) and its [normal power method](https://www.statsmodels.org/v0.14.6/generated/statsmodels.stats.power.normal_power_het.html). Both rejection tails are evaluated with `erfc`; integer bisection returns the smallest `n` reaching the requested power under that approximation, and reports power at `n` and `n − 1`. This is not exact binomial power, a simulation or guaranteed finite-sample performance. No continuity correction is applied.

The tool additionally requires `n*p0`, `n*(1-p0)`, `n*p1` and `n*(1-p1)` all at least 10. This is a conservative product scope gate, not a guarantee that the normal approximation is accurate. If the power-derived sample fails it, the tool refuses the plan rather than silently inflating a sample or claiming exactness. Request an independently reviewed exact/simulation design.

Regression references in `tests/fixtures/power-reference.json` were independently generated with Statsmodels 0.14.6 and SciPy root solving, outside the product runtime. Product execution and tests do not require either dependency. Synthetic worked use: [KYC power case](../../../examples/experiments/KYC-POWER.md) in a repository checkout; the copied skill's command and method are standalone.

## Risk-adjusted decision boundary

The planned MDE is a decision assumption, not a forecast. Power here is the approximate probability of rejecting a **zero-difference null** when the true effect equals the assumed MDE. It is not the probability of proving that the true effect exceeds the MDE or another minimum worthwhile threshold. A decision requiring that stronger claim needs a separately reviewed hypothesis/design.

Primary KYC power does not establish sufficient fraud, complaint, consent, loss or contribution sensitivity. Retain their own approved numeric thresholds, observation horizons and owners. Missing thresholds or approvals block launch; immature loan outcomes block scale-up even if the primary result later succeeds. The command never changes source systems, launches an experiment or declares a design launch-ready.
