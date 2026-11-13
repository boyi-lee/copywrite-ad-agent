#!/usr/bin/env python3
"""Canonical, local-only workflow state machine for copywrite-ad-agent."""
from __future__ import annotations
import argparse, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

STAGES = ["intake", "product_research", "persona_hypothesis", "shopper_tension", "funnel_strategy", "motivation_strategy", "value_translation", "framework_selection", "appeal_matrix", "awaiting_user_confirmation", "copy_drafting", "claim_safety", "deterministic_validation", "independent_review", "learning"]
TERMINAL = {"passed", "blocked", "failed", "escalated"}

def now(): return datetime.now(timezone.utc).isoformat()
def digest(value): return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
def empty_stages(): return {s: {"name": s, "status": "pending", "started_at": None, "completed_at": None, "input_refs": [], "output_refs": [], "validator_refs": [], "failure_codes": [], "actor": "worker", "artifact_digest": ""} for s in STAGES}

def init_run(task: dict, run_id: str) -> dict:
    t = now()
    run = {"schema_version":"1.0.0", "run_id":run_id, "workflow_id":"copywrite-ad-agent", "workflow_version":"2.0.0", "state":"intake", "status":"in_progress", "created_at":t, "updated_at":t, "task":task, "stages":empty_stages(), "transition_log":[], "retry_budget":{"max_revisions":2,"used":0}, "final_verdict":{"status":"blocked","live_ready":False,"manual_check_required":True}}
    run["stages"]["intake"].update(status="passed", started_at=t, completed_at=t, actor="deterministic_runtime", artifact_digest=digest(task))
    run["transition_log"].append({"from":"intake","to":"product_research","at":t,"reason":"initialized"})
    run["state"]="product_research"
    return run

def _nonempty(value): return bool(value) and (not isinstance(value, (list, dict)) or len(value) > 0)
def validate_run(run: dict) -> list[str]:
    issues=[]; stages=run.get("stages", {}); task=run.get("task", {})
    if run.get("workflow_id") != "copywrite-ad-agent": issues.append("missing canonical workflow")
    required=["product_research","persona_hypothesis","shopper_tension","funnel_strategy","motivation_strategy","value_translation","framework_selection","appeal_matrix","awaiting_user_confirmation","copy_drafting","claim_safety","deterministic_validation","independent_review","learning"]
    for s in required:
        if stages.get(s, {}).get("status") != "passed": issues.append(f"stage not passed: {s}")
    conf=stages.get("awaiting_user_confirmation", {}).get("output", {})
    if conf.get("confirmation_status") != "confirmed": issues.append("awaiting_user_confirmation has not been confirmed")
    approved=set(conf.get("approved_angle_ids", [])); drafts=stages.get("copy_drafting", {}).get("output", {}).get("drafts", [])
    if drafts and any(d.get("angle_id") not in approved for d in drafts): issues.append("draft angle_id is not approved")
    angles=stages.get("appeal_matrix", {}).get("output", {}).get("proposed_angles", [])
    for left_index, left in enumerate(angles):
        for right in angles[left_index + 1:]:
            dimensions=("persona_ref", "use_moment", "jtbd_tension", "proof_role", "opening_route", "cta_rationale")
            changed=[field for field in dimensions if left.get(field) != right.get(field)]
            if len(changed) == 0: issues.append("appeal matrix pairwise non-overlap failed")
    research=stages.get("product_research", {}).get("output", {})
    if task.get("product_url") and not research.get("evidence_artifact_ref") and not research.get("source_provenance"): issues.append("product research is missing for product URL")
    claims=stages.get("claim_safety", {}).get("output", {}).get("claim_audit", [])
    if not claims: issues.append("claim safety claim_audit is missing")
    if any(c.get("verdict") != "pass" for c in claims): issues.append("claim safety has unpassed claims")
    review=stages.get("independent_review", {}).get("output", {})
    if review.get("overall_verdict") != "pass": issues.append("independent review is missing or not pass")
    if review.get("reviewer_type") in {"writer", "self"} or review.get("used_writer_self_score") is True: issues.append("writer self-review cannot substitute independent review")
    if stages.get("deterministic_validation", {}).get("output", {}).get("passed") is not True: issues.append("deterministic validation did not pass")
    learning=stages.get("learning", {}).get("output", {})
    if not learning or not _nonempty(learning.get("outcome")): issues.append("learning outcome is missing")
    if run.get("status") in {"blocked","failed","escalated"} or issues: return issues
    return issues

def advance(run: dict, stage: str, output: dict, actor="worker", status="passed") -> dict:
    if stage not in STAGES: raise ValueError(f"unknown stage: {stage}")
    if stage == "copy_drafting" and run.get("stages", {}).get("awaiting_user_confirmation", {}).get("output", {}).get("confirmation_status") != "confirmed":
        raise ValueError("confirmation gate: copy drafting is blocked until explicit confirmation")
    if run.get("state") != stage: raise ValueError(f"invalid transition: current state is {run.get('state')}, expected {stage}")
    if stage == "copy_drafting":
        conf=run["stages"]["awaiting_user_confirmation"].get("output", {})
        if conf.get("confirmation_status") != "confirmed": raise ValueError("confirmation gate: copy drafting is blocked until explicit confirmation")
        approved=set(conf.get("approved_angle_ids", []))
        if any(d.get("angle_id") not in approved for d in output.get("drafts", [])): raise ValueError("draft contains an unapproved angle")
        revision=int(output.get("revision", 0) or 0)
        if revision > int(run.get("retry_budget", {}).get("max_revisions", 2)):
            raise ValueError("retry budget exhausted: third revision is rejected")
        run.setdefault("retry_budget", {})["used"] = max(int(run.get("retry_budget", {}).get("used", 0)), revision)
    entry=run["stages"][stage]; t=now(); entry.update(status=status, started_at=entry.get("started_at") or t, completed_at=t, actor=actor, output=output, artifact_digest=digest(output))
    run["transition_log"].append({"from":stage,"to":STAGES[STAGES.index(stage)+1] if stage != STAGES[-1] else "passed","at":t,"reason":"stage completed","artifact_digest":entry["artifact_digest"]})
    if status != "passed": run["status"]=status; run["state"]=status; return run
    if stage == STAGES[-1]: run["state"]="passed"; run["status"]="passed"; run["final_verdict"].update(status="passed",live_ready=False,manual_check_required=True)
    else: run["state"]=STAGES[STAGES.index(stage)+1]
    run["updated_at"]=t; return run

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    i=sub.add_parser("init"); i.add_argument("--task-json",required=True); i.add_argument("--output",required=True); i.add_argument("--run-id",required=True)
    a=sub.add_parser("advance"); a.add_argument("run"); a.add_argument("stage"); a.add_argument("--output-json",required=True); a.add_argument("--actor",default="worker")
    v=sub.add_parser("validate"); v.add_argument("run")
    args=ap.parse_args()
    if args.cmd=="init": run=init_run(json.loads(Path(args.task_json).read_text()),args.run_id); Path(args.output).write_text(json.dumps(run,ensure_ascii=False,indent=2)+"\n"); return 0
    path=Path(args.run); run=json.loads(path.read_text())
    if args.cmd=="advance": run=advance(run,args.stage,json.loads(Path(args.output_json).read_text()),args.actor); path.write_text(json.dumps(run,ensure_ascii=False,indent=2)+"\n"); return 0
    issues=validate_run(run); print(json.dumps({"passed":not issues,"issues":issues},ensure_ascii=False,indent=2)); return 0 if not issues else 1
if __name__ == "__main__": sys.exit(main())
