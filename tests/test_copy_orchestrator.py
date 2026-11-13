from pathlib import Path
import importlib.util, json, tempfile, unittest
import hashlib

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("copy_orchestrator",ROOT/"scripts/copy_orchestrator.py")
ORCH=importlib.util.module_from_spec(SPEC); assert SPEC.loader is not None; SPEC.loader.exec_module(ORCH)

class OrchestratorTests(unittest.TestCase):
    def setUp(self):
        self.brief=json.loads((ROOT/"tests/fixtures/callaway-real-brief.json").read_text())
        self.evidence=json.loads((ROOT/"tests/fixtures/callaway-real-evidence.json").read_text())
        self.tmp=tempfile.TemporaryDirectory(); self.run=Path(self.tmp.name)/"callaway-run"
    def tearDown(self): self.tmp.cleanup()
    def valid_review(self):
        draft=ORCH.read_json(ORCH.artifact(self.run,"10-copy-drafting"))
        rubric=(ROOT/"references/creative-quality-contract.md").read_bytes()
        rows=[]
        for item in draft["drafts"]:
            row={"angle_id":item["angle_id"]}
            for field in ("opening","buyer_payoff","distinctness","evidence_boundary","field_fit"):
                row[field]={"verdict":"pass","rationale":f"已檢查 {field} 與此角度文案及已提供證據。"}
            row["claim_verdicts"]=[{"claim_id":cid,"verdict":"pass","rationale":"已逐句對照來源事實。"} for cid in item["claim_ids"]]
            rows.append(row)
        return {"review_id":"review-1","reviewer_id":"external-reviewer","producer_id":"external-reviewer","reviewed_draft_sha256":ORCH.sha(draft),"reviewed_evidence_sha256":ORCH.load_manifest(self.run)["task"]["evidence_digest"],"rubric_sha256":hashlib.sha256(rubric).hexdigest(),"overall_verdict":"pass","used_writer_self_score":False,"angle_reviews":rows}
    def test_preview_creates_only_strategy_chain(self):
        ORCH.preview(self.brief,self.evidence,self.run)
        for name in ORCH.PREVIEW: self.assertTrue(ORCH.artifact(self.run,name).exists())
        for name in ORCH.POST: self.assertFalse(ORCH.artifact(self.run,name).exists())
    def test_pending_confirmation_blocks_draft(self):
        ORCH.preview(self.brief,self.evidence,self.run)
        with self.assertRaisesRegex(ValueError,"confirmed matrix"):
            ORCH.draft(self.run)
    def test_confirmation_digest_and_full_chain(self):
        ORCH.preview(self.brief,self.evidence,self.run)
        with self.assertRaisesRegex(ValueError,"scope_digest"):
            ORCH.confirm(self.run,{"confirmation_status":"confirmed","confirmation_id":"x","approved_angle_ids":["angle-dr"],"scope_digest":"bad"})
        c={"confirmation_status":"confirmed","confirmation_id":"x","approved_angle_ids":["angle-dr","angle-hy"],"scope_digest":ORCH.sha(ORCH.read_json(ORCH.artifact(self.run,"08-appeal-matrix")))}
        ORCH.confirm(self.run,c); ORCH.draft(self.run)
        self.assertEqual("independent_review", ORCH.load_manifest(self.run)["state"])
        with self.assertRaisesRegex(ValueError,"review must cover"):
            ORCH.import_review(self.run,{})
        ORCH.import_review(self.run,self.valid_review())
        run=ORCH.load_manifest(self.run)
        self.assertEqual("passed",run["status"])
        for name in ORCH.ALL: self.assertTrue(ORCH.artifact(self.run,name).exists())
        self.assertEqual(0, ORCH.verify(self.run))
    def test_empty_research_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"source fact"):
            ORCH.preview(self.brief,{"facts":[]},self.run)
    def test_writer_cannot_self_review_and_unsupported_hook_blocks(self):
        ORCH.preview(self.brief,self.evidence,self.run)
        matrix=ORCH.read_json(ORCH.artifact(self.run,"08-appeal-matrix"))
        ORCH.confirm(self.run,{"confirmation_status":"confirmed","confirmation_id":"x","approved_angle_ids":["angle-dr","angle-hy"],"scope_digest":ORCH.sha(matrix)})
        ORCH.draft(self.run)
        review=self.valid_review(); review["reviewer_id"]="copy_orchestrator"
        with self.assertRaisesRegex(ValueError,"writer cannot review"):
            ORCH.import_review(self.run,review)
        review=self.valid_review(); review["angle_reviews"][0]["opening"]["verdict"]="fail"
        with self.assertRaisesRegex(ValueError,"opening did not pass"):
            ORCH.import_review(self.run,review)

if __name__=="__main__": unittest.main()
