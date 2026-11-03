import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("power_plan", ROOT / "scripts/plan_power.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class PowerPlanTest(unittest.TestCase):
    def test_independent_statsmodels_reference_and_integer_minimum(self):
        references = json.loads((ROOT / "tests/fixtures/power-reference.json").read_text())
        for case in references["cases"]:
            args = {key: case[key] for key in ("baseline", "mde_absolute", "alpha", "target_power")}
            with self.subTest(args=args):
                sample = m.plan_power(**args)["sample"]
                self.assertEqual(sample["per_arm"], case["per_arm"])
                self.assertEqual(sample["total"], 2 * case["per_arm"])
                self.assertAlmostEqual(sample["approximate_power"], case["approximate_power"], places=12)
                self.assertAlmostEqual(sample["approximate_power_one_fewer_per_arm"],
                                       case["approximate_power_one_fewer_per_arm"], places=12)
                self.assertGreaterEqual(sample["approximate_power"], case["target_power"])
                self.assertLess(sample["approximate_power_one_fewer_per_arm"], case["target_power"])

    def test_stricter_targets_require_more_people(self):
        n = lambda **kwargs: m.plan_power(0.6, **kwargs)["sample"]["per_arm"]
        base = n(mde_absolute=0.03)
        self.assertGreater(n(mde_absolute=0.02), base)
        self.assertGreater(n(mde_absolute=0.03, target_power=0.9), base)
        self.assertGreater(n(mde_absolute=0.03, alpha=0.01), base)

    def test_timing_separates_recruitment_primary_followup_and_risk(self):
        plan = m.plan_power(0.6, 0.03, eligible_per_day=400, primary_followup_days=7)
        timing = plan["timing"]
        self.assertEqual(timing["recruitment_days_at_assumed_rate"], 21)
        self.assertEqual(timing["earliest_primary_readout_day_after_start"], 28)
        self.assertIsNone(timing["delayed_risk_review_day"])
        self.assertEqual(plan["decision"]["launch_readiness"], "not assessed")
        self.assertEqual(plan["decision"]["risk_thresholds_and_approvals"], "unknown")

    def test_missing_timing_remains_unknown(self):
        timing = m.plan_power(0.6, 0.03)["timing"]
        self.assertIsNone(timing["recruitment_days_at_assumed_rate"])
        self.assertIsNone(timing["earliest_primary_readout_day_after_start"])
        self.assertIsNone(m.plan_power(0.6, 0.03, eligible_per_day=400)["timing"]
                          ["earliest_primary_readout_day_after_start"])
        self.assertIsNone(m.plan_power(0.6, 0.03, primary_followup_days=7)["timing"]
                          ["earliest_primary_readout_day_after_start"])
        self.assertEqual(m.plan_power(0.6, 0.03, eligible_per_day=400, primary_followup_days=0)
                         ["timing"]["earliest_primary_readout_day_after_start"], 21)

    def test_invalid_values_rejected_without_coercion(self):
        base = dict(baseline=0.6, mde_absolute=0.03)
        bad = {
            "baseline": [0, 1, -0.1, True, "0.6", float("nan"), float("inf"), 10**400],
            "mde_absolute": [0, -0.03, 0.4, 3, True, "0.03", 1e-20, float("nan")],
            "alpha": [0, 0.5, 1, -0.05, True, float("inf"), 5e-324],
            "target_power": [0.5, 1, -1, True, float("nan")],
            "eligible_per_day": [0, -1, True, "400", float("inf"), 5e-324],
            "primary_followup_days": [-1, 1.5, True, "7", 10**400],
        }
        for key, values in bad.items():
            for value in values:
                with self.subTest(key=key, value_type=type(value).__name__):
                    args = {**base, key: value}
                    with self.assertRaises(ValueError):
                        m.plan_power(**args)

    def test_normal_scope_gate_rejects_sparse_power_derived_design(self):
        with self.assertRaisesRegex(ValueError, "normal approximation guard failed"):
            m.plan_power(0.001, 0.499)

    def test_extremely_small_mde_fails_bounded_search(self):
        with self.assertRaisesRegex(ValueError, "supported maximum"):
            m.plan_power(0.5, 1e-8)

    def test_report_is_deterministic_and_inputs_are_not_mutated(self):
        args = dict(baseline=0.6, mde_absolute=0.03, eligible_per_day=400, primary_followup_days=7)
        original = copy.deepcopy(args)
        plan = m.plan_power(**args)
        self.assertEqual(args, original)
        self.assertEqual(m.render_markdown(plan), m.render_markdown(m.plan_power(**args)))
        json.dumps(plan, allow_nan=False)


class PowerCommandTest(unittest.TestCase):
    ARGS = ["--baseline", "0.6", "--mde-absolute", "0.03", "--alpha", "0.05", "--power", "0.8",
            "--eligible-per-day", "400", "--primary-followup-days", "7"]

    def test_cli_matches_api_and_markdown(self):
        for kind in ("json", "markdown"):
            result = subprocess.run([sys.executable, str(ROOT / "scripts/plan_power.py"),
                                     *self.ARGS, "--format", kind], capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            plan = m.plan_power(0.6, 0.03, eligible_per_day=400, primary_followup_days=7)
            if kind == "json":
                self.assertEqual(json.loads(result.stdout), plan)
            else:
                self.assertEqual(result.stdout, m.render_markdown(plan))

    def test_copied_skill_runs_in_isolated_python_without_repository(self):
        with tempfile.TemporaryDirectory(prefix="fingrowth power skill ") as directory:
            skill = Path(directory) / "growth-experiment-design"
            shutil.copytree(ROOT / "skills/growth-experiment-design", skill,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            result = subprocess.run([sys.executable, "-I", str(skill / "scripts/plan_power.py"), *self.ARGS],
                                    cwd=directory, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout),
                             m.plan_power(0.6, 0.03, eligible_per_day=400, primary_followup_days=7))

    def test_invalid_cli_emits_no_partial_report_or_traceback(self):
        cases = [
            ["--baseline", "nan", "--mde-absolute", "0.03"],
            ["--baseline", "0.6", "--mde-absolute", "0.4"],
            ["--baseline", "0.6", "--mde-absolute", "0.03", "--primary-followup-days", "1.5"],
            ["--baseline", "0.6"],
        ]
        for args in cases:
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, str(ROOT / "scripts/plan_power.py"), *args],
                                        capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
