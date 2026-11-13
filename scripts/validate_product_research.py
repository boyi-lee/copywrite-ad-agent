#!/usr/bin/env python3
"""Deterministic checker for Copywrite Product Research artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


TERMINAL_STATES = {"passed", "failed", "blocked", "escalated"}
CRAWL_STATES = {"success", "failed", "blocked"}
CLASSIFICATIONS = {"verified_fact", "selling_point", "usp_candidate", "verified_usp"}
VOLATILE_FIELDS = {
    "price",
    "price_currency",
    "availability",
    "price_valid_until",
    "rating_value",
    "review_count",
    "discount",
    "deadline",
    "stock",
    "shipping",
}


def is_http_url(value: Any) -> bool:
    parsed = urlparse(str(value))
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def non_empty(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def validate(payload: dict[str, Any]) -> tuple[list[str], list[str]]:
    issues: list[str] = []
    blocked_reasons: list[str] = []
    required = {
        "schema_version",
        "run_id",
        "status",
        "started_at",
        "ended_at",
        "requested_urls",
        "products",
        "usp_candidates",
        "blocked_claims",
        "budgets",
        "live_ready",
        "manual_check_required",
    }
    missing = sorted(required - payload.keys())
    if missing:
        issues.append("Missing top-level fields: " + ", ".join(missing))
    if payload.get("schema_version") != "1.0.0":
        issues.append("schema_version must be 1.0.0.")
    if payload.get("status") not in TERMINAL_STATES:
        issues.append("Invalid terminal status.")
    if payload.get("live_ready") is not False:
        issues.append("L2 research artifacts must set live_ready to false.")
    if payload.get("manual_check_required") is not True:
        issues.append("L2 research artifacts must require manual review.")

    urls = payload.get("requested_urls", [])
    if not isinstance(urls, list) or not 1 <= len(urls) <= 20:
        issues.append("requested_urls must contain 1 to 20 URLs.")
        urls = []
    if len(urls) != len(set(urls)):
        issues.append("requested_urls contains duplicates.")
    for url in urls:
        if not is_http_url(url):
            issues.append(f"Invalid requested URL: {url}")

    products = payload.get("products", [])
    if not isinstance(products, list):
        issues.append("products must be an array.")
        products = []
    product_urls = [item.get("requested_url") for item in products if isinstance(item, dict)]
    if sorted(product_urls) != sorted(urls):
        issues.append("Every requested URL must have exactly one product result.")

    evidence_by_id: dict[str, dict[str, Any]] = {}
    successful_urls: set[str] = set()
    for index, product in enumerate(products, start=1):
        if not isinstance(product, dict):
            issues.append(f"Product {index} must be an object.")
            continue
        label = str(product.get("requested_url") or index)
        crawl_status = product.get("crawl_status")
        if crawl_status not in CRAWL_STATES:
            issues.append(f"{label}: invalid crawl_status.")
        if not is_http_url(product.get("source_url")):
            issues.append(f"{label}: source_url must be HTTP(S).")
        facts = product.get("facts", [])
        if not isinstance(facts, list):
            issues.append(f"{label}: facts must be an array.")
            facts = []
        if crawl_status == "success":
            successful_urls.add(label)
            if not product.get("raw_markdown_path"):
                issues.append(f"{label}: successful crawl lacks raw_markdown_path.")
            if not facts:
                blocked_reasons.append(f"{label}: no normalized evidence; semantic extraction is required.")
        elif not product.get("error"):
            issues.append(f"{label}: failed or blocked crawl lacks an error message.")

        for fact_index, fact in enumerate(facts, start=1):
            if not isinstance(fact, dict):
                issues.append(f"{label}: fact {fact_index} must be an object.")
                continue
            required_fact = {
                "id",
                "field",
                "value",
                "source_url",
                "source_type",
                "source_locator",
                "evidence_text",
                "captured_at",
                "confidence",
            }
            missing_fact = sorted(required_fact - fact.keys())
            if missing_fact:
                issues.append(f"{label}: fact {fact_index} missing {', '.join(missing_fact)}.")
                continue
            evidence_id = str(fact["id"])
            if evidence_id in evidence_by_id:
                issues.append(f"Duplicate evidence id: {evidence_id}.")
            evidence_by_id[evidence_id] = fact
            if not is_http_url(fact["source_url"]):
                issues.append(f"{evidence_id}: invalid source_url.")
            for field in ("field", "value", "source_locator", "evidence_text", "captured_at"):
                if not non_empty(fact[field]):
                    issues.append(f"{evidence_id}: {field} is empty.")
            normalized_field = str(fact["field"]).lower()
            if normalized_field in VOLATILE_FIELDS and fact.get("volatile") is not True:
                issues.append(f"{evidence_id}: volatile field {normalized_field} is not marked volatile.")

    candidates = payload.get("usp_candidates", [])
    if not isinstance(candidates, list):
        issues.append("usp_candidates must be an array.")
        candidates = []
    candidate_products: set[str] = set()
    for index, candidate in enumerate(candidates, start=1):
        if not isinstance(candidate, dict):
            issues.append(f"USP candidate {index} must be an object.")
            continue
        product_url = str(candidate.get("product_url", ""))
        candidate_products.add(product_url)
        if product_url not in urls:
            issues.append(f"USP candidate {index}: product_url is not in requested_urls.")
        classification = candidate.get("classification")
        if classification not in CLASSIFICATIONS:
            issues.append(f"USP candidate {index}: invalid classification.")
        for field in ("feature", "functional_benefit", "use_case", "desire", "buying_reason", "confidence"):
            if not non_empty(candidate.get(field)):
                issues.append(f"USP candidate {index}: {field} is empty.")
        evidence_ids = candidate.get("evidence_ids", [])
        if not isinstance(evidence_ids, list) or not evidence_ids:
            issues.append(f"USP candidate {index}: evidence_ids is empty.")
            evidence_ids = []
        missing_ids = [item for item in evidence_ids if item not in evidence_by_id]
        if missing_ids:
            issues.append(f"USP candidate {index}: unknown evidence ids: {', '.join(missing_ids)}.")
        if classification == "verified_usp":
            source_urls = {
                evidence_by_id[item]["source_url"] for item in evidence_ids if item in evidence_by_id
            }
            if len(source_urls) < 2:
                issues.append(
                    f"USP candidate {index}: verified_usp requires comparison evidence from at least two source URLs."
                )

    missing_candidates = successful_urls - candidate_products
    if missing_candidates:
        blocked_reasons.append(
            "Successful products without USP/FED candidates: " + ", ".join(sorted(missing_candidates))
        )
    if any(product.get("crawl_status") != "success" for product in products if isinstance(product, dict)):
        blocked_reasons.append("One or more requested pages could not be successfully crawled.")

    budgets = payload.get("budgets", {})
    if not isinstance(budgets, dict):
        issues.append("budgets must be an object.")
    else:
        if budgets.get("max_attempts_per_url", 99) > 2:
            issues.append("max_attempts_per_url exceeds the fixed budget of 2.")
        if budgets.get("max_duration_seconds", 999) > 180:
            issues.append("max_duration_seconds exceeds the fixed budget of 180.")
        if budgets.get("max_concurrency", 99) > 4:
            issues.append("max_concurrency exceeds the fixed budget of 4.")
    if payload.get("status") == "passed" and (issues or blocked_reasons):
        issues.append("status cannot be passed while validation or blocking conditions remain.")
    return issues, blocked_reasons


def verdict(payload: dict[str, Any]) -> dict[str, Any]:
    issues, blocked_reasons = validate(payload)
    if issues:
        status = "FAIL"
    elif blocked_reasons:
        status = "BLOCKED"
    elif payload.get("status") == "passed":
        status = "PASS"
    else:
        status = "BLOCKED"
        blocked_reasons.append("Artifact is valid but its terminal status is not passed.")
    deductions = min(20, len(issues) * 2 + len(blocked_reasons) * 2)
    return {
        "status": status,
        "score": 20 - deductions,
        "failed_criteria": issues + blocked_reasons,
        "evidence": [str(payload.get("run_id", "")), *payload.get("requested_urls", [])],
        "retry_instruction": (
            "Repair only the listed validation failures within the existing budget."
            if issues
            else "Collect or supply the missing evidence; rewriting alone cannot resolve this block."
            if blocked_reasons
            else ""
        ),
        "human_review_required": True,
    }


def update_run_record(path: Path, result: dict[str, Any], verdict_path: Path | None) -> None:
    record = json.loads(path.read_text(encoding="utf-8"))
    status_map = {"PASS": "passed", "FAIL": "failed", "BLOCKED": "blocked"}
    record["ended_at"] = datetime.now(timezone.utc).isoformat()
    record["final_verdict"] = {
        "status": status_map[result["status"]],
        "score": result["score"],
        "failed_criteria": result["failed_criteria"],
        "human_review_required": result["human_review_required"],
    }
    record["unresolved_risks"] = list(result["failed_criteria"])
    artifacts = record.setdefault("artifacts", [])
    if verdict_path is not None and str(verdict_path) not in artifacts:
        artifacts.append(str(verdict_path))
    record["live_ready"] = False
    record["manual_check_required"] = True
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate product research evidence and loop state.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--write-verdict", type=Path)
    parser.add_argument("--update-run-record", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result = {
            "status": "FAIL",
            "score": 0,
            "failed_criteria": [f"Unable to read valid JSON: {exc}"],
            "evidence": [],
            "retry_instruction": "Provide a readable JSON artifact.",
            "human_review_required": True,
        }
    else:
        result = verdict(payload)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    print(rendered, end="")
    if args.write_verdict:
        args.write_verdict.write_text(rendered, encoding="utf-8")
    if args.update_run_record:
        try:
            update_run_record(args.update_run_record, result, args.write_verdict)
        except (OSError, json.JSONDecodeError, KeyError) as exc:
            print(f"Unable to update run record: {exc}", file=sys.stderr)
            return 1
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
