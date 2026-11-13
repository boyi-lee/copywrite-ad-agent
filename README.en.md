# copywrite-ad-agent

[繁體中文](README.md) ｜ [English](README.en.md)

An evidence-first Skill for ecommerce ad copy, Meta creative briefs, product research, and copy review. It combines brand and product evidence with structured planning, deterministic checks, and independent review to produce traceable work.

## Download and install

Clone the repository directly into the Codex skills directory:

```bash
git clone https://github.com/boyi-lee/copywrite-ad-agent.git ~/.codex/skills/copywrite-ad-agent
```

Alternatively, choose **Code → Download ZIP** on GitHub, extract it, and place the whole repository in `~/.codex/skills/copywrite-ad-agent/`. The repository root is the Skill root. Keep `SKILL.md`, `agents/`, `knowledge/`, `references/`, `schemas/`, `scripts/`, `templates/`, and `tests/` together.

The Skill is named `copywrite-ad-agent`; invocation metadata is in `agents/openai.yaml`. Start with [SKILL.md](SKILL.md), the authoritative workflow and permission boundary.

## Workflows

### Ecommerce ad copy, rewrites, and reviews

1. Research current product, campaign, landing-page, and creative evidence.
2. Build audience and buying-angle hypotheses, keeping assumptions distinct from verified facts.
3. Preview the strategy and get angle confirmation when required by the task and workflow.
4. Draft copy for the selected angles, then check claims and platform/funnel requirements.
5. Send the current draft, evidence, and rubric through independent review; verify the review run is complete before delivery.

A strategy preview is not ready-to-paste copy. Passing workflow checks does not prove ad performance, platform policy approval, or publication.

### Meta creative briefs for Google Sheets

This is separate from finished ad copy. The Skill creates structured briefs, validates the complete set, and reviews it before any Sheet write. It writes only after the gate passes and the destination is authorized; afterward, it reads the rows back to verify the result.

## Sources and boundaries

- Current source evidence takes precedence over historical examples and brand learning.
- [creative-angle-matrix.md](references/creative-angle-matrix.md) is the single source of truth for angle identity, count handling, distinctness, and confirmation; compatibility documents should point back to it.
- `references/brands/` contains maintained brand profiles. `knowledge/` contains ecommerce guidance and brand-specific failure-pattern learning.
- Machine checks verify structure, hashes, and required fields; they do not independently establish claim truth or reviewer identity.
- This Skill does not publish ads, write to ad accounts, or write to Shopify.

This repository includes brand-specific profiles and historical learning modules. Review those materials and confirm they suit your organization and intended use before adopting them.

## Find the right material

| Task | Start here | Supporting files |
|---|---|---|
| Ecommerce ad copy | [SKILL.md](SKILL.md) | [Ecommerce playbook](knowledge/ecommerce-copywriting-playbook.md), [angle matrix](references/creative-angle-matrix.md), funnel/platform rules in `references/copy-knowledge-pack/`, [quality contract](references/creative-quality-contract.md), [validation contract](references/validation-contract.md) |
| Meta copy or revision | [SKILL.md](SKILL.md) | [Meta review loop](references/meta-conversion-review-loop.md), [format guide](references/meta-formats.md) |
| Brand-specific copy | `references/brands/<brand>.md` | Related failure-pattern notes in `knowledge/`; verify every claim against current evidence |
| Product research and USP evidence | [Product research loop](references/product-research-loop.md) | [Verification rubric](references/product-research-verification-rubric.md), `schemas/product-research-output.schema.json`, `scripts/validate_product_research.py` |
| Meta creative brief | Brief route in [SKILL.md](SKILL.md) | [Brief review rules](references/creative-brief-review-adaptation.md), `schemas/creative-brief-set.schema.json`, `schemas/creative-brief-review.schema.json`, `scripts/validate_creative_brief.py` |
| Google RSA copy | [Google RSA guidance](references/google-rsa.md) | `references/copy-knowledge-pack/08_platform_adaptation_rules.md`, `scripts/validate_copy.py` |
| Workflow maintenance | [Orchestrator](scripts/copy_orchestrator.py) | `schemas/`, `templates/`, and matching regression tests under `tests/` |

## Folder structure

```text
copywrite-ad-agent/
├── SKILL.md       # Workflow entry point and boundaries
├── agents/        # Skill invocation metadata
├── knowledge/     # Ecommerce guidance and brand learning
├── references/    # Brand, platform, research, and quality rules
├── schemas/       # Machine-readable contracts
├── scripts/       # Orchestration, research, and validators
├── templates/     # Starter run records
├── tests/         # Regression tests and fixtures
├── README.md      # Traditional Chinese default documentation
└── README.en.md   # English documentation
```

## Verify the package

Run these commands from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
for f in schemas/*.json; do python3 -m json.tool "$f" >/dev/null || exit 1; done
python3 scripts/review_quality_upgrade.py standards
python3 scripts/review_quality_upgrade.py spec
```

Expected: all unit tests pass, Python compilation succeeds, every schema parses as JSON, and both review commands report `"verdict": "pass"`. These checks cover local structure and regression expectations; they do not verify live product claims, ad performance, policy approval, or publication.

## Version and release status

This repository mirrors the currently installed Skill snapshot. The snapshot has no verified release tag, so it is an unversioned source copy, not a numbered stable release. See [release identity and rollback](references/candidate-release-and-rollback.md) before making or distributing a new release.

---

[繁體中文說明](README.md)
