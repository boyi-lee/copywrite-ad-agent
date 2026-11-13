#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

REQUIRED={"PAS":["problem","agitate","solve"],"TIPS":["tempt","influence","persuade","sell"],"AIDAS":["attention","interest","desire","action","satisfaction"],"4R":["repeat","remind","reassure","relieve"]}

def validate(payload):
    issues=[]
    for trace in payload.get("framework_application", payload if isinstance(payload,list) else []):
        framework=trace.get("selected_message_framework"); steps=trace.get("application_steps",[]); by_name={s.get("step"):s for s in steps}
        if framework not in REQUIRED: issues.append(f"unknown message framework: {framework}"); continue
        for step in REQUIRED[framework]:
            item=by_name.get(step)
            if not item or (item.get("not_used") is not True and (not item.get("copy_quote") or not item.get("copy_block_id"))): issues.append(f"{framework} missing applied step: {step}")
            elif item.get("not_used") is True and not item.get("reason"): issues.append(f"{framework} unused step needs reason: {step}")
            elif item.get("not_used") is not True and item.get("copy_quote") not in trace.get("final_draft_text",""): issues.append(f"{framework} quote not found in draft: {step}")
        vf=trace.get("selected_value_framework")
        chain=trace.get("value_chain",{})
        if vf=="FEB" and not all(chain.get(k) for k in ("feature_fact_id","evidence_quote","benefit_copy_quote")): issues.append("FEB requires feature, evidence, benefit chain")
        if vf=="FEB" and chain.get("benefit_copy_quote") and chain.get("benefit_copy_quote") not in trace.get("final_draft_text",""): issues.append("FEB benefit quote not found in draft")
        if vf=="FAB" and not all(chain.get(k) for k in ("feature_fact_id","advantage_copy_quote","benefit_copy_quote")): issues.append("FAB requires feature, advantage, benefit chain")
        if vf=="FAB" and chain.get("benefit_copy_quote") and chain.get("benefit_copy_quote") not in trace.get("final_draft_text",""): issues.append("FAB benefit quote not found in draft")
    return issues

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("payload"); args=ap.parse_args(); issues=validate(json.loads(Path(args.payload).read_text())); print(json.dumps({"passed":not issues,"issues":issues},ensure_ascii=False,indent=2)); return 0 if not issues else 1
if __name__=="__main__": sys.exit(main())
