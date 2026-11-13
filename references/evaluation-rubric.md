# Copywriter Evaluation Rubric v0.2.1

Each copy version must be scored out of 10.

Minimum passing score: 8/10.

## 1. Funnel Fit: 0-2

2 = Fully matches the requested funnel stage.
1 = Somewhat matches but mixes funnel logic.
0 = Wrong funnel stage.

TOFU should not sound like retargeting. BOFU should not over-explain basic brand awareness. Retargeting should assume prior interest.

## 2. USP Clarity: 0-2

2 = Clear, specific buying reason.
1 = Has a benefit but not specific enough.
0 = Generic or no real USP.

Promotion alone is not a USP.

## 3. Visual Flow Fit: 0-2

2 = Adds meaning beyond the creative and headline.
1 = Slightly repeats creative but adds some value.
0 = Repeats the same message as the creative/headline.

If visual says `最後倒數`, primary text must not simply repeat `最後倒數`.

## 4. Market-Native Ecommerce Tone: 0-2

2 = Natural, clear language for the requested market and platform. For Traditional Chinese requests, default to Taiwan ecommerce wording unless the user specifies another market.
1 = Understandable but a bit stiff, translated, or weakly localized.
0 = Corporate, generic, AI-sounding, or mismatched to the requested market.

## 5. Specificity and Non-Generic Quality: 0-2

2 = Specific to product, audience, campaign, or buying scenario.
1 = Somewhat specific but still replaceable.
0 = Could fit any brand.

## Automatic Failure Conditions

A copy fails automatically if:

- It uses generic inspirational slogans as the main message.
- It repeats the creative text without adding a new reason.
- It has no product or campaign-specific buying reason.
- It does not match the requested funnel stage.
- It sounds like a translated English marketing slogan.
- It ignores the user's provided LP, product, brand, or creative context.
- It uses urgency without explaining why the user should care.
- It claims inventory, stock, bestseller, technology, endorsement, discount, guarantee, or deadline without support.

## Revision Rule

If score is below 8:

1. Identify the weakest category.
2. Rewrite the copy.
3. Score again.
4. Only output the revised version.

## Recommended Review Note Format

For each final option:

- Funnel Fit: /2
- USP Clarity: /2
- Visual Flow Fit: /2
- Market-Native Ecommerce Tone: /2
- Specificity: /2
- Total: /10
- Main reason it passed:
- Evidence gap, if any:
