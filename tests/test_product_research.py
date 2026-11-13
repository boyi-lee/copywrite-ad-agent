from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import crawl_products  # noqa: E402
import validate_product_research  # noqa: E402


class ProductResearchTests(unittest.TestCase):
    def test_url_validation_deduplicates(self) -> None:
        urls = crawl_products.validate_urls(
            ["https://example.com/a", "https://example.com/a", "https://example.com/b"], 20
        )
        self.assertEqual(urls, ["https://example.com/a", "https://example.com/b"])

    def test_url_validation_rejects_non_http(self) -> None:
        with self.assertRaises(ValueError):
            crawl_products.validate_urls(["file:///tmp/private"], 20)

    def test_url_validation_rejects_private_network_by_default(self) -> None:
        with self.assertRaises(ValueError):
            crawl_products.validate_urls(["http://127.0.0.1:8000/product"], 20)

    def test_url_validation_allows_explicit_local_test_override(self) -> None:
        urls = crawl_products.validate_urls(
            ["http://127.0.0.1:8000/product"], 20, allow_private_network=True
        )
        self.assertEqual(urls, ["http://127.0.0.1:8000/product"])

    def test_json_ld_product_extraction_and_volatile_offer(self) -> None:
        html = """
        <script type="application/ld+json">
        {"@context":"https://schema.org","@type":"Product","name":"Shirt",
         "material":"Polyester","offers":{"@type":"Offer","price":"1000","priceCurrency":"TWD"}}
        </script>
        """
        nodes = crawl_products.product_json_ld(html)
        self.assertEqual(len(nodes), 1)
        facts = crawl_products.normalize_product_nodes(
            nodes, "https://example.com/products/shirt", "2026-07-20T00:00:00+00:00"
        )
        by_field = {fact["field"]: fact for fact in facts}
        self.assertEqual(by_field["name"]["value"], "Shirt")
        self.assertTrue(by_field["price"]["volatile"])
        self.assertFalse(by_field["material"]["volatile"])

    def test_pass_fixture_passes(self) -> None:
        payload = json.loads((ROOT / "tests/fixtures/product-research-pass.json").read_text())
        result = validate_product_research.verdict(payload)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["score"], 20)

    def test_blocked_fixture_is_blocked_not_passed(self) -> None:
        payload = json.loads((ROOT / "tests/fixtures/product-research-blocked.json").read_text())
        result = validate_product_research.verdict(payload)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(result["failed_criteria"])

    def test_verified_usp_needs_comparison_sources(self) -> None:
        payload = json.loads((ROOT / "tests/fixtures/product-research-pass.json").read_text())
        payload["usp_candidates"][0]["classification"] = "verified_usp"
        result = validate_product_research.verdict(payload)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("two source URLs" in item for item in result["failed_criteria"]))

    def test_checker_verdict_updates_run_record(self) -> None:
        result = {
            "status": "PASS",
            "score": 20,
            "failed_criteria": [],
            "human_review_required": True,
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            record_path = Path(temp_dir) / "run-record.json"
            record_path.write_text(
                json.dumps(
                    {
                        "ended_at": "",
                        "final_verdict": {},
                        "artifacts": [],
                        "unresolved_risks": [],
                        "live_ready": False,
                        "manual_check_required": True,
                    }
                )
            )
            verdict_path = Path(temp_dir) / "checker-verdict.json"
            validate_product_research.update_run_record(record_path, result, verdict_path)
            updated = json.loads(record_path.read_text())
            self.assertEqual(updated["final_verdict"]["status"], "passed")
            self.assertIn(str(verdict_path), updated["artifacts"])


if __name__ == "__main__":
    unittest.main()
