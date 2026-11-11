import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/growth-funnel-diagnosis"
FIXTURE = ROOT / "examples/registration-credit/synthetic-intake.json"


class RegistrationCreditTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.cwd = Path(self.directory.name)
        self.skill = self.cwd / "copied-skill"
        shutil.copytree(SKILL, self.skill)
        self.intake = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def run_cli(self, document, output_format="json"):
        path = self.cwd / "intake.json"
        path.write_text(document if isinstance(document, str) else json.dumps(document), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(self.skill / "scripts/analyze_registration_credit.py"), str(path),
             "--format", output_format],
            cwd=self.cwd, capture_output=True, text=True, encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )

    def assert_invalid(self, document, message):
        result = self.run_cli(document)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn(message, result.stderr)

    def test_copied_skill_reports_distinct_rankings_and_cumulative_conversion(self):
        result = self.run_cli(self.intake)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["cumulative_conversion"]["credit_approved"], 0.224)
        self.assertEqual(report["investigation_candidates"]["by_not_progressed"][0]["from"], "registered")
        self.assertEqual(report["investigation_candidates"]["by_lowest_conversion"][0]["from"], "kyc_passed")
        for step in report["steps"]:
            self.assertEqual(step["population"], step["converted"] + step["not_progressed"])
        markdown = self.run_cli(self.intake, "markdown")
        self.assertEqual(markdown.returncode, 0, markdown.stderr)
        self.assertIn("未继续人数最多：注册 → 填资完成", markdown.stdout)
        self.assertIn("相邻转化率最低：KYC 通过 → 银行资料完成", markdown.stdout)

    def test_blank_template_and_duplicate_keys_fail_without_report(self):
        template = SKILL / "assets/registration-credit-intake.json"
        self.assert_invalid(template.read_text(encoding="utf-8"), "ready_for_analysis")
        self.assert_invalid('{"status":"ready_for_analysis","status":"awaiting_aggregate_evidence"}',
                            "duplicate JSON field")

    def test_incomplete_local_followup_and_premature_extraction_are_rejected(self):
        early = copy.deepcopy(self.intake)
        early["cohort"]["observation_cutoff"] = "2026-02-06"
        self.assert_invalid(early, "full fixed follow-up window")
        self.intake["cohort"]["timezone"] = "America/Mexico_City"
        self.assert_invalid(self.intake, "after the end of the local observation cutoff date")
        self.intake["provenance"]["extracted_at"] = "2026-02-08T00:00:00-06:00"
        result = self.run_cli(self.intake)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_counts_or_unconfirmed_quality_gate(self):
        for value in (None, True, -1, 701):
            with self.subTest(value=value):
                row = copy.deepcopy(self.intake)
                row["stages"][2]["unique_people"] = value
                self.assert_invalid(row, "nonnegative nested integer")
        self.intake["quality_checks"]["same_journey_linkage"] = False
        self.assert_invalid(self.intake, "same_journey_linkage must be confirmed")

    def test_approved_aggregate_declaration_requires_authorization_reference(self):
        self.intake["provenance"]["data_kind"] = "approved_aggregate"
        self.assert_invalid(self.intake, "authorization_reference")
        self.intake["provenance"]["authorization_reference"] = "synthetic test reference"
        result = self.run_cli(self.intake)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["data_kind"], "approved_aggregate")
        self.assertNotIn("synthetic test reference", result.stdout)

    def test_zero_denominators_and_ties(self):
        for stage, count in zip(self.intake["stages"], (6, 4, 2, 0, 0)):
            stage["unique_people"] = count
        markdown = self.run_cli(self.intake, "markdown")
        self.assertEqual(markdown.returncode, 0, markdown.stderr)
        self.assertIn("注册 → 填资完成、填资完成 → KYC 通过、KYC 通过 → 银行资料完成", markdown.stdout)
        self.assertIn("银行资料完成 → 授信通过 | 0 | 0 | 0 | 未知 | 0.00%", markdown.stdout)
        for stage, count in zip(self.intake["stages"], (16, 8, 4, 2, 1)):
            stage["unique_people"] = count
        markdown = self.run_cli(self.intake, "markdown")
        self.assertEqual(markdown.returncode, 0, markdown.stderr)
        self.assertIn("相邻转化率最低：注册 → 填资完成、填资完成 → KYC 通过、"
                      "KYC 通过 → 银行资料完成、银行资料完成 → 授信通过", markdown.stdout)


if __name__ == "__main__":
    unittest.main()
