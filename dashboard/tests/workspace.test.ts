import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import {
  cents,
  parseWorkspace,
  metrics,
  validateWorkspace,
} from "../lib/workspace";
const root = fileURLToPath(new URL("../../", import.meta.url));
const fixture = () =>
  JSON.parse(
    readFileSync(
      new URL("../../examples/dashboard/workspace.json", import.meta.url),
      "utf8",
    ),
  );
test("demo is valid and browser metrics match Python analyzer per cohort", () => {
  const workspace = validateWorkspace(fixture());
  const python = spawnSync(
    "python3",
    ["scripts/analyze.py", "examples/lending/cohorts.json"],
    { cwd: root, encoding: "utf8" },
  );
  assert.equal(python.status, 0, python.stderr);
  const expected = JSON.parse(python.stdout);
  for (const [index, c] of workspace.cohorts.entries()) {
    const actual = metrics(c);
    assert.equal(actual.contribution, expected[index].contribution);
    assert.equal(actual.funded_cac, expected[index].funded_cac);
    for (const step of actual.steps)
      assert.equal(
        step.conversion,
        expected[index].rates[step.from + "->" + step.to],
      );
    assert.deepEqual(
      actual.byCount,
      expected[index].investigation_candidates.by_not_progressed,
    );
    assert.deepEqual(
      actual.byRate,
      expected[index].investigation_candidates.by_lowest_conversion,
    );
  }
});
test("count and rate leaders remain separate in the cheap channel", () => {
  const result = metrics(validateWorkspace(fixture()).cohorts[1]);
  assert.equal(result.countLeaders[0].from, "acquired");
  assert.equal(result.rateLeaders[0].from, "applied");
  assert.equal(result.rateLeaders[0].conversion, 1800 / 3500);
});
test("integer cents preserve fractional reconciliation", () => {
  const workspace = validateWorkspace(fixture()),
    c = workspace.cohorts[0];
  c.revenue = 0.3;
  c.acquisition_cost = 0.1;
  c.credit_loss = 0.2;
  c.funding_cost = 0;
  c.servicing_cost = 0;
  c.incentives = 0;
  assert.equal(metrics(c).contribution, 0);
  assert.equal(cents(0.29), 29);
});
test("zero denominators, missing leaders and immature economics remain unknown", () => {
  const workspace = fixture();
  for (const key of Object.keys(workspace.cohorts[0].counts))
    workspace.cohorts[0].counts[key] = 0;
  workspace.cohorts[0].mature = false;
  const result = metrics(validateWorkspace(workspace).cohorts[0]);
  assert.equal(result.funded_cac, null);
  assert.equal(result.contribution, null);
  assert.equal(result.countLeaders.length, 0);
  assert.equal(result.rateLeaders.length, 0);
});
test("malformed imports are rejected, not defaulted", () => {
  const mutations = [
    (w: any) => delete w.cohorts[0].credit_loss,
    (w: any) => (w.cohorts[0].counts.registered = 99999),
    (w: any) => (w.cohorts[0].mature = "true"),
    (w: any) => (w.cohorts[0].window = "2026-02-30/2026-03-01"),
    (w: any) => (w.cohorts[0].revenue = 1e13),
    (w: any) => (w.cohorts[0].revenue = 0.001),
    (w: any) => (w.provenance.extracted_at = "yesterday"),
    (w: any) => w.cohorts.push(w.cohorts[0]),
    (w: any) => (w.extra = "invented"),
  ];
  for (const mutate of mutations) {
    const w = fixture();
    mutate(w);
    assert.throws(() => validateWorkspace(w));
  }
});
test("approved aggregates retain false flags and require approval provenance", () => {
  const w = fixture();
  w.data_mode = "approved_aggregate";
  w.cohorts.forEach((c: any) => (c.synthetic = false));
  assert.throws(() => validateWorkspace(w));
  w.provenance.approval_reference = "synthetic-approval-reference-for-test";
  assert.equal(validateWorkspace(w).cohorts[0].synthetic, false);
  w.cohorts[0].synthetic = true;
  assert.throws(() => validateWorkspace(w));
});
test("cohort currencies stay separate; no implicit portfolio total is created", () => {
  const w = fixture();
  w.cohorts[1].currency = "EUR";
  const parsed = validateWorkspace(w);
  assert.equal(parsed.cohorts[0].currency, "USD");
  assert.equal(parsed.cohorts[1].currency, "EUR");
  assert.equal(metrics(parsed.cohorts[1]).contribution, -1000);
});

test("field provenance cannot be empty, duplicated or incomplete", () => {
  for (const change of [
    (w: any) => (w.provenance.mappings = []),
    (w: any) => w.provenance.mappings.push(w.provenance.mappings[0]),
    (w: any) => w.provenance.mappings.pop(),
  ]) {
    const w = fixture();
    change(w);
    assert.throws(() => validateWorkspace(w));
  }
});

test("paste capacity is measured in UTF-8 bytes, not characters", () => {
  assert.throws(() => parseWorkspace("界".repeat(700000)), /2 MB/);
  assert.equal(parseWorkspace(JSON.stringify(fixture())).cohorts.length, 2);
});
test("timestamp clock values cannot silently normalize into another day", () => {
  for (const stamp of [
    "2026-11-03T24:00:00Z",
    "2026-11-03T12:60:00Z",
    "2026-11-03T12:00:60Z",
    "2026-11-03T12:00:00+24:00",
  ]) {
    const w = fixture();
    w.provenance.extracted_at = stamp;
    assert.throws(() => validateWorkspace(w));
  }
});

test("strict JSON import rejects duplicate fields, comments and trailing commas", () => {
  const payload = JSON.stringify(fixture());
  assert.throws(
    () =>
      parseWorkspace(
        payload.replace(
          '"data_mode":"synthetic"',
          '"data_mode":"approved_aggregate","data_mode":"synthetic"',
        ),
      ),
    /Duplicate JSON/,
  );
  assert.throws(
    () =>
      parseWorkspace(
        payload.replace(
          '"registered":6000',
          '"registered":1,"registered":6000',
        ),
      ),
    /Duplicate JSON/,
  );
  assert.throws(() => parseWorkspace("/* comment */" + payload), /strict JSON/);
  assert.throws(
    () => parseWorkspace(payload.slice(0, -1) + ",}"),
    /strict JSON/,
  );
});
test("individually valid plan fields cannot create an oversized workspace", () => {
  const w = fixture();
  w.experiments = Array.from({ length: 900 }, (_, i) => ({
    ...w.experiments[0],
    id: "exp-" + i,
    title: "界".repeat(1000),
  }));
  assert.throws(() => validateWorkspace(w), /2 MB/);
});
