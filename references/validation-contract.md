# Validation JSON Contract

This document describes the delivery payload only. Passing `scripts/validate_copy.py` does not mean the workflow completed. The workflow contract and state transitions live in `schemas/copy-run.schema.json` and are checked by `scripts/copy_run.py validate`; both gates are required.

Save generated assets in this shape before running `scripts/validate_copy.py`:

```json
{
  "campaign_brief": {
    "brand": "ASH GOLF",
    "platform": "meta",
    "ad_format": "collection",
    "audience": {
      "identity": "具有固定下場習慣的球友",
      "situation": "夏季下場",
      "dissatisfaction": "不想穿得制式",
      "purchase_motivation": "兼顧活動需求與造型",
      "product_expectation": "看出值得點進去的理由"
    },
    "usp_fed": [{"feature": "source-backed feature", "evidence": "source pointer", "desire": "concrete result", "purchase_reason": "reason to click"}],
    "reason_to_act_now": ["Campaign ends on 6/18"],
    "asset_visible_text": ["618 limited offer", "Selected items up to 60% off"],
    "phrases_to_avoid": ["custom banned phrase"]
  },
  "meta_copies": [
    {
      "variant_name": "A",
      "angle_id": "angle-01",
      "primary_text": "...",
      "headline": "...",
      "description": "...",
      "call_to_action": "Shop now",
      "destination_button_text": "Browse the edit"
    }
  ],
  "google_rsa": {
    "headlines": [],
    "descriptions": []
  }
}
```

The validator checks deterministic constraints and evidence guards. For Meta, it also blocks Boyi's default banned sentence structures, consumer-facing commentary about specifications or professional terms, and any exact phrase listed in `campaign_brief.phrases_to_avoid`. For ASH GOLF Meta output, it additionally requires the audience and FED fields and rejects recorded weak opening lines. It does not replace human review of voice, factual interpretation, or likely ad performance.

## Ecommerce product-copy extension

When `campaign_brief.task_type` is `ecommerce_product_copy`, add:

```json
{
  "ecommerce_copy_check": {
    "audience_problem": "The concrete shopper problem or desired outcome.",
    "use_moment": "When the product becomes relevant.",
    "product_help": "A source-backed practical result.",
    "proof_available": [{"type": "product_page", "source": "https://example.com/product"}],
    "objection": "What could stop the click or purchase.",
    "next_action": "The product, collection, guide, or offer to open next."
  }
}
```

The validator checks that this bridge and at least one evidence pointer exist. It does not decide whether a story, review, number, or product claim is true; the source and editorial claim-safety review remain required.

## Funnel-stage contract

For ecommerce outputs, `campaign_brief.funnel_stage` is required and must be `TOFU`, `MOFU`, or `BOFU`. The brief must also provide `audience_state` and `buying_task`. Each Meta variant must repeat the stage and provide the matching evidence map:

```json
{
  "funnel_stage": "TOFU | MOFU | BOFU",
  "stage_evidence": {
    "TOFU": ["problem_scene", "hook_tension", "initial_product_help", "soft_next_action"],
    "MOFU": ["shopper_tension", "comparison_standard", "product_feature", "feature_translation", "objection_handling", "proof_available", "offer_reason", "next_action"],
    "BOFU": ["known_product_or_intent", "decision_blocker", "verified_offer", "risk_reducer", "reason_to_act_now", "purchase_action"]
  }
}
```

The validator also requires at least three non-empty, scanable primary-text lines or blocks for staged ecommerce copy. This is a minimum depth check, not a maximum length rule: mobile formatting still requires short paragraphs, while funnel stage determines the required persuasion depth.

It also requires `scene_anchor.scene_text` and `scene_anchor.copy_quote` to occur in `primary_text`, plus `plain_language_product_help` to occur in `primary_text`. Technical terms retained in the copy must be listed in `technical_term_translations` with a non-identical plain-language translation and an in-copy quote. The rule is not a ban on technical terms; it prevents jargon from replacing explanation.

## Ecommerce Collection-ad extension

When `campaign_brief.task_type` is `ecommerce_collection_ad`, add:

```json
{
  "collection_ad_evidence": {
    "asset_to_products": [{
      "asset_id": "creative-01",
      "product_anchor": "official product name or verified category",
      "source_url": "https://example.com/collection-or-product",
      "source_excerpt": "short source-backed text"
    }],
    "conversion_lever": {
      "type": "offer | product_difference | use_case | verified_service",
      "source": "URL or approved brief pointer",
      "evidence": "short supporting text"
    },
    "shopper_tension": "the concrete hesitation or problem",
    "decision_to_make": "the specific choice the Collection helps make",
    "angle_groups": [{
      "angle_id": "angle-01",
      "product_anchor": "official product name or verified category",
      "source_evidence": [{"source_url": "https://...", "locator": "page section or line", "excerpt": "..."}],
      "shopper_problem": "concrete hesitation or use friction",
      "use_moment": "when the item matters",
      "product_feature": "only source-backed or visibly proven detail",
      "felt_outcome": "plain-language outcome without unsupported performance claims",
      "purchase_reason": "specific reason to open or buy",
      "brand_removed_copy": "copy with the brand name removed",
      "could_fit_another_brand": false,
      "distinct_from_other_angles": true
    }]
  }
}
```

The validator blocks a missing evidence object, missing angle group, missing source evidence, `could_fit_another_brand: true`, and copy whose primary text and headline do not name its mapped product or category anchor. It cannot determine whether a claim is persuasive; the independent editorial checker must reject generic-brand and navigation-only copy.
