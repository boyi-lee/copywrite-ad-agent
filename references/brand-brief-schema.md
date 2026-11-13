# Universal Brand Brief Schema

Use this schema to normalize any brand, company, product, or campaign before writing copy.

## Required When Available

- Brand name
- Product/service/category
- Campaign objective
- Platform and ad format
- Funnel stage or audience awareness
- Offer, if any
- Landing page, product page, asset, or draft source
- Visible creative text
- Required terms
- Prohibited claims or phrasing
- Market and language

## Brand Profile Fields

Use these only when supplied by the user, found in a matching repo profile, or clearly supported by the source.

```yaml
brand_name:
category:
positioning:
audience:
voice:
proof_points:
product_or_service_strengths:
common_use_cases:
conversion_barriers:
competitors_or_alternatives:
offer_rules:
compliance_or_claim_guardrails:
phrases_to_use:
phrases_to_avoid:
```

## Ecommerce Product-Copy Extension

Use this extension for ecommerce product, collection, or promotion copy. These fields make the product-to-buyer bridge explicit; they do not create product claims.

```yaml
task_type: ecommerce_product_copy
ecommerce_copy_check:
  audience_problem: What the named shopper wants solved or avoided.
  use_moment: The concrete moment when the product becomes relevant.
  product_help: The source-backed practical result the shopper can understand.
  proof_available:
    - type: product_page | supplied_creative | verified_review | verified_campaign_term
      source: URL, asset identifier, or supplied evidence pointer
  objection: The remaining hesitation before clicking or buying.
  next_action: The specific product, collection, guide, or offer route to open.
```

Rules:

- A feature must have a use moment before it becomes a leading benefit.
- `proof_available` is an evidence inventory, not permission to invent testimonials, numbers, popularity, or technical claims.
- Choose story, product explanation, comparison, or proof according to funnel stage and available evidence. Do not force a story or social proof when none is verified.
- If the proof source is unavailable, mark the run `blocked` or use neutral, source-backed browsing logic; do not fill the gap with a claim.

## Universal Rule

A missing brand profile does not block the task. It only limits how specific the brand voice can be.

If no brand profile exists:

- Use the current brief and source facts.
- Use category-appropriate but neutral copy.
- Avoid invented personality, heritage, awards, audience stereotypes, or claims.
- Flag brand voice as an evidence gap when relevant.

## Brand Context Priority

1. Current user instructions.
2. Supplied campaign and product facts.
3. Matching brand profile selected or supplied for this task.
4. General category logic.
5. General copywriting principles.

Never use an unrelated sample profile to fill missing facts.
