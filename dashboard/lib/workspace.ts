import {
  parseTree,
  type Node as JsonNode,
  type ParseError,
} from "jsonc-parser";
export const STAGES = [
  "acquired",
  "registered",
  "kyc",
  "applied",
  "approved",
  "accepted",
  "disbursed",
  "repaid",
  "repeat",
] as const;
export const COSTS = [
  "acquisition_cost",
  "credit_loss",
  "funding_cost",
  "servicing_cost",
  "incentives",
] as const;
export type Stage = (typeof STAGES)[number];
export type Cost = (typeof COSTS)[number];
export type Cohort = {
  cohort: string;
  window: string;
  outcome_as_of: string;
  currency: string;
  synthetic: boolean;
  mature: boolean;
  counts: Record<Stage, number>;
  revenue: number;
} & Record<Cost, number>;
export type Experiment = {
  id: string;
  title: string;
  status: string;
  owner: string;
  primary_metric: string;
  hypothesis: string;
  guardrails: string[];
  next_action: string;
};
export type Initiative = {
  id: string;
  title: string;
  owner: string;
  status: string;
  acceptance: string;
  dependency: string;
};
export type Workspace = {
  schema_version: "1.0";
  name: string;
  description: string;
  data_mode: "synthetic" | "approved_aggregate";
  provenance: {
    source: string;
    extracted_at: string;
    timezone: string;
    cohort_definition: string;
    approval_reference: string | null;
    mappings: { target: string; source: string; transform: string }[];
  };
  cohorts: Cohort[];
  experiments: Experiment[];
  initiatives: Initiative[];
};
export const LABELS: Record<Stage, string> = {
  acquired: "Acquired",
  registered: "Registered",
  kyc: "KYC completed",
  applied: "Applied",
  approved: "Approved",
  accepted: "Offer accepted",
  disbursed: "First funded",
  repaid: "Fully repaid",
  repeat: "Repeat borrower",
};
const fail = (message: string): never => {
  throw new Error(message);
};
function object(
  value: unknown,
  keys: string[],
  where: string,
): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value))
    return fail(`${where}: expected an object.`);
  const row = value as Record<string, unknown>;
  if (Object.keys(row).sort().join("|") !== [...keys].sort().join("|"))
    return fail(`${where}: fields do not match the workspace contract.`);
  return row;
}
function text(value: unknown, where: string, empty = false): string {
  if (
    typeof value !== "string" ||
    (!empty && !value.trim()) ||
    value.length > 10000
  )
    return fail(
      `${where}: expected ${empty ? "text" : "nonempty text"} (up to 10,000 characters).`,
    );
  return value;
}
function array(value: unknown, where: string, max = 1000): unknown[] {
  if (!Array.isArray(value) || value.length > max)
    return fail(`${where}: expected an array with at most ${max} entries.`);
  return value;
}
function isoDate(value: unknown, where: string): string {
  const result = text(value, where);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(result))
    return fail(`${where}: expected YYYY-MM-DD.`);
  const date = new Date(`${result}T00:00:00Z`);
  if (
    !Number.isFinite(date.getTime()) ||
    date.toISOString().slice(0, 10) !== result
  )
    return fail(`${where}: invalid calendar date.`);
  return result;
}
export function cents(value: unknown, where = "amount"): number {
  if (
    typeof value !== "number" ||
    !Number.isFinite(value) ||
    value < 0 ||
    value > 1e12 ||
    !/^\d+(\.\d{1,2})?$/.test(String(value))
  )
    return fail(
      `${where}: use a nonnegative amount up to 1 trillion with at most two decimals.`,
    );
  const [whole, decimal = ""] = String(value).split(".");
  return Number(whole) * 100 + Number(decimal.padEnd(2, "0"));
}
export function validateWorkspace(value: unknown): Workspace {
  const row = object(
    value,
    [
      "schema_version",
      "name",
      "description",
      "data_mode",
      "provenance",
      "cohorts",
      "experiments",
      "initiatives",
    ],
    "Workspace",
  );
  if (row.schema_version !== "1.0")
    fail("Unsupported workspace version; use 1.0.");
  text(row.name, "Workspace name");
  text(row.description, "Description");
  if (row.data_mode !== "synthetic" && row.data_mode !== "approved_aggregate")
    fail("Data mode must be synthetic or approved_aggregate.");
  const p = object(
    row.provenance,
    [
      "source",
      "extracted_at",
      "timezone",
      "cohort_definition",
      "approval_reference",
      "mappings",
    ],
    "Provenance",
  );
  for (const field of ["source", "timezone", "cohort_definition"])
    text(p[field], `Provenance ${field}`);
  const extracted = text(p.extracted_at, "Extraction date");
  if (
    !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$/.test(
      extracted,
    ) ||
    !Number.isFinite(Date.parse(extracted))
  )
    fail("Extraction date must be an ISO timestamp including timezone.");
  isoDate(extracted.slice(0, 10), "Extraction date");
  const clock = extracted.slice(11, 19).split(":").map(Number);
  const offset = /[+-](\d{2}):(\d{2})$/.exec(extracted);
  if (
    clock[0] > 23 ||
    clock[1] > 59 ||
    clock[2] > 59 ||
    (offset && (Number(offset[1]) > 23 || Number(offset[2]) > 59))
  )
    fail("Extraction date has an invalid clock or UTC offset.");
  if (p.approval_reference !== null)
    text(p.approval_reference, "Approval reference");
  if (row.data_mode === "approved_aggregate" && p.approval_reference === null)
    fail(
      "Approved aggregate data requires an approval reference. This is a declaration, not a privacy certification.",
    );
  const targets = new Set<string>();
  for (const [i, entry] of array(p.mappings, "Field mappings").entries()) {
    const map = object(
      entry,
      ["target", "source", "transform"],
      `Mapping ${i + 1}`,
    );
    for (const field of ["target", "source", "transform"])
      text(map[field], `Mapping ${i + 1} ${field}`);
    if (targets.has(map.target as string))
      fail("Mapping targets must be unique.");
    targets.add(map.target as string);
  }
  const requiredTargets = [
    "cohort",
    "window",
    "outcome_as_of",
    "currency",
    "synthetic",
    "mature",
    "revenue",
    ...COSTS,
    ...STAGES.map((s) => "counts." + s),
  ];
  if ([...targets].sort().join("|") !== requiredTargets.sort().join("|"))
    fail("Mappings must cover every canonical cohort field exactly once.");
  const cohorts = array(row.cohorts, "Cohorts", 200);
  if (!cohorts.length) fail("At least one cohort is required.");
  const identities = new Set<string>();
  for (const [i, value] of cohorts.entries()) {
    const c = object(
      value,
      [
        "cohort",
        "window",
        "outcome_as_of",
        "currency",
        "synthetic",
        "mature",
        "counts",
        "revenue",
        ...COSTS,
      ],
      `Cohort ${i + 1}`,
    );
    text(c.cohort, "Cohort name");
    if (typeof c.synthetic !== "boolean" || typeof c.mature !== "boolean")
      fail("Synthetic and maturity flags must be explicit booleans.");
    if (c.synthetic !== (row.data_mode === "synthetic"))
      fail("Cohort synthetic flags must match the declared data mode.");
    if (typeof c.currency !== "string" || !/^[A-Z]{3}$/.test(c.currency))
      fail("Currency must have three uppercase letters.");
    const dates = text(c.window, "Cohort window").split("/");
    if (dates.length !== 2) fail("Cohort window must use start/end dates.");
    const start = isoDate(dates[0], "Cohort start"),
      end = isoDate(dates[1], "Cohort end"),
      asof = isoDate(c.outcome_as_of, "Outcome date");
    if (start > end || asof < end)
      fail(
        "Cohort dates must be ordered and outcomes observed after cohort entry closes.",
      );
    const identity = JSON.stringify([c.cohort, c.window]);
    if (identities.has(identity)) fail("Duplicate cohort and window.");
    identities.add(identity);
    const counts = object(c.counts, [...STAGES], "Stage counts");
    let previous = Number.MAX_SAFE_INTEGER;
    for (const stage of STAGES) {
      const n = counts[stage];
      if (
        typeof n !== "number" ||
        !Number.isSafeInteger(n) ||
        n < 0 ||
        n > previous
      )
        fail("Stage counts must be nested nonnegative safe integers.");
      previous = n as number;
    }
    for (const field of ["revenue", ...COSTS]) cents(c[field], field);
  }
  const seenExperiments = new Set<string>(),
    seenInitiatives = new Set<string>();
  for (const [i, entry] of array(row.experiments, "Experiments").entries()) {
    const e = object(
      entry,
      [
        "id",
        "title",
        "status",
        "owner",
        "primary_metric",
        "hypothesis",
        "guardrails",
        "next_action",
      ],
      `Experiment ${i + 1}`,
    );
    for (const key of [
      "id",
      "title",
      "status",
      "owner",
      "primary_metric",
      "hypothesis",
      "next_action",
    ])
      text(e[key], `Experiment ${i + 1} ${key}`);
    if (seenExperiments.has(e.id as string))
      fail("Experiment IDs must be unique.");
    seenExperiments.add(e.id as string);
    for (const item of array(e.guardrails, "Guardrails"))
      text(item, "Guardrail");
  }
  for (const [i, entry] of array(row.initiatives, "Initiatives").entries()) {
    const item = object(
      entry,
      ["id", "title", "owner", "status", "acceptance", "dependency"],
      `Initiative ${i + 1}`,
    );
    for (const key of [
      "id",
      "title",
      "owner",
      "status",
      "acceptance",
      "dependency",
    ])
      text(item[key], `Initiative ${i + 1} ${key}`);
    if (seenInitiatives.has(item.id as string))
      fail("Initiative IDs must be unique.");
    seenInitiatives.add(item.id as string);
  }
  if (
    new TextEncoder().encode(JSON.stringify(row, null, 2) + "\n").byteLength >
    2_000_000
  )
    fail("Canonical workspace exceeds the 2 MB limit.");
  return row as unknown as Workspace;
}
export function metrics(cohort: Cohort) {
  const steps = STAGES.slice(0, -1).map((from, index) => {
    const to = STAGES[index + 1];
    return {
      from,
      to,
      population: cohort.counts[from],
      converted: cohort.counts[to],
      not_progressed: cohort.counts[from] - cohort.counts[to],
      conversion: cohort.counts[from]
        ? cohort.counts[to] / cohort.counts[from]
        : null,
    };
  });
  const journey = steps.slice(0, 6);
  const byCount = [...journey]
    .filter((s) => s.not_progressed > 0)
    .sort((a, b) => b.not_progressed - a.not_progressed);
  const byRate = [...journey]
    .filter((s) => s.conversion !== null)
    .sort((a, b) => a.conversion! - b.conversion!);
  const countLeaders = byCount.filter(
    (s) => s.not_progressed === byCount[0]?.not_progressed,
  );
  const rateLeaders = byRate.filter(
    (s) => s.conversion === byRate[0]?.conversion,
  );
  const costs = COSTS.map((key) => ({
    key,
    amount: cohort[key],
    cents: cents(cohort[key]),
  }));
  return {
    steps,
    journey,
    byCount,
    byRate,
    countLeaders,
    rateLeaders,
    costs,
    funded_cac: cohort.counts.disbursed
      ? cohort.acquisition_cost / cohort.counts.disbursed
      : null,
    contribution: cohort.mature
      ? (cents(cohort.revenue) -
          costs.reduce((sum, cost) => sum + cost.cents, 0)) /
        100
      : null,
  };
}

export function parseWorkspace(text: string): Workspace {
  if (new TextEncoder().encode(text).byteLength > 2_000_000)
    throw new Error("Workspace exceeds the 2 MB limit.");
  const errors: ParseError[] = [];
  const tree = parseTree(text, errors, {
    allowTrailingComma: false,
    disallowComments: true,
  });
  if (!tree || errors.length)
    fail("Workspace must be strict JSON without comments or trailing commas.");
  const pending: JsonNode[] = [tree!];
  while (pending.length) {
    const node = pending.pop()!;
    if (node.type === "object") {
      const keys = new Set<string>();
      for (const property of node.children ?? []) {
        const key = property.children?.[0]?.value;
        if (keys.has(key))
          fail(
            "Duplicate JSON field. Resolve the source conflict before import.",
          );
        keys.add(key);
      }
    }
    pending.push(...(node.children ?? []));
  }
  return validateWorkspace(JSON.parse(text));
}
