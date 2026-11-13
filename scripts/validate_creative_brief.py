#!/usr/bin/env python3
"""Fail-closed schema, count, evidence-reference, and review gate before Sheet writes."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STAGES = ("TOFU", "MOFU", "BOFU")
RUBRIC = ROOT / "references" / "meta-creative-reviewer-v0.4.md"


def canonical_sha256(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def schema_errors(value: object, schema_path: Path, label: str) -> list[str]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return ["jsonschema is required; install requirements-brief-validation.txt before validation"]
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        return [f"{label}: {e.message} at {list(e.absolute_path)}" for e in validator.iter_errors(value)]
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load {label} schema: {exc}"]


def validate(brief_set: object, review: object) -> list[str]:
    errors = schema_errors(brief_set, ROOT / "schemas" / "creative-brief-set.schema.json", "brief_set")
    errors.extend(schema_errors(review, ROOT / "schemas" / "creative-brief-review.schema.json", "review"))
    if errors:
        return errors
    assert isinstance(brief_set, dict) and isinstance(review, dict)
    if brief_set["request"]["platform"].strip().casefold() != "meta":
        errors.append("bundled meta-creative-reviewer rubric supports Meta briefs only")
    counts = brief_set["request"]["requested_counts"]
    briefs = brief_set["briefs"]
    actual = {stage: sum(item["funnel_stage"] == stage for item in briefs) for stage in STAGES}
    if counts != actual:
        errors.append(f"funnel counts mismatch: requested {counts}; received {actual}")
    evidence_by_id = {item["evidence_id"]: item for item in brief_set["source_evidence"]}
    brief_ids = [item["brief_id"] for item in briefs]
    if len(set(brief_ids)) != len(brief_ids):
        errors.append("brief_id values must be unique")
    evidence_ids = list(evidence_by_id)
    if len(evidence_by_id) != len(brief_set["source_evidence"]):
        errors.append("evidence_id values must be unique")
    for item in briefs:
        for ref in item["source_refs"]:
            if ref not in evidence_by_id:
                errors.append(f"{item['brief_id']} has unresolved source reference: {ref}")
        for claim in item["claim_evidence"]:
            source = evidence_by_id.get(claim["evidence_id"])
            if source is None:
                errors.append(f"{item['brief_id']} claim points to unresolved evidence: {claim['evidence_id']}")
            elif source["evidence_class"] not in {"OBSERVED", "SUPPORTED_BY_BRIEF"}:
                errors.append(f"{item['brief_id']} claim uses non-verified evidence class: {claim['evidence_id']}")
    if not RUBRIC.is_file():
        errors.append("bundled reviewer rubric is missing")
    else:
        rubric_digest = hashlib.sha256(RUBRIC.read_bytes()).hexdigest()
        if review["reviewer_provenance"]["rubric_sha256"] != rubric_digest:
            errors.append("review did not bind to the bundled v0.4 rubric")
    if review["reviewed_brief_set_sha256"] != canonical_sha256(brief_set):
        errors.append("review digest does not match the exact brief_set")
    if [item["brief_id"] for item in review["brief_reviews"]] != brief_ids:
        errors.append("review must cover every brief exactly once and in the same order")
    if review["decision"] != "PASS":
        errors.append("review decision is not PASS")
    for item in review["brief_reviews"]:
        if item["verdict"] != "PASS" or item["blocking_findings"]:
            errors.append(f"{item['brief_id']} is not individually review-passed")
        for criterion, result in item["criteria"].items():
            if result["verdict"] != "PASS":
                errors.append(f"{item['brief_id']} criterion {criterion} is not PASS")
    batch = review["batch_review"]
    if batch["verdict"] != "PASS" or batch["blocking_findings"]:
        errors.append("batch review is not PASS")
    for criterion in ("batch_coverage", "similarity_check"):
        if batch[criterion]["verdict"] != "PASS":
            errors.append(f"batch criterion {criterion} is not PASS")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief-set", required=True, type=Path)
    parser.add_argument("--review", required=True, type=Path)
    args = parser.parse_args()
    try:
        brief_set: Any = json.loads(args.brief_set.read_text(encoding="utf-8"))
        review: Any = json.loads(args.review.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"SHEET_WRITE_BLOCKED: cannot read valid JSON artifacts: {exc}", file=sys.stderr)
        return 2
    try:
        errors = validate(brief_set, review)
    except (KeyError, TypeError, ValueError) as exc:
        print(f"SHEET_WRITE_BLOCKED: invalid artifact structure: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("SHEET_WRITE_BLOCKED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"SHEET_WRITE_ALLOWED brief_set_sha256={canonical_sha256(brief_set)} rows={len(brief_set['briefs'])}")
    print("Gate scope: schemas, counts, evidence links, rubric/digest binding, and review attestations. It does not authenticate reviewer identity or independently judge semantic quality.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
