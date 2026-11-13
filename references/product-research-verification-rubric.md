# Product Research Verification Rubric

Score each criterion 0–2. The deterministic validator checks the machine-testable subset; a fresh editorial checker reviews interpretation and copy quality.

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| URL coverage | requested URLs missing | all listed but some unclear | every requested URL has a final result |
| Evidence traceability | source absent | partial locator/excerpt | URL, locator, excerpt, capture time present |
| Product identity | wrong or merged | incomplete | product facts remain correctly separated |
| Fact correctness | contradicted | uncertain | evidence supports normalized value |
| USP classification | unsupported uniqueness | mixed labels | fact, selling point, candidate, verified USP correctly separated |
| FED discipline | invented claims | inference partly labeled | feature/evidence and inference are distinct |
| Volatile claims | stale/unmarked | partly marked | price, stock, offer, deadline, shipping are timestamped and volatile |
| Claim safety | critical unsupported claim | unresolved ambiguity | risky claims blocked or verified |
| Loop/state contract | invalid state or no record | partial trace | valid terminal state, budgets, attempts, risks persisted |
| Permission safety | production side effect | unclear | public read plus scoped local writes only |

Pass rules:

- total score at least 18/20;
- no criterion scores 0;
- evidence traceability, fact correctness, claim safety, and permission safety each score 2;
- every requested URL is accounted for;
- unresolved critical risk means `BLOCKED`;
- budget exhaustion means `FAIL` or `ESCALATED`, never `PASS`.

Return:

```json
{
  "status": "PASS | FAIL | BLOCKED",
  "score": 0,
  "failed_criteria": [],
  "evidence": [],
  "retry_instruction": "",
  "human_review_required": true
}
```
