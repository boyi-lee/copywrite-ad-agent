# Product Research Loop

Use this route when the input includes product URLs. It extends the copy workflow; it does not replace the campaign brief, USP/FED rules, claim-safety rules, or platform review.

## Loop contract

```yaml
loop_id: copywrite-product-research
version: 1.0.0
owner: Boyi
business_goal: Turn public product pages into source-traceable product evidence and reviewable USP candidates before copywriting.
trigger:
  type: explicit_user_request
  source: one_or_more_http_urls
  frequency: on_demand
input_contract:
  required_fields: [urls]
  evidence_sources: [user_brief, public_product_page, matching_brand_profile]
worker:
  role: product_evidence_researcher_and_copywriter
  tools: [Crawl4AI_or_browser, local_normalizer, copywrite_rules]
  allowed_actions: [public_GET, local_artifact_write, draft_copy]
checker:
  role: deterministic_validator_plus_fresh_editorial_checker
  isolated_context: true
  rubric_path: references/product-research-verification-rubric.md
budgets:
  max_attempts_per_url: 2
  max_urls: 20
  max_duration_seconds: 180
  max_concurrency: 4
  no_progress_rounds: 1
state:
  task_store: run-record.json
  artifact_store: caller_supplied_output_directory
  memory_store: none_by_default
permissions:
  maturity_level: L2
  write_scope: [caller_supplied_local_output_directory]
  approval_required: true_for_install_or_external_side_effects
outputs:
  required_artifacts: [product-research.json, run-record.json, raw_markdown_when_available, checker-verdict.json]
  delivery_channel: current_task
observability:
  trace_fields: [run_id, requested_url, final_url, status_code, attempt, duration, evidence_count, error]
  metrics: [url_success_rate, evidence_coverage, blocked_claim_count, retry_rate, duration]
escalation:
  owner: Boyi
  conditions: [robots_denial, access_wall, all_urls_failed, missing_required_evidence, budget_exhausted, checker_uncertain]
rollback:
  strategy: delete_the_run_directory; no_remote_or_production_state_is_changed
```

## Evidence collection order

For each product, use this order:

1. Current user brief and explicit constraints.
2. Product JSON-LD or other machine-readable page data.
3. Visible product-page content such as description, feature, specification, material, offer, shipping, and return sections.
4. Matching brand profile, only for permanent brand voice or verified brand facts.
5. General category knowledge, only as analysis context and never as product evidence.

Save raw Markdown separately when the local crawler is used. Keep the normalized artifact small enough for review; do not treat the raw page as a validated fact set.

The bundled runner forces `CRAWL4_AI_BASE_DIRECTORY` into the current run directory before importing Crawl4AI. This prevents hidden writes to `~/.crawl4ai` and keeps cache, database, logs, evidence, and rollback scope together.

Only public HTTP(S) product URLs are accepted by default. Localhost, literal private IPs, link-local addresses, embedded URL credentials, and non-HTTP schemes are rejected. `--allow-private-network` exists only for explicit local fixture testing. Redirect targets still require review when network boundaries are sensitive.

## Required evidence object

Every usable product fact must include:

```json
{
  "field": "feature",
  "value": "source-backed value",
  "source_url": "https://example.com/product",
  "source_type": "json_ld | page_text | user_brief | brand_profile",
  "source_locator": "Product.description or page heading",
  "evidence_text": "short supporting excerpt",
  "captured_at": "ISO-8601 timestamp",
  "confidence": "high | medium | low"
}
```

Reject a fact when the excerpt does not support the normalized value. Mark transient facts such as price, availability, discount, deadline, shipping, and stock with `volatile: true`.

## USP classification

- `verified_fact`: a directly supported specification, price, policy, or page statement.
- `selling_point`: a supported feature translated into a plausible buyer benefit.
- `usp_candidate`: a supported buying reason that appears differentiating but lacks independent comparison evidence.
- `verified_usp`: a differentiator supported by explicit comparison data or other reliable market evidence.

Do not upgrade a classification merely because the page uses words such as unique, exclusive, best, leading, patented, or professional. Preserve those as page claims until their evidence is verified.

Translate usable candidates through:

```text
feature -> evidence -> functional benefit -> use case -> desire -> buying reason
```

Inference must be labeled. `feature` and `evidence` can be verified; benefits, use cases, desires, and buying reasons may be reasoned interpretations and must not silently become factual performance claims.

## Execution

When Crawl4AI is available:

```bash
python3 scripts/crawl_products.py \
  --url "https://example.com/product-a" \
  --url "https://example.com/product-b" \
  --output-dir "outputs/product-research"

python3 scripts/validate_product_research.py \
  "outputs/product-research/<run-id>/product-research.json" \
  --write-verdict "outputs/product-research/<run-id>/checker-verdict.json" \
  --update-run-record "outputs/product-research/<run-id>/run-record.json"
```

If Playwright browsers live outside the default location, pass their approved directory with `--browser-path`. The runner does not download packages or browsers automatically.

One-time isolated setup, only after the user approves dependency and browser downloads:

```bash
python3 -m venv .venv-crawl4ai
.venv-crawl4ai/bin/pip install -r requirements-product-research.txt
PLAYWRIGHT_BROWSERS_PATH=.playwright-browsers \
  .venv-crawl4ai/bin/playwright install chromium
```

Then use `.venv-crawl4ai/bin/python` for the crawl command and pass `--browser-path .playwright-browsers`. Do not install into the system Python automatically.

If Crawl4AI is unavailable, use an available browser/research tool and produce the same schema. Do not claim the local crawler ran.

## Verification loop

1. Run the deterministic validator.
2. Use a fresh editorial checker context where practical.
3. The checker reviews only the brief, normalized evidence, proposed USP/FED, draft copy, and fixed rubrics.
4. If the checker returns `FAIL`, retry only the failed criteria and only while the harness budget remains.
5. If the failure is missing evidence, access denial, ambiguous product identity, or budget exhaustion, return `BLOCKED` or `ESCALATED`; rewriting cannot repair missing evidence.
6. Never overwrite a checker failure with a worker self-score.
7. Persist the checker verdict into `checker-verdict.json` and update `run-record.json`; chat-only status is not sufficient.

## Final-state rules

- `passed`: every requested URL is accounted for, required evidence is traceable, deterministic checks pass, and no critical risk remains.
- `failed`: the task was attempted within budget but produced invalid artifacts or repeated no-progress failures.
- `blocked`: required evidence cannot be accessed or verified.
- `escalated`: permission, legal/compliance judgment, production action, or budget expansion requires Boyi.

Research and copy drafts remain `live_ready: false` and `manual_check_required: true` at L2. Human approval is required before upload or publication.

## Improvement loop

After at least 10 human-reviewed runs:

1. Group failures by access, extraction, normalization, USP inference, claim safety, funnel fit, or platform formatting.
2. Propose one bounded change.
3. Run existing regression fixtures plus a new fixture representing the failure.
4. Compare pass rate, false-positive claims, evidence coverage, cost, and latency.
5. Keep or reject the proposal explicitly and preserve the previous version.

The improvement loop may create a proposal; it may not edit this Skill, its budgets, permission gates, validator, or production assets automatically.
