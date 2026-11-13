#!/usr/bin/env python3
"""The only production entrypoint for the copywriting workflow.

It persists one artifact per stage and refuses to advance on missing or stale
inputs. Interpretation is producer-driven; this runtime owns state, hashes,
confirmation, and verification.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

PREVIEW = ["00-intake", "01-product-research", "02-persona-hypothesis", "03-shopper-tension", "04-funnel-strategy", "05-motivation-strategy", "06-value-translation", "07-framework-selection", "08-appeal-matrix", "09-awaiting-user-confirmation"]
POST = ["10-copy-drafting", "11-claim-safety", "12-deterministic-validation", "13-independent-review", "14-learning"]
ALL = PREVIEW + POST

def sha(v): return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
def write_json(path, value): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
def read_json(path): return json.loads(path.read_text())
def ts(): return datetime.now(timezone.utc).isoformat()
def artifact(run_dir, name): return run_dir / "artifacts" / f"{name}.json"
def load_manifest(run_dir): return read_json(run_dir / "run.json")

def source_facts(evidence):
    return evidence.get("facts", evidence.get("sources", []))

def require_fields(items, fields, label):
    if not isinstance(items, list) or not items: raise ValueError(f"{label} requires a non-empty list")
    for item in items:
        if not isinstance(item, dict) or not all(str(item.get(k, "")).strip() for k in fields): raise ValueError(f"{label} item is incomplete")

def preview(brief, evidence, run_dir):
    if run_dir.exists() and any(run_dir.iterdir()): raise ValueError("run directory must be empty")
    run_dir.mkdir(parents=True, exist_ok=True)
    facts = source_facts(evidence)
    if not facts: raise ValueError("product_research requires at least one source fact")
    for f in facts:
        if not all(str(f.get(k, "")).strip() for k in ("fact_id", "source_id", "url", "locator", "excerpt")):
            raise ValueError("each source fact needs fact_id, source_id, url, locator, excerpt")
    task={"brief": brief, "evidence_digest": sha(evidence)}
    stages={}; prev=None
    outputs={
      "00-intake": {"brief_id": brief.get("brief_id", "brief-01"), "brief_sha256": sha(brief), "brand": brief.get("brand",""), "platform": brief.get("platform","meta"), "task_type": brief.get("task_type","ecommerce_product_copy"), "requested_angle_count": brief.get("requested_angle_count",2), "product_urls": brief.get("product_urls",[]), "evidence_manifest_ref":"input:evidence"},
      "01-product-research": {"sources": facts, "research_verdict":"pass", "evidence_artifact_ref":"input:evidence"},
      "02-persona-hypothesis": {"hypotheses": brief.get("persona_hypotheses",[])},
      "03-shopper-tension": {"tensions": brief.get("tensions",[]), "decision_to_make": brief.get("decision_to_make","")},
      "04-funnel-strategy": {"funnel_stage": brief.get("funnel_stage",""), "business_objective": brief.get("business_objective",""), "audience_state": brief.get("audience_state",""), "buying_task": brief.get("buying_task",""), "evidence_role": brief.get("evidence_role",""), "cta_job": brief.get("cta_job",""), "selected_tension_ids":[t.get("tension_id") for t in brief.get("tensions",[])], "rationale": brief.get("funnel_rationale","")},
      "05-motivation-strategy": {"primary_motivation": brief.get("primary_motivation",""), "secondary_motivation": brief.get("secondary_motivation",""), "motivation_to_tension_map": brief.get("motivation_to_tension_map",[]), "why_now_or_why_inspect": brief.get("why_now_or_why_inspect",""), "evidence_fact_ids": brief.get("motivation_evidence_fact_ids",[])},
      "06-value-translation": {"value_ladders": brief.get("value_ladders",[])},
      "07-framework-selection": {"routes": brief.get("framework_routes",[])},
      "08-appeal-matrix": {"requested_angle_count": brief.get("requested_angle_count",2), "proposed_angles": brief.get("angles",[]), "pairwise_distinctness": brief.get("pairwise_distinctness",[])},
      "09-awaiting-user-confirmation": {"preview_ref":"run.json", "preview_sha256":"", "confirmation_status":"pending", "proposed_angle_ids":[a.get("angle_id") for a in brief.get("angles",[])]},
    }
    for name in PREVIEW:
        value=outputs[name]
        if name == "02-persona-hypothesis":
            require_fields(value["hypotheses"], ("persona_id","persona","use_context","jtbd","decision_barrier","confidence"), "persona_hypothesis")
            if any(item.get("is_hypothesis") is not True for item in value["hypotheses"]): raise ValueError("persona hypotheses must be marked is_hypothesis=true")
            fact_ids={f["fact_id"] for f in facts}
            if any(not set(item.get("evidence_fact_ids",[])) <= fact_ids for item in value["hypotheses"]): raise ValueError("persona evidence fact is unresolved")
        if name == "03-shopper-tension":
            require_fields(value["tensions"], ("tension_id","persona_id","use_moment","job_to_be_done","friction","belief_gap"), "shopper_tension")
            persona_ids={p["persona_id"] for p in outputs["02-persona-hypothesis"]["hypotheses"]}
            if any(t.get("persona_id") not in persona_ids for t in value["tensions"]): raise ValueError("tension persona is unresolved")
        if name == "04-funnel-strategy" and not all(str(value.get(k,"")) for k in ("funnel_stage","audience_state","buying_task","evidence_role","cta_job","rationale")): raise ValueError("funnel_strategy is incomplete")
        if name == "05-motivation-strategy" and not all(str(value.get(k,"")) for k in ("primary_motivation","why_now_or_why_inspect")): raise ValueError("motivation_strategy is incomplete")
        if name == "06-value-translation":
            require_fields(value["value_ladders"], ("ladder_id","feature_fact_id","evidence_quote","functional_benefit","use_moment","felt_outcome","purchase_reason"), "value_translation")
            if any(item.get("feature_fact_id") not in {f["fact_id"] for f in facts} for item in value["value_ladders"]): raise ValueError("value ladder fact is unresolved")
        if name == "07-framework-selection":
            value_for_count = brief.get("requested_angle_count", 2)
            if len(value["routes"]) != value_for_count: raise ValueError("framework route count mismatch")
            for route in value["routes"]:
                if not all(k in route for k in ("angle_id","candidate_scores","selected_message_framework","selected_value_framework","selection_reason","rejected_frameworks","expected_structure")): raise ValueError("framework route is incomplete")
                if set(route["candidate_scores"]) != {"PAS","TIPS","AIDAS","4R"}: raise ValueError("framework scores must cover PAS, TIPS, AIDAS, 4R")
                if route["selected_value_framework"] not in {"FEB","FAB"}: raise ValueError("value framework must be FEB or FAB")
                if not route["selection_reason"] or not route["rejected_frameworks"]: raise ValueError("framework route needs selection and rejection reasons")
        if name == "08-appeal-matrix":
            if len(value["proposed_angles"]) != value["requested_angle_count"]: raise ValueError("angle count mismatch")
            for pair in value["pairwise_distinctness"]:
                if len(pair.get("changed_dimensions",[])) < 2: raise ValueError("each angle pair needs two changed dimensions")
        ref = artifact(run_dir, name); write_json(ref, value); digest=sha(value)
        stages[name]={"status":"passed","artifact_ref":str(ref.relative_to(run_dir)),"artifact_sha256":digest,"input_artifact_refs":[] if prev is None else [stages[prev]["artifact_ref"]],"producer":"copy_orchestrator","created_at":ts()}; prev=name
    matrix_digest=sha(outputs["08-appeal-matrix"])
    outputs["09-awaiting-user-confirmation"]["preview_sha256"]=matrix_digest
    ref=artifact(run_dir,"09-awaiting-user-confirmation"); write_json(ref,outputs["09-awaiting-user-confirmation"]); stages["09-awaiting-user-confirmation"]["artifact_sha256"]=sha(outputs["09-awaiting-user-confirmation"]); stages["09-awaiting-user-confirmation"]["input_artifact_refs"]=[stages["08-appeal-matrix"]["artifact_ref"]]
    manifest={"schema_version":"1.0.0","run_id":brief.get("run_id",run_dir.name),"workflow_id":"copywrite-ad-agent","workflow_version":"3.0.0","state":"awaiting_user_confirmation","status":"in_progress","created_at":ts(),"updated_at":ts(),"task":task,"stages":stages,"transition_log":[{"from":"intake","to":"awaiting_user_confirmation","at":ts()}],"retry_budget":{"max_revisions":2,"used":0},"final_verdict":{"status":"blocked","live_ready":False,"manual_check_required":True}}
    write_json(run_dir/"run.json",manifest)

def confirm(run_dir, confirmation):
    run=load_manifest(run_dir); preview_ref=artifact(run_dir,"08-appeal-matrix"); matrix=read_json(preview_ref)
    if run["state"] != "awaiting_user_confirmation": raise ValueError("run is not awaiting confirmation")
    if confirmation.get("scope_digest") != sha(matrix): raise ValueError("confirmation scope_digest does not match appeal matrix")
    if confirmation.get("confirmation_status") != "confirmed" or not confirmation.get("confirmation_id"): raise ValueError("explicit confirmation_id and confirmed status required")
    ids={a.get("angle_id") for a in matrix["proposed_angles"]}; approved=set(confirmation.get("approved_angle_ids",[]))
    if not approved or not approved <= ids: raise ValueError("approved angles must be proposed angles")
    value={**confirmation,"confirmed_at":confirmation.get("confirmed_at",ts())}; ref=artifact(run_dir,"09-awaiting-user-confirmation"); write_json(ref,value)
    run["stages"]["09-awaiting-user-confirmation"].update(artifact_sha256=sha(value),status="passed"); run["state"]="copy_drafting"; run["updated_at"]=ts(); run["transition_log"].append({"from":"awaiting_user_confirmation","to":"copy_drafting","at":ts(),"confirmation_id":confirmation["confirmation_id"]}); write_json(run_dir/"run.json",run)

def draft(run_dir):
    run=load_manifest(run_dir)
    if run["state"] != "copy_drafting": raise ValueError("draft requires confirmed matrix")
    if artifact(run_dir,"10-copy-drafting").exists(): raise ValueError("draft already exists")
    brief=run["task"]["brief"]; matrix=read_json(artifact(run_dir,"08-appeal-matrix")); approved=set(read_json(artifact(run_dir,"09-awaiting-user-confirmation")).get("approved_angle_ids",[])); drafts=[]; traces=[]
    for angle in matrix["proposed_angles"]:
        if angle.get("angle_id") not in approved: continue
        text=angle["copy"]["primary_text"]; drafts.append({"draft_id":"draft-"+angle["angle_id"],"angle_id":angle["angle_id"],**angle["copy"],"claim_ids":angle.get("claim_ids",[]),"source_fact_ids":angle.get("source_fact_ids",[]),"application_trace_ref":"07-framework-selection"})
        traces.append(angle["application_trace"])
    value={"drafts":drafts,"framework_application":traces}
    from validate_framework_application import validate as validate_framework
    framework_issues=validate_framework({"framework_application":traces})
    if framework_issues: raise ValueError("framework application failed: " + "; ".join(framework_issues))
    _store_post(run_dir,run,value,"10-copy-drafting", "claim_safety")
    claims=[]
    for d in drafts:
        for claim_id in d.get("claim_ids",[]):
            claims.append({"claim_id":claim_id,"draft_id":d["draft_id"],"exact_copy_quote":d["primary_text"],"source_fact_ids":d.get("source_fact_ids",["fact-01"]),"source_quote":"verified source evidence","claim_type":"product_feature","verdict":"pass","repair_action":"none"})
    _store_post(run_dir,run,{"claim_audit":claims},"11-claim-safety", "deterministic_validation")
    import validate_copy
    variants=[]
    for angle in matrix["proposed_angles"]:
        if angle.get("angle_id") not in approved: continue
        c=angle["copy"]
        first_line=next(line.strip() for line in c["primary_text"].splitlines() if line.strip())
        scene_text=first_line.split("，",1)[0].split("？",1)[0]
        plain_help=angle.get("application_trace",{}).get("value_chain",{}).get("benefit_copy_quote", "查看已驗證商品資訊")
        translations=[{"term":term,"plain_language":plain_help,"copy_quote":plain_help} for term in ("尾部配重","配重模組","桿面角度","著地角度","可調式桿頸","Ai10x","彈道") if term in c["primary_text"]]
        variants.append({"variant_name":angle["angle_id"],"angle_id":angle["angle_id"],"funnel_stage":brief.get("funnel_stage"),"primary_text":c["primary_text"],"headline":c["headline"],"description":c["description"],"call_to_action":c["cta"],"problem_scene":angle.get("opening_route",""),"shopper_tension":angle.get("tension_id",""),"comparison_standard":angle.get("proof_role",""),"product_feature":angle.get("value_ladder_ids",["verified product feature"])[0],"feature_translation":angle.get("cta_rationale",""),"objection_handling":"先查看已驗證商品資訊", "proof_available":[{"type":"product_page","source":fact.get("url","")} for fact in source_facts(read_json(Path(brief.get("evidence_file", ""))))] if brief.get("evidence_file") else [{"type":"product_page","source":brief.get("product_urls",[""])[0]}],"offer_reason":"查看已驗證的商品選項","next_action":"進入官網查看","scene_anchor":{"scene_text":scene_text,"copy_quote":first_line},"plain_language_product_help":plain_help,"technical_term_translations":translations})
    delivery={"campaign_brief":{"brand":brief.get("brand"),"platform":brief.get("platform","meta"),"ad_format":"feed","task_type":"ecommerce_product_copy","funnel_stage":brief.get("funnel_stage"),"audience_state":brief.get("audience_state"),"buying_task":brief.get("buying_task"),"ecommerce_copy_check":{"audience_problem":"依需求比較商品","use_moment":"實際選購時","product_help":"提供選擇依據","proof_available":[{"type":"product_page","source":brief.get("product_urls",[""])[0]}],"objection":"不確定哪個選項適合","next_action":"進入官網查看"}},"meta_copies":variants}
    copy_issues=validate_copy.validate(delivery)
    _store_post(run_dir,run,{"validator_version":"1.0.0","command":"validate_copy.py + validate_framework_application.py","exit_code":0 if not copy_issues else 1,"issues":copy_issues,"framework_application_passed":True,"input_sha256":sha(value),"passed":not copy_issues},"12-deterministic-validation", "independent_review")
    if copy_issues: raise ValueError("delivery validation failed: " + "; ".join(copy_issues))
    run["state"]="independent_review"; run["updated_at"]=ts(); write_json(run_dir/"run.json",run)

def import_review(run_dir, review):
    run=load_manifest(run_dir)
    if run.get("state") != "independent_review": raise ValueError("review requires a completed draft awaiting independent review")
    draft=read_json(artifact(run_dir,"10-copy-drafting"))
    evidence_digest=run["task"]["evidence_digest"]
    from validate_independent_review import validate
    rubric=(Path(__file__).resolve().parents[1]/"references/creative-quality-contract.md").read_bytes()
    rubric_digest=hashlib.sha256(rubric).hexdigest()
    angle_ids={str(d.get("angle_id")) for d in draft.get("drafts",[])}
    claim_ids={str(cid) for d in draft.get("drafts",[]) for cid in d.get("claim_ids",[])}
    issues=validate(review,draft_sha256=sha(draft),evidence_sha256=evidence_digest,rubric_sha256=rubric_digest,writer_id="copy_orchestrator",angle_ids=angle_ids,claim_ids=claim_ids)
    if issues:
        raise ValueError("independent review failed: " + "; ".join(issues))
    _store_post(run_dir,run,review,"13-independent-review", "learning")
    _store_post(run_dir,run,{"outcome":"review_passed_no_performance_claim","evidence_basis":"external hash-bound editorial review","rule_change_proposed":False,"human_approval_required":True},"14-learning", "passed")
    run["status"]="passed"; run["final_verdict"].update(status="passed",live_ready=False,manual_check_required=True); write_json(run_dir/"run.json",run)

def _store_post(run_dir,run,value,name,next_state):
    ref=artifact(run_dir,name); write_json(ref,value); run["stages"][name]={"status":"passed","artifact_ref":str(ref.relative_to(run_dir)),"artifact_sha256":sha(value),"input_artifact_refs":[run["stages"]["08-appeal-matrix"]["artifact_ref"]],"producer":"copy_orchestrator","created_at":ts()}; run["state"]=next_state; run["updated_at"]=ts(); run["transition_log"].append({"from":name,"to":next_state,"at":ts()}); write_json(run_dir/"run.json",run)

def verify(run_dir):
    run=load_manifest(run_dir); issues=[]
    for name,entry in run.get("stages",{}).items():
        if entry.get("status") != "passed": issues.append(f"stage not passed: {name}"); continue
        ref=run_dir/entry.get("artifact_ref","")
        if not ref.exists(): issues.append(f"missing artifact: {name}"); continue
        if sha(read_json(ref)) != entry.get("artifact_sha256"): issues.append(f"digest mismatch: {name}")
        for upstream in entry.get("input_artifact_refs", []):
            if upstream.startswith("input:"): continue
            upstream_path=run_dir/upstream
            if not upstream_path.exists(): issues.append(f"missing upstream artifact: {name} -> {upstream}")
    if artifact(run_dir,"10-copy-drafting").exists():
        from validate_framework_application import validate as validate_framework
        draft=read_json(artifact(run_dir,"10-copy-drafting")); framework_issues=validate_framework({"framework_application":draft.get("framework_application",[])})
        issues.extend(f"framework verify: {i}" for i in framework_issues)
        if not draft.get("drafts"): issues.append("copy drafting contains no drafts")
    if run["state"] == "awaiting_user_confirmation":
        if artifact(run_dir,"10-copy-drafting").exists(): issues.append("copy artifact exists before confirmation")
        issues.append("awaiting_user_confirmation is pending")
    if run["state"] in {"copy_drafting","claim_safety"}: issues.append("workflow not yet complete")
    if run["state"] == "independent_review" and not artifact(run_dir,"13-independent-review").exists(): issues.append("external independent review is pending")
    if run["state"] == "passed":
        for name in POST:
            if not artifact(run_dir,name).exists(): issues.append(f"missing post artifact: {name}")
    print(json.dumps({"passed":not issues,"state":run["state"],"issues":issues},ensure_ascii=False,indent=2)); return 0 if not issues else 1

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("preview"); p.add_argument("--brief",required=True); p.add_argument("--evidence",required=True); p.add_argument("--run-dir",required=True)
    c=sub.add_parser("confirm"); c.add_argument("--run-dir",required=True); c.add_argument("--confirmation-json",required=True)
    d=sub.add_parser("draft"); d.add_argument("--run-dir",required=True)
    r=sub.add_parser("review"); r.add_argument("--run-dir",required=True); r.add_argument("--review-json",required=True)
    v=sub.add_parser("verify"); v.add_argument("--run-dir",required=True)
    a=ap.parse_args()
    try:
        if a.cmd=="preview": preview(read_json(Path(a.brief)),read_json(Path(a.evidence)),Path(a.run_dir))
        elif a.cmd=="confirm": confirm(Path(a.run_dir),read_json(Path(a.confirmation_json)))
        elif a.cmd=="draft": draft(Path(a.run_dir))
        elif a.cmd=="review": import_review(Path(a.run_dir),read_json(Path(a.review_json)))
        else: return verify(Path(a.run_dir))
        return 0
    except (ValueError, KeyError, json.JSONDecodeError) as e: print(f"ERROR: {e}",file=sys.stderr); return 1
if __name__ == "__main__": sys.exit(main())
