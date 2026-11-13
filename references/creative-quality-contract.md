# Creative Quality Contract

This is the editorial contract for copy and brief review. It complements product evidence and deterministic format checks; it does not claim or predict ad performance.

| Check | Pass condition | Block when |
|---|---|---|
| Opening | Within the requested format, the opening gives the intended audience a recognizable scene, tension, choice, useful payoff, or specific curiosity. | Generic brand language, feature label, or setup that gives the reader no reason to continue. |
| Buyer payoff | Each material feature is connected to a relevant use moment or decision, a supported practical or felt outcome, and a reason to inspect/buy. | Specs are listed without explaining what the buyer gains or can decide. |
| Distinctness | Each requested angle expresses a meaningfully different shopper motivation, desired progress, tension, or buying reason. | The differences are only hooks, wording, benefits adjectives, frameworks, CTAs, visuals, or persona labels. |
| Evidence boundary | Product, offer, endorsement, performance, and comparison claims match supplied source scope; audience assumptions remain labeled as hypotheses. | Missing evidence is presented as fact or used to invent urgency, outcomes, testimonials, or demand. |
| Field fit | Primary text, headline, description, and CTA each do a useful, non-duplicative job in the requested format. | User-requested fields are omitted or fields merely repeat one another/the visible asset. |

For user-requested opening lines, follow the exact count. When no count is specified, choose a concise opening for the placement and creative. Do not claim a universal Meta fold location, reading-time limit, or character threshold. A separate platform contract may specify a field limit only when tied to a verified platform requirement or an explicit local delivery profile.

## Review record

For every angle, record verdict and concrete rationale for `opening`, `buyer_payoff`, `distinctness`, `evidence_boundary`, and `field_fit`. Rationale must point to the actual copy and supplied evidence; generic praise does not pass. Keep semantic editorial findings separate from deterministic format findings. A reviewer must not receive writer self-scores or be represented as independent when the same producer created the draft and review.

The separate reviewer returns `schemas/independent-review.schema.json`, bound to the canonical draft digest, source-evidence digest, and SHA-256 of this rubric. Import it with `python3 scripts/copy_orchestrator.py review --run-dir <run-dir> --review-json <review.json>`. The production run stops at `independent_review`; it cannot reach `passed` until this import covers every draft angle and claim, uses a different reviewer/producer identity from `copy_orchestrator`, and all editorial verdicts pass with rationale.

## Regression cases

Use the synthetic cross-category cases in `tests/fixtures/creative-quality-cases.json`. At minimum, regression coverage must include: a feature dump that fails buyer payoff; vivid copy that adds an unsupported promise and fails evidence; distinct motivations that pass; superficial hook-only variants that fail distinctness; and a user-specified two-line opening that is honored without applying an invented universal line/character rule.

Ensure text meets WCAG AA 4.5
