# Meta Conversion Copy Review Loop

Use this route for Facebook / Instagram conversion-copy review or rewrite, including Feed, Reels, Stories, Collection, Carousel, and Catalog. It is a writing-and-review workflow, not permission to publish an ad.

## Required decision bridge

Complete this compact brief before editing. Mark unknown commercial facts as `missing`; never guess them.

| Field | Decision question |
| --- | --- |
| Persona | Who sees this, what are they doing, and what wording sounds natural to them? |
| Funnel | Cold / MOFU / BOFU / retargeting: what do they know and still need to believe? |
| Need angle | Which concrete desire or friction is worth opening with now? |
| JTBD / problem | What is the buyer trying to get done, and what physical or social friction blocks it? |
| Evidence | Which current source supports product help, proof, offer, and urgency? |
| Creative pattern | What does the visual already say, and what must copy add instead of repeat? |
| CTA | What exact next action should happen, and what verified benefit makes it worth doing now? |

## Process gates

1. **Source gate:** keep product facts, campaign terms, and visible creative text separate. Missing evidence may lead to a safe review, never an invented claim.
2. **Opening gate:** honor the user's requested number of opening lines and the supplied placement/asset. Make the opening immediately recognizable to the intended buyer through a concrete moment, choice, tension, useful payoff, or specific curiosity. Do not impose a universal line count, character count, reading-time claim, or feed-fold threshold. A long English model name should not consume the opening unless identification is the intended hook.
3. **Language gate:** turn a feature into `real situation → felt friction → useful outcome`. Prefer a visual action such as `黏在背上`, `狂晃`, or `扣扣撞` when accurate for the source and audience.
4. **Field-job gate:** primary text earns attention and gives a buying reason; the headline adds a decision cue; a Collection CTA tells shoppers what to browse next and why.
5. **Action gate:** the final CTA names the next action and connects it to a verified benefit, offer, deadline, or remaining decision. Never manufacture urgency.
6. **Quality gate:** run deterministic validation, then independently check evidence, opening strength, buyer payoff, angle distinctness, Taiwan spoken rhythm, mobile scanability, and CTA usefulness. A feature list without a buyer-relevant payoff fails. Revise no more than twice.

## Taiwan conversion-language hard constraints

Campaign-specific constraints may add to these defaults. They may not weaken them unless the user explicitly approves an exception.

- Do not use `無縫接軌`, `俐落`, `跟上行程`, `為您帶來`, `完美結合`, `撐`, or `卡卡` in consumer-facing copy.
- Do not use `無論是……還是……` or `不是……，是……`, including close reconstructions.
- Do not place a long English model name or product code in the first three non-empty primary-text lines. Keep an official name only where identification requires it, then add a plain Traditional-Chinese category name.
- Do not use technical jargon as a benefit. Translate it into moment, friction, and supported outcome first.
- Do not write unverified stock, countdown, discount, guarantee, endorsement, comparison, or performance outcomes.

## Review output contract

For a review-only task, return exactly these five Markdown sections. For a drafting task, follow the user's requested deliverable structure instead; include primary text, headline, description, CTA, or other fields when requested.

### 1. 整體意見

Assess pain-point precision, scene construction, product value, mobile readability, and conversion push. State evidence limits plainly.

### 2. 品名與標示編輯

Shorten or translate long English names. Give a usable Chinese display name and state where an official model name may remain for identification.

### 3. 文法與鉤子診斷（逐項列點）

Review `主文案開頭／鉤子`, `素材標題`, and `精選集 CTA` sentence by sentence. State the issue and editing direction for each.

### 4. 待加強部分

List missing conversion levers: concrete friction, product proof, objection answer, offer, urgency, visual punctuation, or shopper-benefit CTA. Call for urgency only when a source can support it.

### 5. 重寫提案（正式上稿版）

Return a ready-to-paste `主文案`, `素材標題`, and `精選集 CTA`. Use blank lines and restrained emoji only where they improve mobile scanning.

## Learning record

For each material rejection, retain:

```yaml
rejected_copy: ""
failure_reason: ""
smallest_rule_change: ""
regression_fixture: ""
validation_result: "passed | failed"
```

Do not promote a one-off preference into a global rule without a regression fixture and a passing test suite.
