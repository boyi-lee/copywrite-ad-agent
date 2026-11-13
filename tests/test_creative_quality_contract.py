import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CreativeQualityContractTests(unittest.TestCase):
    def test_machine_contract_has_all_distinct_quality_checks(self):
        contract = json.loads((ROOT / "schemas/creative-quality-contract.json").read_text())
        self.assertEqual(
            {"angle_id", "opening", "buyer_payoff", "distinctness", "evidence_boundary", "field_fit"},
            set(contract["required"]),
        )

    def test_regressions_cover_multiple_categories_and_failure_modes(self):
        fixture = json.loads((ROOT / "tests/fixtures/creative-quality-cases.json").read_text())
        cases = fixture["cases"]
        categories = {case["category"] for case in cases}
        self.assertGreaterEqual(len(categories), 4)
        expected_ids = {case["case_id"] for case in cases}
        self.assertTrue({"saas-feature-dump", "food-unsupported-promise", "apparel-distinct-motivation", "equipment-hook-only-variants", "two-line-hook-request"} <= expected_ids)
        self.assertEqual("fail", next(c for c in cases if c["case_id"] == "equipment-hook-only-variants")["expected"]["distinctness"])

    def test_angle_matrix_does_not_force_twenty_four_variants(self):
        matrix = (ROOT / "references/creative-angle-matrix.md").read_text()
        self.assertIn("Do not generate 24 combinations as a default", matrix)
        self.assertIn("shopper_motivation", matrix)
        self.assertIn("desired_progress", matrix)


if __name__ == "__main__":
    unittest.main()
