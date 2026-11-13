from pathlib import Path
import importlib.util
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "copy_run.py"
SPEC = importlib.util.spec_from_file_location("copy_run", MODULE_PATH)
RUN = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RUN)


def complete_run():
    run = RUN.init_run({"brand": "Callaway", "product_url": "https://example.com", "funnel_stage": "MOFU"}, "test-run")
    outputs = {
        "product_research": {"evidence_artifact_ref": "evidence.json", "source_provenance": [{"source_url": "https://example.com", "source_type": "product", "source_locator": "page", "evidence_text": "verified", "captured_at": "now", "confidence": "high"}]},
        "persona_hypothesis": {"hypotheses": [{"persona": "正在比較球桿的球友", "evidence_refs": ["evidence.json"], "confidence": "medium", "jtbd": "找到適合目前球路的球桿", "decision_barrier": "不確定差異"}]},
        "shopper_tension": {"selected_or_proposed_tensions": [{"persona_ref": "p1", "use_moment": "開球", "job_to_be_done": "比較彈道設定", "friction": "難判斷", "belief_gap": "不知設定是否有用", "evidence_refs": ["evidence.json"]}]},
        "funnel_strategy": {"business_objective": "purchase", "funnel_stage": "MOFU", "audience_state": "正在比較", "buying_task": "判斷是否購買", "rationale": "比較差異", "evidence_refs": ["evidence.json"]},
        "motivation_strategy": {"maslow_primary": "esteem", "purchase_motivation": "提高選擇信心", "why_this_motivation_fits": "比較情境", "evidence_refs": ["evidence.json"]},
        "value_translation": {"usp_ladder": [{"feature": "可調設定", "evidence": "evidence.json", "functional_benefit": "提供比較依據", "use_case": "開球前", "felt_outcome": "更有把握", "purchase_reason": "值得查看", "feature_status": "verified", "evidence_status": "verified"}]},
        "framework_selection": {"selected_framework": "FEB", "selection_reason": "把設定連到選擇利益", "rejected_frameworks": ["PAS"], "stage_fit": "MOFU"},
        "appeal_matrix": {"requested_angle_count": 1, "proposed_angles": [{"angle_id": "a1", "persona_ref": "p1", "jtbd_tension": "比較彈道", "funnel": "MOFU", "maslow_motivation": "esteem", "usp_ladder_refs": ["u1"], "framework": "FEB", "cta_rationale": "查看規格", "source_evidence_refs": ["evidence.json"], "distinctness_reason": "以設定比較為核心"}], "pairwise_distinctness": []},
    }
    for stage in RUN.STAGES[1:9]: run = RUN.advance(run, stage, outputs[stage])
    run = RUN.advance(run, "awaiting_user_confirmation", {"confirmation_status": "confirmed", "confirmation_id": "c1", "approved_angle_ids": ["a1"], "scope_digest": "d", "confirmed_at": "now"}, actor="user")
    run = RUN.advance(run, "copy_drafting", {"drafts": [{"angle_id": "a1", "claim_ids": ["c1"]}]})
    run = RUN.advance(run, "claim_safety", {"claim_audit": [{"claim_id": "c1", "evidence_refs": ["evidence.json"], "verdict": "pass"}]})
    run = RUN.advance(run, "deterministic_validation", {"passed": True, "exit_code": 0})
    run = RUN.advance(run, "independent_review", {"overall_verdict": "pass", "reviewer_type": "independent", "used_writer_self_score": False})
    return RUN.advance(run, "learning", {"outcome": "no_rule_change", "reason": "baseline"})


class CopyRunTests(unittest.TestCase):
    def test_confirmation_gate_blocks_drafting(self):
        run = RUN.init_run({}, "x")
        with self.assertRaisesRegex(ValueError, "confirmation gate"):
            RUN.advance(run, "copy_drafting", {"drafts": []})

    def test_manual_delivery_without_run_fails(self):
        issues = RUN.validate_run({"workflow_id": "copywrite-ad-agent", "status": "in_progress", "task": {}, "stages": {}})
        self.assertTrue(any("stage not passed" in issue for issue in issues))

    def test_happy_path_passes_but_is_not_live_ready(self):
        run = complete_run()
        self.assertEqual([], RUN.validate_run(run))
        self.assertEqual("passed", run["final_verdict"]["status"])
        self.assertFalse(run["final_verdict"]["live_ready"])
        self.assertTrue(run["final_verdict"]["manual_check_required"])

    def test_unapproved_angle_fails(self):
        run = RUN.init_run({}, "x")
        run["state"] = "copy_drafting"
        run["stages"]["awaiting_user_confirmation"]["output"] = {"confirmation_status": "confirmed", "approved_angle_ids": ["a1"]}
        with self.assertRaisesRegex(ValueError, "unapproved"):
            RUN.advance(run, "copy_drafting", {"drafts": [{"angle_id": "a2"}]})

    def test_missing_claim_audit_and_review_fail(self):
        run = complete_run()
        run["stages"]["claim_safety"]["output"]["claim_audit"] = []
        run["stages"]["independent_review"]["output"]["overall_verdict"] = "pending"
        issues = RUN.validate_run(run)
        self.assertTrue(any("claim safety" in issue for issue in issues))
        self.assertTrue(any("independent review" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
