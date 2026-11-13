"""Validate semantic review coverage and provenance fields for a draft bundle."""
from typing import Any


def validate(review: dict[str, Any], *, draft_sha256: str, evidence_sha256: str,
             rubric_sha256: str, writer_id: str, angle_ids: set[str],
             claim_ids: set[str]) -> list[str]:
    issues = []
    required = ("review_id", "reviewer_id", "producer_id", "reviewed_draft_sha256",
                "reviewed_evidence_sha256", "rubric_sha256", "overall_verdict",
                "used_writer_self_score", "angle_reviews")
    for key in required:
        if review.get(key) in (None, "", []):
            issues.append(f"missing review field: {key}")
    if review.get("reviewer_id") == writer_id or review.get("producer_id") == writer_id:
        issues.append("writer cannot review their own draft")
    if review.get("used_writer_self_score") is not False:
        issues.append("writer self-score cannot be used")
    for key, expected, label in (("reviewed_draft_sha256", draft_sha256, "draft"),
                                 ("reviewed_evidence_sha256", evidence_sha256, "evidence"),
                                 ("rubric_sha256", rubric_sha256, "rubric")):
        if review.get(key) != expected:
            issues.append(f"review {label} hash mismatch")
    if review.get("overall_verdict") != "pass":
        issues.append("overall review verdict is not pass")
    rows = review.get("angle_reviews", [])
    found_angles = {str(row.get("angle_id", "")) for row in rows if isinstance(row, dict)}
    if found_angles != angle_ids:
        issues.append("review must cover exactly the drafted angles")
    found_claims = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        angle_id = str(row.get("angle_id", ""))
        for field in ("opening", "buyer_payoff", "distinctness", "evidence_boundary", "field_fit"):
            verdict = row.get(field, {})
            if not isinstance(verdict, dict) or verdict.get("verdict") != "pass" or not str(verdict.get("rationale", "")).strip():
                issues.append(f"{angle_id}: {field} did not pass with rationale")
        for claim in row.get("claim_verdicts", []):
            if not isinstance(claim, dict):
                continue
            cid = str(claim.get("claim_id", "")); found_claims.add(cid)
            if claim.get("verdict") != "pass" or not str(claim.get("rationale", "")).strip():
                issues.append(f"{cid}: claim review did not pass with rationale")
    if found_claims != claim_ids:
        issues.append("review must cover exactly the drafted claims")
    return issues
