# Creative Brief Review Gate

## Purpose and boundary

Use this gate only for the brief-first ecommerce workflow. The source rubric is `meta-creative-reviewer-v0.4.md`, supplied by the user, and is scoped to Meta creative. For another platform, do not claim this file provides a complete platform review; pause the Sheet gate until a suitable rubric is provided or the user narrows the task to Meta. It reviews finished Meta ad creatives. A brief contains proposed content and directions, not a finished visual; therefore its visual composition, typography, legibility, crop, mobile readability, and production-finish scores cannot be assessed yet. Do not invent those scores or claim that the design has passed review.

The user's operative instruction is: generate creative briefs, review them against the applicable parts of the supplied rubric, and write to Google Sheets only after the complete brief set passes. The source document's finished-creative output format does not replace this workflow or require its five-section report when reviewing briefs.

## Review inputs

Review the exact versioned brief set and source-evidence manifest. The writer's explanations or prior self-review are not evidence. Run a distinct second-pass review against the structured brief rows, source references, request constraints, and batch; do not provide writer self-scores as review evidence. The review artifact records whether this was an AI second pass or a human review. The deterministic script checks that record and its bindings, but cannot authenticate identity or decide semantic correctness; never describe its output as proof of independent review.

Use evidence classes from the source rubric:

- `OBSERVED`: directly visible in supplied creative or source.
- `SUPPORTED_BY_BRIEF`: explicitly supported by the approved user brief or current product/campaign source.
- `INFERRED`: a hypothesis; must be labeled and cannot become a confirmed product claim.
- `UNKNOWN`: missing or unverifiable; state what must be confirmed.

Keep product evidence separate from audience-demand evidence. Product pages can support features and product identity; they do not prove customer demographics, purchase history, or market demand.

## Brief-level review criteria

Each per-brief criterion must be marked `PASS` or `BLOCK` with a short rationale. Batch coverage and similarity are reviewed once at batch level, also as `PASS` or `BLOCK`. `NOT_APPLICABLE` is reserved for finished-asset checks because no designed asset exists yet. A block requires correction or a clearly identified user-owned input before Sheet writing.

1. `target_clarity`: each brief identifies a specific user-confirmed target or a user-approved audience hypothesis and a relevant situation. Do not infer sensitive demographics or treat a brand profile as campaign targeting.
2. `funnel_fit`: the awareness state, buying task, and proposed persuasion depth fit the requested TOFU, MOFU, or BOFU stage.
3. `shopper_tension`: the need, friction, or decision barrier is concrete and grounded or explicitly labeled as a hypothesis.
4. `product_and_claim_evidence`: product identity and every proposed factual benefit, offer, urgency, or service claim have current evidence; unsupported claims are removed or marked unknown.
5. `message_focus`: the brief states one primary buying reason and a clear message direction without substituting generic praise for a reason to choose.
6. `visual_direction_fit`: the suggested visual direction can express the message and point to its mapped product/category. Assess as a proposed direction only; do not grade actual composition, readability, or mobile rendering.
7. `next_action`: the CTA direction names a plausible next action and does not invent an offer or urgency.
8. `creative_angle_clarity`: the reason or presentation route is clear for this single brief; a label alone such as “comfort” or “style” is insufficient. This applies the source rubric's Creative Angle clarity check.
9. `angle_distinctness`: the angle differs from other briefs by meaningful target, context, benefit, tension, proof role, or decision—not merely wording, color, or format changes.
10. `brand_and_campaign_fit`: the brief follows the user-approved campaign scope and applicable brand constraints without treating historical brand facts as current SKU evidence.
Batch criterion `batch_coverage`: requested stage counts are met and the coverage map reflects the requested audience and stage mix.
Batch criterion `similarity_check`: the set has no accidental duplicate routes; meaningful variation is grounded in target, context, benefit, tension, proof role, or decision.

`finished_asset_checks`: `NOT_APPLICABLE` at brief stage. The eventual designed assets must later receive the full source rubric, including all 15 scores and applicable batch analysis, before design-delivery approval. This does not block writing an otherwise passing brief to the planning Sheet.

A brief set passes only when criteria 1–10 for every row are `PASS`, both batch criteria are `PASS`, there are no unresolved blocking findings, every requested row passes, and the review is bound to the exact brief-set and bundled rubric digests. Any `BLOCK`, missing required criterion, wrong count, unresolved product claim, or unconfirmed Target blocks the entire requested batch from Sheet writing. Do not write a partial batch unless the user explicitly changes scope.

## Review and repair loop

1. Generate the complete brief set and validate its structure, stage counts, and evidence references.
2. Freeze the canonical brief-set digest.
3. Review every row against criteria 1–10; then assess both batch criteria once and mark finished-asset checks `NOT_APPLICABLE`.
4. Save a structured review artifact with reviewer type and identifier, bundled rubric digest, decision, a verdict for every brief and criterion, batch verdicts, blocking findings, and the exact digest reviewed.
5. Run `scripts/validate_creative_brief.py` on the brief set plus review artifact. Only exit code 0 with `SHEET_WRITE_ALLOWED` authorizes a Sheet write.
6. If blocked, revise only the identified issues, record the failure reason and targeted correction, create a new digest, and review again. Allow at most two repair rounds; then stop as `BLOCKED` and request the missing information.
7. If the Google Sheets connector or user-authorized destination is unavailable, stop after review and report `PASS — NOT WRITTEN`; do not imply a write occurred. Otherwise write the exact reviewed rows to the designated/new Google Sheet. Do not change content after review. If content changes, re-review the new digest.
8. Read back the written range and verify row count, headers, and values against the reviewed rows. Report the Sheet link, reviewer decision, and read-back result.

A rubric PASS certifies brief readiness for Sheet planning, not finished-creative quality, ad-policy approval, expected performance, or permission to publish. The CLI pass only validates the schema and recorded gate conditions; it cannot authenticate the reviewer or replace the rubric review.
