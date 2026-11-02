"""Aggregate-only, deterministic educational cohort analysis."""
import json, math, sys
STAGES = ('acquired','registered','kyc','applied','approved','accepted','disbursed','repaid','repeat')
COSTS = ('acquisition_cost','credit_loss','funding_cost','servicing_cost','incentives')
def analyze(row):
    if row.get('synthetic') is not True:
        raise ValueError('v0.1 accepts explicitly synthetic fixtures only')
    for field in ('cohort','window','outcome_as_of','currency'):
        if not isinstance(row.get(field),str) or not row[field]:
            raise ValueError('missing metadata: '+field)
    c = row['counts']
    previous = None
    for stage in STAGES:
        n = c[stage]
        if type(n) is not int or n < 0 or (previous is not None and n > previous):
            raise ValueError('counts must be nonnegative nested integer populations')
        previous = n
    for key in COSTS + ('revenue',):
        n = row[key]
        if type(n) not in (int,float) or not math.isfinite(n) or n < 0:
            raise ValueError('invalid monetary value: '+key)
    rates = {a+'->'+b: c[b]/c[a] if c[a] else None for a,b in zip(STAGES,STAGES[1:])}
    mature = row.get('mature') is True
    return dict(cohort=row['cohort'],currency=row['currency'],mature=mature,
        rates=rates, funded_cac=row['acquisition_cost']/c['disbursed'] if c['disbursed'] else None,
        contribution=row['revenue']-sum(row[k] for k in COSTS) if mature else None,
        explanation='contribution = revenue - acquisition - credit loss - funding - servicing - incentives; immature contribution is unknown')
if __name__ == '__main__':
    try:
        print(json.dumps([analyze(r) for r in json.load(open(sys.argv[1]))],indent=2,allow_nan=False))
    except (ValueError,KeyError,TypeError,IndexError) as exc:
        sys.exit('Invalid input: '+str(exc))
