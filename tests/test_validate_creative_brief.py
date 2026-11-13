import copy
import hashlib
import unittest
from pathlib import Path
from scripts.validate_creative_brief import RUBRIC, canonical_sha256, validate


def valid_artifacts():
    brief_set = {
        "schema_version": "1.0.0",
        "request": {"brand": "Demo", "objective": "Purchase", "platform": "Meta", "ad_format": "Feed", "market": "TW", "language": "zh-TW", "requested_counts": {"TOFU": 1, "MOFU": 0, "BOFU": 0}},
        "source_evidence": [{"evidence_id": "e1", "url": "https://example.com/p", "locator": "Product details", "fact": "Official product name", "evidence_class": "SUPPORTED_BY_BRIEF"}],
        "briefs": [{"brief_id": "b1", "funnel_stage": "TOFU", "target": {"audience": "使用者確認的受眾", "situation": "通勤", "confirmation_status": "user_confirmed"}, "shopper_tension": "選品時不知道差異", "creative_angle": "從商品選擇切入", "primary_buying_reason": "清楚辨認商品類別", "key_message": "先確認商品類別", "product_anchor": "商品 A", "claim_evidence": [{"claim": "官方商品名稱", "evidence_id": "e1", "evidence_class": "SUPPORTED_BY_BRIEF"}], "visual_direction": "呈現商品頁可見商品", "cta_direction": "查看商品", "source_refs": ["e1"], "unknowns": [], "distinctness_reason": "聚焦類別辨識"}]
    }
    row_criteria = {k: {"verdict": "PASS", "rationale": "有對應欄位與依據"} for k in ("target_clarity", "funnel_fit", "shopper_tension", "product_and_claim_evidence", "message_focus", "creative_angle_clarity", "visual_direction_fit", "next_action", "angle_distinctness", "brand_and_campaign_fit")}
    review = {
        "reviewer_provenance": {"reviewer_type": "ai_second_pass", "reviewer_id": "reviewer-01", "method": "fresh rubric review without writer self-score", "rubric_sha256": hashlib.sha256(RUBRIC.read_bytes()).hexdigest(), "completed_at": "2026-09-30T00:00:00Z"},
        "decision": "PASS",
        "reviewed_brief_set_sha256": canonical_sha256(brief_set),
        "brief_reviews": [{"brief_id": "b1", "verdict": "PASS", "criteria": row_criteria, "finished_asset_checks": {"verdict": "NOT_APPLICABLE", "rationale": "尚無成品視覺可評"}, "blocking_findings": []}],
        "batch_review": {"verdict": "PASS", "batch_coverage": {"verdict": "PASS", "rationale": "requested counts match"}, "similarity_check": {"verdict": "PASS", "rationale": "no duplicate angle"}, "blocking_findings": []}
    }
    return brief_set, review


class BriefGateTests(unittest.TestCase):
    def test_matching_review_allows_sheet_write(self):
        briefs, review = valid_artifacts()
        self.assertEqual(validate(briefs, review), [])

    def test_non_meta_platform_blocks(self):
        briefs, review = valid_artifacts()
        briefs["request"]["platform"] = "Google"
        review["reviewed_brief_set_sha256"] = canonical_sha256(briefs)
        self.assertTrue(any("Meta briefs only" in e for e in validate(briefs, review)))

    def test_wrong_funnel_count_blocks(self):
        briefs, review = valid_artifacts()
        briefs["request"]["requested_counts"]["TOFU"] = 8
        review["reviewed_brief_set_sha256"] = canonical_sha256(briefs)
        self.assertTrue(any("funnel counts mismatch" in e for e in validate(briefs, review)))

    def test_changed_brief_digest_blocks(self):
        briefs, review = valid_artifacts()
        briefs["briefs"][0]["creative_angle"] = "改過內容"
        self.assertTrue(any("digest does not match" in e for e in validate(briefs, review)))

    def test_row_block_blocks_entire_batch(self):
        briefs, review = valid_artifacts()
        review["brief_reviews"][0]["verdict"] = "BLOCK"
        self.assertTrue(any("not individually review-passed" in e for e in validate(briefs, review)))

    def test_blocking_batch_review_blocks(self):
        briefs, review = valid_artifacts()
        review["batch_review"]["verdict"] = "BLOCK"
        review["batch_review"]["blocking_findings"] = ["角度重複"]
        self.assertTrue(validate(briefs, review))

    def test_unverified_claim_evidence_blocks(self):
        briefs, review = valid_artifacts()
        briefs["source_evidence"][0]["evidence_class"] = "INFERRED"
        review["reviewed_brief_set_sha256"] = canonical_sha256(briefs)
        self.assertTrue(any("non-verified evidence class" in e for e in validate(briefs, review)))

    def test_unapproved_target_blocks(self):
        briefs, review = valid_artifacts()
        briefs["briefs"][0]["target"]["confirmation_status"] = "hypothesis"
        self.assertTrue(any("is not one of" in e for e in validate(briefs, review)))

    def test_unknown_field_fails_schema_validation(self):
        briefs, review = valid_artifacts()
        briefs["unexpected"] = True
        self.assertTrue(any("Additional properties are not allowed" in e for e in validate(briefs, review)))

    def test_wrong_type_fails_cleanly(self):
        briefs, review = valid_artifacts()
        briefs["briefs"][0]["source_refs"] = [[]]
        errors = validate(briefs, review)
        self.assertTrue(errors)
        self.assertTrue(any("is not of type 'string'" in e for e in errors))

    def test_missing_per_brief_criterion_blocks(self):
        briefs, review = valid_artifacts()
        del review["brief_reviews"][0]["criteria"]["creative_angle_clarity"]
        self.assertTrue(any("creative_angle_clarity" in e for e in validate(briefs, review)))

    def test_missing_finished_asset_disposition_blocks(self):
        briefs, review = valid_artifacts()
        del review["brief_reviews"][0]["finished_asset_checks"]
        self.assertTrue(any("finished_asset_checks" in e for e in validate(briefs, review)))

    def test_wrong_rubric_digest_blocks(self):
        briefs, review = valid_artifacts()
        review["reviewer_provenance"]["rubric_sha256"] = "0" * 64
        self.assertTrue(any("did not bind" in e for e in validate(briefs, review)))

if __name__ == "__main__":
    unittest.main()
