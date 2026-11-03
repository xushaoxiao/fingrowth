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
spec = importlib.util.spec_from_file_location("workspace", ROOT / "scripts/build_workspace.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class WorkspaceTest(unittest.TestCase):
    def setUp(self):
        self.rows = json.loads((ROOT / "examples/lending/cohorts.json").read_text())
        self.profile = json.loads((ROOT / "skills/growth-data-adapter/assets/identity-profile.json").read_text())

    def test_synthetic_demo_is_reproducible_and_source_is_unchanged(self):
        original = copy.deepcopy(self.rows)
        workspace = m.build_workspace(self.rows, self.profile)
        self.assertEqual(workspace, json.loads((ROOT / "examples/dashboard/workspace.json").read_text()))
        self.assertEqual(workspace["cohorts"], original)
        self.assertEqual(self.rows, original)
        self.assertEqual(len(workspace["experiments"]), 3)
        self.assertEqual(len(workspace["initiatives"]), 3)
        self.assertTrue(all("Hypothetical:" in c["title"] for c in workspace["experiments"] + workspace["initiatives"]))

    def test_renamed_nested_fields_map_without_numeric_coercion(self):
        profile = json.loads((ROOT / "skills/growth-data-adapter/assets/renamed-fields-profile.json").read_text())
        source = []
        for row in self.rows:
            source.append({
                "metadata": {key: row[key] for key in ("cohort", "window", "outcome_as_of", "currency", "synthetic", "mature")},
                "populations": row["counts"],
                "economics": {key: row[key] for key in m.MONEY},
                "unused_aggregate_note": "Not copied to canonical rows",
            })
        workspace = m.build_workspace(source, profile)
        self.assertEqual(workspace["cohorts"], self.rows)
        mapping = {item["target"]: item for item in workspace["provenance"]["mappings"]}
        self.assertEqual(mapping["counts.disbursed"]["source"], "populations.disbursed")
        self.assertEqual(mapping["revenue"]["transform"], "copy without coercion")
        source[0]["economics"]["revenue"] = "42000"
        with self.assertRaisesRegex(ValueError, "JSON number"):
            m.build_workspace(source, profile)

    def test_missing_source_value_does_not_become_zero(self):
        del self.rows[0]["funding_cost"]
        with self.assertRaisesRegex(ValueError, "mapped source field is missing"):
            m.build_workspace(self.rows, self.profile)

    def test_mapping_must_cover_all_canonical_fields(self):
        del self.profile["field_map"]["counts.disbursed"]
        with self.assertRaisesRegex(ValueError, "field_map"):
            m.build_workspace(self.rows, self.profile)

    def test_mapping_does_not_evaluate_expressions_or_constants(self):
        self.profile["field_map"]["revenue"] = "revenue * 2"
        with self.assertRaisesRegex(ValueError, "mapped source field is missing"):
            m.build_workspace(self.rows, self.profile)
        self.profile["field_map"]["revenue"] = 0
        with self.assertRaisesRegex(ValueError, "nonempty string"):
            m.build_workspace(self.rows, self.profile)

    def test_approved_mode_preserves_false_and_requires_reference(self):
        for row in self.rows:
            row["synthetic"] = False
        self.profile["data_mode"] = "approved_aggregate"
        with self.assertRaisesRegex(ValueError, "approval_reference"):
            m.build_workspace(self.rows, self.profile)
        self.profile["provenance"]["approval_reference"] = "synthetic-test-approval-reference"
        workspace = m.build_workspace(self.rows, self.profile)
        self.assertTrue(all(row["synthetic"] is False for row in workspace["cohorts"]))
        self.assertEqual(workspace["data_mode"], "approved_aggregate")
        self.assertEqual(workspace["provenance"]["approval_reference"], "synthetic-test-approval-reference")

    def test_synthetic_mismatch_and_mixed_modes_are_rejected(self):
        self.rows[1]["synthetic"] = False
        with self.assertRaisesRegex(ValueError, "synthetic flag"):
            m.build_workspace(self.rows, self.profile)
        self.profile["data_mode"] = "approved_aggregate"
        self.profile["provenance"]["approval_reference"] = "synthetic-test-reference"
        with self.assertRaisesRegex(ValueError, "synthetic flag"):
            m.build_workspace(self.rows, self.profile)

    def test_date_and_population_validation(self):
        for field, value in (("window", "2026-02-30/2026-03-01"),
                             ("window", "2026-02-01/2026-01-31"),
                             ("outcome_as_of", "2026-01-30"),
                             ("mature", "true"), ("synthetic", 1), ("currency", "usd")):
            with self.subTest(field=field, value=value):
                rows = copy.deepcopy(self.rows)
                rows[0][field] = value
                with self.assertRaises(ValueError):
                    m.build_workspace(rows, self.profile)
        for value in (999999, True, 1.5, -1, m._implementation["MAX_SAFE_INTEGER"] + 1):
            with self.subTest(count=value):
                rows = copy.deepcopy(self.rows)
                rows[0]["counts"]["disbursed"] = value
                with self.assertRaises(ValueError):
                    m.build_workspace(rows, self.profile)

    def test_fractional_money_and_bounds(self):
        for value in (0, 0.01, 1.23, 10**12):
            with self.subTest(valid=value):
                self.rows[0]["revenue"] = value
                self.assertEqual(m.build_workspace(self.rows, self.profile)["cohorts"][0]["revenue"], value)
        for value in (0.001, -1, 10**12 + 1, float("nan"), float("inf"), True, "1.23", 10**400):
            with self.subTest(invalid_type=type(value).__name__):
                self.rows[0]["revenue"] = value
                with self.assertRaises(ValueError):
                    m.build_workspace(self.rows, self.profile)

    def test_workspace_rejects_unknown_fields_duplicates_and_wrong_planning_shape(self):
        base = m.build_workspace(self.rows, self.profile)
        mutations = [
            lambda w: w.update(secret="not a supported field"),
            lambda w: w.update(schema_version="2.0"),
            lambda w: w["cohorts"].append(copy.deepcopy(w["cohorts"][0])),
            lambda w: w["cohorts"][0].update(unknown=0),
            lambda w: w["provenance"].update(extracted_at="2026-11-03"),
            lambda w: w["provenance"]["mappings"].append(copy.deepcopy(w["provenance"]["mappings"][0])),
            lambda w: w["experiments"][0].update(guardrails="safe"),
            lambda w: w["initiatives"].append(copy.deepcopy(w["initiatives"][0])),
        ]
        for index, mutate in enumerate(mutations):
            workspace = copy.deepcopy(base)
            mutate(workspace)
            with self.subTest(case=index), self.assertRaises(ValueError):
                m.validate_workspace(workspace)

    def test_oversized_workspace_is_rejected_before_import(self):
        base = m.build_workspace(self.rows, self.profile)
        mutations = [
            (lambda w: w.update(description="x" * 10001), "10000 characters"),
            (lambda w: w.update(description="\U0001f600" * 5001), "10000 characters"),
            (lambda w: w.update(cohorts=[copy.deepcopy(w["cohorts"][0])] * 201), "200 entries"),
            (lambda w: w.update(experiments=[copy.deepcopy(w["experiments"][0])] * 1001), "1000 entries"),
            (lambda w: w.update(initiatives=[copy.deepcopy(w["initiatives"][0])] * 1001), "1000 entries"),
            (lambda w: w["provenance"].update(mappings=[copy.deepcopy(w["provenance"]["mappings"][0])] * 1001), "1000 entries"),
            (lambda w: w["experiments"][0].update(guardrails=["hypothetical guardrail"] * 1001), "1000 entries"),
        ]
        for index, (mutate, message) in enumerate(mutations):
            workspace = copy.deepcopy(base)
            mutate(workspace)
            with self.subTest(case=index), self.assertRaisesRegex(ValueError, message):
                m.validate_workspace(workspace)
        with self.assertRaisesRegex(ValueError, "200 aggregate cohorts"):
            m.build_workspace(self.rows * 101, self.profile)

    def test_timestamp_invalid_clock_and_offset_are_rejected(self):
        for stamp in ("2026-11-03T25:00:00Z", "2026-11-03T00:61:00Z", "2026-11-03T00:00:60Z",
                      "2026-11-03T00:00:00+24:00", "2026-11-03T00:00:00+01:60",
                      "2026-11-03T00:00:00-00:99"):
            profile = copy.deepcopy(self.profile)
            profile["provenance"]["extracted_at"] = stamp
            with self.subTest(stamp=stamp), self.assertRaisesRegex(ValueError, "timestamp"):
                m.build_workspace(self.rows, profile)

    def test_individually_valid_cards_cannot_exceed_total_utf8_capacity(self):
        workspace = m.build_workspace(self.rows, self.profile)
        template = copy.deepcopy(workspace["experiments"][0])
        # 3000 UTF-16 code units each, but 9000 UTF-8 bytes; all per-field and
        # collection limits are valid while the total exceeds the 2 MB import.
        workspace["experiments"] = [
            {**template, "id": f"hyp-large-{index}", "hypothesis": "\u4f60" * 3000}
            for index in range(250)
        ]
        self.assertGreater(len((json.dumps(workspace, ensure_ascii=False, indent=2) + "\n").encode("utf-8")), 2000000)
        with self.assertRaisesRegex(ValueError, "2000000 UTF-8 bytes"):
            m.validate_workspace(workspace)

    def test_canonical_serializer_keeps_unicode_and_exact_trailing_newline(self):
        workspace = m.build_workspace(self.rows, self.profile)
        workspace["description"] = "\u4f60\u597d — synthetic workspace"
        output = m.serialize_workspace(workspace)
        self.assertEqual(output, json.dumps(workspace, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
        self.assertIn("\u4f60\u597d", output)
        self.assertNotIn("\\u4f60", output)
        self.assertEqual(json.loads(output), workspace)


class WorkspaceCommandTest(unittest.TestCase):
    def test_cli_oversized_workspace_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            profile = json.loads((ROOT / "skills/growth-data-adapter/assets/identity-profile.json").read_text())
            template = profile["experiments"][0]
            profile["experiments"] = [
                {**template, "id": f"hyp-large-{index}", "hypothesis": "\u4f60" * 3000}
                for index in range(250)
            ]
            profile_path, output = base / "profile.json", base / "output.json"
            profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
            output.write_text("existing output")
            result = subprocess.run([sys.executable, str(ROOT / "scripts/build_workspace.py"),
                                     str(ROOT / "examples/lending/cohorts.json"), "--profile", str(profile_path),
                                     "--output", str(output)], capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("2000000 UTF-8 bytes", result.stderr)
            self.assertEqual(output.read_text(), "existing output")

    def test_copied_skill_executes_without_repository(self):
        with tempfile.TemporaryDirectory(prefix="fingrowth adapter ") as directory:
            base = Path(directory)
            skill = base / "growth-data-adapter"
            shutil.copytree(ROOT / "skills/growth-data-adapter", skill,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            source = base / "cohorts.json"
            shutil.copyfile(ROOT / "examples/lending/cohorts.json", source)
            result = subprocess.run([sys.executable, "-I", str(skill / "scripts/build_workspace.py"),
                                     str(source), "--profile", str(skill / "assets/identity-profile.json")],
                                    cwd=base, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["cohorts"], json.loads(source.read_text()))

    def test_cli_invalid_source_has_no_partial_output_and_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "source.json"
            output = base / "workspace.json"
            output.write_text("existing output")
            for document in ('[{"cohort": "incomplete"}]', '[{"a":1,"a":2}]', "null", "{"):
                source.write_text(document)
                result = subprocess.run([sys.executable, str(ROOT / "scripts/build_workspace.py"),
                                         str(source), "--profile", str(ROOT / "skills/growth-data-adapter/assets/identity-profile.json"),
                                         "--output", str(output)], capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(output.read_text(), "existing output")

    def test_cli_refuses_to_overwrite_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.json"
            shutil.copyfile(ROOT / "examples/lending/cohorts.json", source)
            original = source.read_bytes()
            result = subprocess.run([sys.executable, str(ROOT / "scripts/build_workspace.py"), str(source),
                                     "--profile", str(ROOT / "skills/growth-data-adapter/assets/identity-profile.json"),
                                     "--output", str(source)], capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
