---
name: copywrite-ad-agent
description: Build evidence-grounded Meta creative briefs and route ad-copy tasks to the modular copywriting workflow; brief rows pass the supplied creative-review rubric before any Google Sheets write.
---

# Skill Entrypoint

This is the stable `copywrite-ad-agent` Skill used by Hermes and existing callers. The complete implementation is this folder:

`/Users/boyi/.codex/skills/copywrite-ad-agent/`

Select the workflow by deliverable before doing research:

- **素材 brief only / Google Sheet brief:** follow `references/creative-brief-review-adaptation.md`. Produce structured brief rows, run the deterministic brief-and-review gate, and write to Google Sheets only after the entire requested set passes.
- **廣告文案／改寫／文案審查：** use the copy workflow below. Do not draft copy during the brief-only path.

For every copywriting request, initialize one canonical run artifact with `scripts/copy_run.py`; this run is the source of truth for execution state. `schemas/copy-run.schema.json` is the machine-readable workflow contract. A delivery payload passing `scripts/validate_copy.py` is not evidence that the workflow completed.

Use the single production entrypoint `scripts/copy_orchestrator.py` for copy tasks:

- `preview --brief ... --evidence ... --run-dir ...` creates and verifies the strategy artifacts, then stops at confirmation.
- `confirm --run-dir ... --confirmation-json ...` unlocks only the explicitly approved angles whose matrix digest matches.
- `draft --run-dir ...` creates copy, claim-safety, and deterministic-validation artifacts, then stops at the independent-review stage.
- `review --run-dir ... --review-json ...` imports a separate review bound to the draft, evidence, and rubric hashes; only a passing import allows learning and final verification.
- `verify --run-dir ...` independently rechecks artifact existence, hashes, stage state, and confirmation boundary.

Do not use `copy_run.py advance` as the production path; it remains a low-level test helper. Execute the stages in order and write a stage artifact before advancing:
`product_research → persona_hypothesis → shopper_tension → funnel_strategy → motivation_strategy → value_translation → framework_selection → appeal_matrix → awaiting_user_confirmation → copy_drafting → claim_safety → deterministic_validation → independent_review → learning`

For every copywriting request, load this file first, then route and load only the relevant bundled resources in this order:

1. `knowledge/ecommerce-copywriting-playbook.md` for ecommerce work.
2. `references/creative-angle-matrix.md` for motivation-based, non-overlapping buyer arguments and count handling.
3. `references/copy-knowledge-pack/07_funnel_copy_rules.md` and identify `TOFU`, `MOFU`, or `BOFU` before drafting.
4. `references/copy-knowledge-pack/08_platform_adaptation_rules.md` for platform formatting.
5. `references/brands/<brand>.md` when a brand is named.
6. Current campaign, product, landing-page, and creative evidence.
7. `references/creative-quality-contract.md`, `references/validation-contract.md`, and `scripts/validate_copy.py` before delivery.

When a brand is named, load the matching brand module and relevant historical Learning records; when no brand is named, use only the universal and applicable industry modules. Mobile brevity controls line length and paragraph scanning; it never replaces funnel-stage depth.

Before drafting multiple copy angles, separate shopper motivation, tension, desired progress, and buying reason for each. Use the creative-quality contract to check the opening, buyer payoff, distinctness, evidence boundary, and field fit. Do not pad output with feature lists or wording-only variants. Obey explicitly requested opening-line counts; do not apply a universal Meta character/fold rule.

Every TOFU, MOFU, and BOFU output must include its stage-specific evidence map and pass the matching validator contract. A short primary text is not a pass if it omits the stage's required persuasion task. Do not draft formal ready-to-paste copy while `awaiting_user_confirmation.confirmation_status` is pending; strategy preview is allowed, final delivery is blocked.

Honor the user's explicit deliverable and requested angle count. If a materially necessary scope is missing, ask a concise question or state a reasonable assumption. Do not require a redundant approval step after the user has already supplied the scope and authorized drafting. Recommend a focused set of distinct angles when useful, but never pad the count with wording variants or generated matrix combinations. Keep consumer copy free of internal theory tags; include visual direction only when requested.

For ecommerce copy, the final primary text must contain a concrete `scene_anchor` (time/place/action or decision moment) and a plain-language product-help sentence. Any technical term retained in consumer-facing copy must have a `technical_term_translations` entry whose plain-language translation also appears in the copy. These are runtime checks, not self-reported editorial notes.

After deterministic validation, stop at `independent_review` and import a separate hash-bound review using `copy_orchestrator.py review`. The reviewer must not receive writer self-scores, previous verdicts, or learning conclusions. The generated record alone is not review evidence. Only a passed `validate_copy.py`, a passing imported review, and a verified complete run may be delivered. The final status means workflow passed, not live-ready or published.

Do not treat this compatibility directory as a second rule source. Do not use old sibling files here when the bundled project skill provides the corresponding resource.

The project skill preserves these boundaries: evidence before persuasion, current Campaign evidence over historical copy, independent review, bounded repair, no automatic ad publishing, no ad-account writes, and no Shopify writes.


## 素材 brief → Review → Google Sheet 路徑

1. 先確認 campaign objective、平台／版位、語言／市場、商品或活動來源、各漏斗階段素材數量，以及 Target。此附件審查路徑目前限定 Meta 素材 brief；其他平台先取得相符的 review rubric，不可把 Meta rubric 說成完整通過。沒有數量或漏斗配置時先詢問，不可套預設支數。沒有明確 Target 時，提出有來源脈絡的受眾假說並先請使用者確認；不可把品牌輪廓或商品頁推論寫成已確認受眾。
2. 研究來源並建立 evidence manifest，分開記錄商品事實、使用者提供資訊、推論與未知。集合頁素材每列必須映射到具體商品／品類與來源依據。
3. 依使用者確認的 Target 和各漏斗任務規劃素材角度，輸出一列一支 brief。brief 提供溝通方向，不輸出可直接上稿的完整廣告文案，也不產生設計師工單。
4. 將 brief set 存成符合 `schemas/creative-brief-set.schema.json` 的 JSON；用 `scripts/validate_creative_brief.py` 檢查必填欄位、來源連結、受眾確認狀態、各漏斗數量與 review gate；若 `jsonschema` 不可用，先依 `requirements-brief-validation.txt` 安裝，不可略過 schema 驗證。
5. 以 `references/creative-brief-review-adaptation.md` 所列附件適用條件，另做一次 rubric review，逐列檢查 brief 並檢查整批差異，輸出符合 `schemas/creative-brief-review.schema.json` 的紀錄，綁定附件與 brief set SHA-256。不得用撰稿自評代替 review，也不得把 CLI 結構通過描述成語意審查或 reviewer 身分已獨立驗證。
6. 只有每列與整批 review 都通過、沒有阻擋項且 digest 相符時，`validate_creative_brief.py` 才會輸出 `SHEET_WRITE_ALLOWED`。任何一列或批次檢查未通過，整批不得寫入 Google Sheet；先針對阻擋項修正並重新 review，最多兩輪，之後標示阻擋並詢問缺少資訊。
7. 通過後才載入可用的 `google-drive:google-sheets` Skill，依其規則建立或更新指定 Sheet 並讀回驗證；不得自行重造 connector 流程。若 connector 或使用者授權的目的地不可用，回報 `PASS — NOT WRITTEN`，不得宣稱已寫入。寫入內容必須與已審查版本一致；內容一旦變更就重跑 review gate。寫入後讀回確認標題、列數與欄位值，再回報 Sheet 連結和驗證結果。

完整 brief 欄位、逐列及整批 review criteria、適用限制與停止條件以 `references/creative-brief-review-adaptation.md` 和兩份 JSON schema 為準。`SHEET_WRITE_ALLOWED` 僅代表機器契約與審查紀錄條件完整；不會認證 reviewer 身分或自行判斷內容語意。此 PASS 只表示 brief 可寫入規劃用 Sheet；不代表成品素材通過審核、Meta 政策核准或可發布。

## Mandatory collection-page conversion gate

For any ecommerce collection or catalogue destination, do not deliver final copy from a collection title, campaign slogan, or product list alone. Before drafting, create a source-backed mapping for every angle:

`product/category anchor -> concrete use moment -> source-backed feature -> felt outcome -> purchase reason`

The primary text or headline must name the mapped product or a specific verified category. A generic phrase such as "高爾夫系列" or "夏日穿搭" is not a product USP. If the page exposes only names and prices, use those facts as selection anchors but do not infer cooling, breathability, stretch, UV protection, moisture management, or performance outcomes.

For each final angle, run and record this independent test:

`Could this copy fit another brand by replacing the brand name?`

If the answer is yes, the angle fails. Brand presence, premium adjectives, or a navigation CTA do not make copy brand-distinctive. A collection conversion draft may be marked `blocked` or `failed`; it must not be promoted to a formal ready-to-paste version until the product anchor, evidence pointer, purchase reason, and brand-distinctiveness check all pass.
