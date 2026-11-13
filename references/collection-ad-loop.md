# Collection-Ad Loop

Use this procedure for Meta Collection or Instant Experience ads that lead to an ecommerce collection, campaign hub, or catalogue selection.

## Task layer

Record `objective`, `platform`, `ad_format`, `audience_stage`, `deliverables`, and `definition_of_done`. Do not infer that a purchase objective means retargeting or that a collection page means a product benefit.

## Required evidence

Complete `collection_ad_evidence` before drafting:

```json
{
  "asset_to_products": [{
    "asset_id": "creative-01",
    "product_anchor": "official product name or verified category",
    "source_url": "https://...",
    "source_excerpt": "page text or user-supplied proof",
    "role_in_asset": "what the shopper sees"
  }],
  "conversion_lever": {
    "type": "offer | product_difference | use_case | verified_service",
    "source": "URL, brief, or asset identifier",
    "evidence": "short supporting text"
  },
  "shopper_tension": "concrete reason the buyer hesitates",
  "decision_to_make": "specific choice the Collection helps make"
}
```

For every distinct angle, also require:

```json
{
  "angle_id": "angle-01",
  "product_anchor": "official product name or verified category",
  "source_evidence": [{"source_url": "https://...", "locator": "line or page section", "excerpt": "..."}],
  "shopper_problem": "concrete hesitation or use friction",
  "use_moment": "when the item matters",
  "product_feature": "only what the source states or visibly proves",
  "felt_outcome": "plain-language result without unsupported performance claims",
  "purchase_reason": "why this product/category is worth opening now",
  "brand_removed_copy": "copy with the brand name removed",
  "could_fit_another_brand": false,
  "distinct_from_other_angles": true
}
```

The angle is incomplete if any field is blank. Product names and category labels are anchors, not automatically USPs. The writer must connect the anchor to a shopper decision; otherwise the run is `evidence-limited`.

If a source is inaccessible, an asset cannot be mapped, or no conversion lever exists, return `blocked` or `evidence-limited`. Do not draft a purchase conversion ad from a generic collection title.

## Writer role

Write one evidence-led route:

`recognisable shopper tension -> mapped product reason -> source-backed buying reason -> directional Collection CTA`

The primary text and headline together must name a mapped product anchor or specific verified category. The CTA may guide browsing, but the body must not merely guide browsing.

## Independent checker role

Give the checker the brief, mapped evidence, draft, and user constraints only. Require these answers:

1. Does each central claim have an evidence pointer?
2. Does the copy add a decision reason beyond the visible asset?
3. Would it still work for an unrelated brand after replacing the name?
4. Is the CTA a next step after a buying reason, rather than the buying reason itself?

Any `no` to questions 1, 2, or 4, or `yes` to question 3, fails the draft. Revise only the failed criterion, up to two times. Enforce this with the run's `retry_budget`; a third revision must be rejected by the transition runtime. The reviewer receives the brief, mapped evidence, and current draft only—not writer self-scores, prior verdicts, or learning conclusions.

The checker must return a per-angle verdict for `product_anchor_present`, `source_evidence_present`, `specific_purchase_reason`, `could_fit_another_brand`, and `distinct_from_other_angles`. A `yes` for `could_fit_another_brand`, or a missing product anchor/evidence pointer, is a hard failure rather than an editorial suggestion.

## Learning layer

Save one concise learning entry: rejected wording, failure category, evidence gap or rule change, and a regression fixture when a new deterministic check is warranted. Preserve user taste feedback verbatim enough to prevent recurrence.
