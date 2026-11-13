# copywrite-ad-agent

Evidence-grounded workflows for ecommerce advertising copy and Meta creative briefs.

## Status and entry points

- **Installed Skill path:** `/Users/boyi/.codex/skills/copywrite-ad-agent/` (the directory containing this file).
- **Release identity:** this installed snapshot has no verified release tag. Treat the path above as the active source; do not call it an uninstalled candidate.
- **Agent invocation:** `copywrite-ad-agent`, configured in `agents/openai.yaml`.
- **Normative workflow:** [SKILL.md](SKILL.md). It controls task routing, required evidence, approval boundaries, and delivery gates. This README is navigation and maintenance documentation only.

A separately stored, dated candidate or backup is not active unless it is installed at the canonical path and verified. See [release and rollback](references/candidate-release-and-rollback.md).

## Find the right material by task

| Task | Start here | Supporting material |
|---|---|---|
| Ecommerce ad copy | [SKILL.md](SKILL.md), then [ecommerce playbook](knowledge/ecommerce-copywriting-playbook.md) | [angle planning](references/creative-angle-matrix.md), funnel and platform rules under `references/copy-knowledge-pack/`, [quality contract](references/creative-quality-contract.md), [validation contract](references/validation-contract.md) |
| Meta ad copy or revision | [SKILL.md](SKILL.md) | [Meta conversion review loop](references/meta-conversion-review-loop.md), [Meta formats](references/meta-formats.md), funnel/platform rules in `references/copy-knowledge-pack/` |
| Brand-specific copy | The brand file in `references/brands/` | Relevant brand failure patterns in `knowledge/`; current product and campaign evidence still takes precedence |
| Product research / USP evidence | [Product research loop](references/product-research-loop.md) | [Verification rubric](references/product-research-verification-rubric.md), `schemas/product-research-output.schema.json`, `scripts/validate_product_research.py` |
| Creative brief for Google Sheets | The brief route in [SKILL.md](SKILL.md) | [Brief review adaptation](references/creative-brief-review-adaptation.md), the two `creative-brief-*.schema.json` files, `scripts/validate_creative_brief.py`; load the Google Sheets Skill only at the authorized write stage |
| Google RSA copy | [Google RSA guidance](references/google-rsa.md) | Platform constraints in `references/copy-knowledge-pack/08_platform_adaptation_rules.md`; delivery validation in `scripts/validate_copy.py` |
| Workflow implementation or repair | [orchestrator](scripts/copy_orchestrator.py) and [run contract](schemas/copy-run.schema.json) | Matching tests in `tests/`; do not bypass the orchestrator for production runs |

## Source-of-truth map

- `SKILL.md` is the only top-level workflow router.
- `references/creative-angle-matrix.md` is authoritative for angle identity, distinctness, counts, and confirmation. `references/orthogonal-matrix-logic.md` is a compatibility guide only; it points back to the angle matrix and does not define another workflow or require 24 angles.
- `references/brands/<brand>.md` is the maintained brand profile. Brand-specific files in `knowledge/` describe failure patterns or historical learning; they do not replace the profile or current evidence. `references/ash-golf.md` is a compatibility redirect to `references/brands/ash-golf.md`.
- `references/copy-knowledge-pack/` is a modular reference library. Load only the sections selected by `SKILL.md`; its examples and background do not override current product, campaign, or market evidence.
- `schemas/` defines machine-readable payloads; `scripts/` implements deterministic workflow and validation; `templates/` provides starting records; `tests/` protects expected behavior.

## Verification

Run from this directory:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
for f in schemas/*.json; do python3 -m json.tool "$f" >/dev/null || exit 1; done
python3 scripts/review_quality_upgrade.py standards
python3 scripts/review_quality_upgrade.py spec
```

Expected result: unit tests and compilation finish successfully; each JSON schema parses; both review commands report `"verdict": "pass"`. Standards Review checks workflow boundaries and source-of-truth rules. Spec Review checks the documented quality requirements and regression-test presence.

These checks validate local structure and regression behavior. They do **not** establish that a particular product claim is true, that a human reviewer is independent, that copy will perform, that a live ad is policy-approved, or that anything has been published. For a specific copy run, follow the per-run gates and verification in [SKILL.md](SKILL.md).

## Folder map

- `agents/` — invocation metadata.
- `knowledge/` — ecommerce guidance and brand-specific failure-pattern learning.
- `references/` — workflow details, brand profiles, platform guidance, and quality contracts.
- `schemas/` — machine-readable data contracts.
- `scripts/` — orchestration, research, and validators.
- `templates/` — starter run records.
- `tests/` — regression tests and fixtures.
