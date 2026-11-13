#!/usr/bin/env python3
"""Run separate structural Standards Review or machine-spec review for this candidate."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def standards_review():
    skill = (ROOT / "SKILL.md").read_text()
    matrix = (ROOT / "references/creative-angle-matrix.md").read_text()
    checks = {
        "preserves_brief_sheet_route": "素材 brief only / Google Sheet brief" in skill,
        "preserves_copy_entrypoint": "scripts/copy_orchestrator.py" in skill,
        "one_angle_source_of_truth": "references/creative-angle-matrix.md" in skill and "orthogonal-matrix-logic.md" not in skill,
        "no_default_angle_quota": "Do not generate 24 combinations as a default" in matrix,
        "claims_not_performance_proof": "does not claim or predict ad performance" in (ROOT / "references/creative-quality-contract.md").read_text(),
        "external_review_import_required": "def import_review" in (ROOT / "scripts/copy_orchestrator.py").read_text(),
        "workflow_stops_for_external_review": 'run["state"]="independent_review"' in (ROOT / "scripts/copy_orchestrator.py").read_text(),
        "rollback_and_limitation_documented": (ROOT / "references/candidate-release-and-rollback.md").exists(),
    }
    return {"review_type":"Standards Review","verdict":"pass" if all(checks.values()) else "fail","checks":checks}


def spec_review():
    spec = json.loads((ROOT / "schemas/creative-quality-release-spec.json").read_text())
    checks = {}
    for row in spec["requirements"]:
        path = ROOT / row["file"]
        checks[row["id"]] = path.exists() and row["must_contain"] in path.read_text()
    tests = "\n".join(p.read_text() for p in (ROOT / "tests").glob("test_*.py"))
    for name in spec["required_tests"]:
        checks[f"test::{name}"] = name in tests
    limitation = ROOT / spec["limitation_document"]
    checks["limitation_document"] = limitation.exists()
    return {"review_type":"Spec Review","verdict":"pass" if all(checks.values()) else "fail","checks":checks}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("review", choices=["standards", "spec"])
    kind = parser.parse_args().review
    result = standards_review() if kind == "standards" else spec_review()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
