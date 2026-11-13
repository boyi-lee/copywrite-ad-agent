# Meta Formats

## Shared rules

- The first three non-empty lines are the hook zone and should stay near 125 Chinese characters or fewer. This is not a limit on the full primary text.
- Keep headlines near 40 characters or fewer.
- Use PAS as reasoning support, not as visible fixed labels.
- Match verbs to what the interface actually lets the shopper do.

## Collection and Instant Experience

The hero creative earns attention; the collection or destination supports curated exploration.

- Explain what has been selected and what shoppers can browse after opening.
- Use behavior such as open, browse, look through, choose, or continue downward.
- Organize multi-category offers into a useful route when appropriate.
- Supply `destination_button_text` only when the destination supports a custom button; make it benefit-led and concise.

## Carousel and Catalog

The interface supports card-by-card browsing and comparison.

- Explicitly guide left-right swiping or item comparison.
- Provide a category order or selection route when useful.
- Help shoppers understand what to inspect on each card.
- Avoid writing Collection-style downward exploration for a standard carousel.

## Feed

- Let the creative carry visible promotional facts.
- Use primary text for the scene, problem, product value, and action.
- Use headline and description to add, not repeat, information.

## Required Meta output

```json
{
  "variant_name": "A",
  "angle": "brief description of the chosen route",
  "primary_text": "...",
  "headline": "...",
  "description": "...",
  "call_to_action": "...",
  "destination_button_text": ""
}
```
