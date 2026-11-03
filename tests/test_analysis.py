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
spec = importlib.util.spec_from_file_location("analysis", ROOT / "scripts/analyze.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class AnalysisTest(unittest.TestCase):
    def setUp(self):
        self.rows = json.loads((ROOT / "examples/lending/cohorts.json").read_text())

    def test_economics(self):
        baseline, cheap = m.analyze_document(self.rows)
        self.assertEqual(baseline["contribution"], 4000)
        self.assertEqual(cheap["contribution"], -1000)
        self.assertEqual(baseline["funded_cac"], 10)
        self.assertAlmostEqual(cheap["funded_cac"], 50 / 7)
        self.assertLess(cheap["funded_cac"], baseline["funded_cac"])

    def test_rates_and_people_reconcile(self):
        for row in self.rows:
            result = m.analyze(row)
            for step in result["steps"]:
                self.assertEqual(step["population"], step["converted"] + step["not_progressed"])
                self.assertAlmostEqual(step["conversion"], step["converted"] / step["population"])
                self.assertEqual(result["rates"][step["from"] + "->" + step["to"]], step["conversion"])
            product = 1
            for step in result["steps"][:6]:
                product *= step["conversion"]
            self.assertAlmostEqual(product * row["counts"]["acquired"], row["counts"]["disbursed"])

    def test_rankings_answer_different_questions(self):
        candidates = m.analyze(self.rows[0])["investigation_candidates"]
        self.assertEqual(candidates["by_not_progressed"][0]["not_progressed"], 4000)
        self.assertEqual(candidates["by_not_progressed"][0]["from"], "acquired")
        self.assertEqual(candidates["by_lowest_conversion"][0]["from"], "applied")
        for ranked in candidates.values():
            self.assertFalse(any(s["to"] in ("repaid", "repeat") for s in ranked))

    def test_zero_denominator(self):
        row = self.rows[0]
        row["counts"] = {k: 0 for k in m.STAGES}
        result = m.analyze(row)
        self.assertIsNone(result["funded_cac"])
        self.assertTrue(all(rate is None for rate in result["rates"].values()))
        self.assertFalse(result["investigation_candidates"]["by_lowest_conversion"])
        self.assertIn("unknown", m.render_markdown([result]))

    def test_tied_candidates_are_not_presented_as_unique(self):
        row = self.rows[0]
        row["counts"] = dict(zip(m.STAGES, (128, 64, 32, 16, 8, 4, 2, 1, 0)))
        result = m.analyze(row)
        line = next(line for line in m.render_markdown([result]).splitlines()
                    if line.startswith("- Lowest observed conversion:"))
        self.assertIn("acquired → registered", line)
        self.assertIn("accepted → disbursed", line)
        self.assertNotIn("repaid", line)

    def test_immature(self):
        self.rows[0]["mature"] = False
        result = m.analyze(self.rows[0])
        self.assertIsNone(result["contribution"])
        self.assertIn("Immature cohort", " ".join(result["warnings"]))
        self.assertIn("contribution: unknown", m.render_markdown([result]))

    def test_maturity_must_be_explicit_boolean(self):
        for value in (None, "true", 1, 0):
            with self.subTest(value=value):
                self.rows[0]["mature"] = value
                with self.assertRaises(ValueError):
                    m.analyze(self.rows[0])
        del self.rows[0]["mature"]
        with self.assertRaises(ValueError):
            m.analyze(self.rows[0])

    def test_invalid_monetary_values(self):
        for field in m.COSTS + ("revenue",):
            for value in (float("nan"), float("inf"), -1, True, "12", None, 10**400):
                with self.subTest(field=field, value_type=type(value).__name__):
                    row = copy.deepcopy(self.rows[0])
                    row[field] = value
                    with self.assertRaises(ValueError):
                        m.analyze(row)

    def test_non_synthetic_rejected(self):
        for value in (False, "true", 1):
            self.rows[0]["synthetic"] = value
            with self.assertRaises(ValueError):
                m.analyze(self.rows[0])

    def test_invalid_count_types_and_order(self):
        for value in (-1, True, 1.5, "1400", None, 99999):
            with self.subTest(value=value):
                row = copy.deepcopy(self.rows[0])
                row["counts"]["disbursed"] = value
                with self.assertRaises(ValueError):
                    m.analyze(row)

    def test_missing_extra_and_wrong_shapes(self):
        for field in self.rows[0]:
            row = copy.deepcopy(self.rows[0])
            del row[field]
            with self.subTest(missing=field), self.assertRaises(ValueError):
                m.analyze(row)
        for value in (None, [], 1, "row", {**self.rows[0], "customer": "invented"},
                      {**self.rows[0], "counts": []},
                      {**self.rows[0], "counts": {**self.rows[0]["counts"], "other": 0}}):
            with self.subTest(shape=type(value).__name__), self.assertRaises(ValueError):
                m.analyze(value)

    def test_date_contract(self):
        for field, value in (
            ("window", "2026-02-30/2026-03-01"),
            ("window", "2026-02-01/2026-01-31"),
            ("window", "20260101/2026-01-31"),
            ("window", "January"), ("window", None),
            ("outcome_as_of", "2026-01-30"), ("outcome_as_of", "2026-13-01"),
            ("outcome_as_of", "20261031"),
        ):
            with self.subTest(field=field, value=value):
                row = copy.deepcopy(self.rows[0])
                row[field] = value
                with self.assertRaises(ValueError):
                    m.analyze(row)

    def test_label_and_currency_contract(self):
        for field, value in (("cohort", " "), ("cohort", None), ("currency", "usd"),
                             ("currency", "US"), ("currency", None)):
            row = copy.deepcopy(self.rows[0])
            row[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                m.analyze(row)

    def test_document_contract(self):
        for rows in (None, {}, [], "cohorts", [None], [self.rows[0], self.rows[0]]):
            with self.subTest(shape=type(rows).__name__), self.assertRaises(ValueError):
                m.analyze_document(rows)

    def test_cohorts_with_different_currencies_remain_separate(self):
        self.rows[1]["currency"] = "EUR"
        result = m.analyze_document(self.rows)
        self.assertEqual([r["currency"] for r in result], ["USD", "EUR"])
        self.assertEqual(len(result), 2)

    def test_markdown_preserves_evidence_and_escapes_labels(self):
        self.rows[0]["cohort"] = "invented|label\n<script>"
        report = m.render_markdown(m.analyze_document(self.rows))
        self.assertIn("invented&#124;label &lt;script&gt;", report)
        self.assertIn("| acquired → registered | 10000 | 6000 | 4000 | 60.00% |", report)
        self.assertIn("2026-10-31", report)
        self.assertIn("Funded CAC: 7.14; contribution: -1,000.00", report)
        self.assertIn("do not establish causes", report)


class CommandTest(unittest.TestCase):
    def run_command(self, *args, cwd=None):
        return subprocess.run([sys.executable, str(ROOT / "scripts/analyze.py"), *map(str, args)],
                              capture_output=True, text=True, cwd=cwd, timeout=15)

    def test_existing_json_command(self):
        result = self.run_command(ROOT / "examples/lending/cohorts.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["contribution"], 4000)
        self.assertEqual(result.stderr, "")

    def test_markdown_command(self):
        result = self.run_command(ROOT / "examples/lending/cohorts.json", "--format", "markdown")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# FinGrowth synthetic cohort report", result.stdout)

    def test_bad_inputs_have_no_partial_output_or_traceback(self):
        rows = json.loads((ROOT / "examples/lending/cohorts.json").read_text())
        rows[1]["counts"]["approved"] = 99999
        bad_documents = ("{", "{}", "null", "[]", "[1]", json.dumps(rows),
                         '[{"synthetic":true,"synthetic":false}]', b"\xff")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            for document in bad_documents:
                with self.subTest(document_type=type(document).__name__):
                    path.write_bytes(document if isinstance(document, bytes) else document.encode())
                    result = self.run_command(path)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertIn("Invalid input:", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_missing_file_or_argument(self):
        with tempfile.TemporaryDirectory() as directory:
            for args in ((), (Path(directory) / "absent.json",)):
                result = self.run_command(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("Traceback", result.stderr)

    def test_copied_skill_runs_without_repository_or_current_directory(self):
        with tempfile.TemporaryDirectory(prefix="fingrowth skill ") as directory:
            install = Path(directory) / "installed" / "growth-funnel-diagnosis"
            shutil.copytree(ROOT / "skills/growth-funnel-diagnosis", install)
            fixture = Path(directory) / "input.json"
            shutil.copyfile(ROOT / "examples/lending/cohorts.json", fixture)
            script = install / "scripts/analyze.py"
            for format_name in ("json", "markdown"):
                result = subprocess.run([sys.executable, "-I", str(script), str(fixture),
                                         "--format", format_name], cwd=directory,
                                        capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)
                expected = self.run_command(fixture, "--format", format_name)
                self.assertEqual(result.stdout, expected.stdout)
            # Read exactly the documented standalone example and execute it.
            contract = (install / "references/input-contract.md").read_text()
            sample = contract.split("```json\n", 1)[1].split("```", 1)[0]
            fixture.write_text(sample)
            result = subprocess.run([sys.executable, "-I", str(script), str(fixture)],
                                    cwd=directory, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)[0]["funded_cac"], 10)


if __name__ == "__main__":
    unittest.main()
