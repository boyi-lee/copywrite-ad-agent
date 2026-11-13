# copywrite-ad-agent

[繁體中文（預設）](README.md) ｜ [English](README.en.md)

An evidence-first ecommerce copywriting Skill for Meta ad copy, creative briefs, product research, and copy review. It combines brand and product evidence with structured planning, deterministic checks, and independent review to produce traceable work.

## Download and install

Clone the repository into the Codex skills directory:

```bash
git clone https://github.com/boyi-lee/copywrite-ad-agent.git ~/.codex/skills/copywrite-ad-agent
```

Or select **Code → Download ZIP** on GitHub, extract it, and place the complete repository in `~/.codex/skills/copywrite-ad-agent/`. The repository root is the Skill root. Keep `SKILL.md`, `agents/`, `knowledge/`, `references/`, `schemas/`, `scripts/`, `templates/`, and `tests/` together.

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

## Marketing principles used

The Skill uses marketing principles as **analysis and planning tools**, selected for the task. It does not force every copy request into one formula.

| Principle area | Guide | How it is used |
|---|---|---|
| Audience intent and core copy principles | [Universal copywriting principles](references/copy-knowledge-pack/01_universal_copywriting_principles.md) | Start from audience intent, problems, or friction; connect product details to benefits and relevant outcomes; identify and address objections. |
| Persuasion and message frameworks | [Persuasion frameworks](references/copy-knowledge-pack/02_persuasion_frameworks.md), [message structures](references/copy-knowledge-pack/06_message_structure_patterns.md) | Includes TIPS, PAS, BAB, FAB, and objection-handling structures. These organize a message; they are not mandatory templates. |
| Audience motivation and psychology | [Audience intent and psychology](references/copy-knowledge-pack/03_audience_intent_and_psychology.md), [creative angle matrix](references/creative-angle-matrix.md) | Explore buying motivations, use situations, shopper tensions, desired progress, and distinct reasons to buy. Audience inferences must remain labeled as hypotheses. |
| Value, offers, and USP | [Offer and value translation](references/copy-knowledge-pack/04_offer_and_value_translation.md), [USP translation rules](references/usp-translation-rules.md), [ecommerce playbook](knowledge/ecommerce-copywriting-playbook.md) | Connect features to functional benefits, use cases, possible felt outcomes, and buying reasons. Offers and urgency require current source support. |
| Attention and hooks | [Hook and attention patterns](references/copy-knowledge-pack/05_hook_and_attention_patterns.md) | Offers opening options such as questions, scenes, contrast, and warnings. Choose based on audience, creative, and evidence; do not exaggerate to attract attention. |
| Funnel and channel context | [Funnel copy rules](references/copy-knowledge-pack/07_funnel_copy_rules.md), [platform adaptation](references/copy-knowledge-pack/08_platform_adaptation_rules.md), [industry adaptation](references/copy-knowledge-pack/09_industry_adaptation_rules.md) | Adjust information depth, evidence, and next action to TOFU/MOFU/BOFU decision stages and platform placements. |
| Creative and field roles | [Meta format guide](references/meta-formats.md), [visual flow rules](references/visual-flow-rules.md) | Make the creative, primary text, headline, description, and CTA work as a sequence while reducing repetition. |

### Boundaries when applying these principles

- A framework label is not evidence and does not prove an angle works. The [creative angle matrix](references/creative-angle-matrix.md) defines distinctness by the actual buying reason.
- Audience, demand, and motivation inferences must remain hypotheses unless supported by customer data; do not present them as market facts.
- Product specifications, offers, stock, testimonials, comparisons, and performance claims must be checked against current sources. General marketing principles cannot replace missing product evidence.
- The knowledge pack provides cross-industry examples and candidate approaches. Assess their fit for the brand, product, platform, and regulatory context; frameworks may be left unused when they do not fit.

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

[繁體中文說明（預設）](README.md)
