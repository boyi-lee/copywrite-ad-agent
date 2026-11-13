# ASH GOLF Copy Failure Patterns

Use this file only for ASH GOLF requests. It records rejected directions and acts as a hard editorial preflight; it does not create product claims.

## Required preflight

Reject or revise an ASH GOLF draft before scoring when any answer is missing:

1. Is the target golfer named beyond gender or “people who like golf”?
2. Does the first line name a concrete choice, friction, use scene, difference, or source-backed result?
3. Does the copy state why this product or look is worth clicking, rather than list features?
4. Does each text field add to—not repeat—the creative’s visible message?
5. Could this copy still work after replacing ASH GOLF and the product name with another fashion brand? If yes, reject it.

For structured ASH GOLF Meta output, retain the audience fields and at least one `usp_fed` entry in `campaign_brief`; the deterministic validator checks their presence.

## Failure: audience is too broad

### Reject

- 男性球友
- 女性球友
- 喜歡高爾夫的人
- 重視舒適與造型的人

### Why it fails

The copy has no clear listener, moment, dissatisfaction, or purchase motive, so its hook and benefit become generic.

### Corrective action

Specify identity, golf situation, clothing dissatisfaction, purchase motivation, and expected reason to click. Use only details supported by the current brief or creative.

## Failure: weather or mood is mistaken for a hook

### Reject as opening directions

- 打完一場，今天的行程還沒結束。
- 太陽正曬，球衣更要穿得輕。
- 球衣別讓你分心。
- 悶熱比體力更早拖慢節奏。
- 夏天打球，穿著狀態也很重要。

### Why it fails

These lines do not establish a product-relevant tension or a credible reason to click. They sound like ad copy written to sound like advertising, not a thought a golfer would naturally have.

### Corrective action

Begin with one concrete choice or friction the identified golfer recognises. Verify any feature-led result from the landing page or product source.

## Failure: features presented as the USP

### Reject

```text
涼感面料、輕量設計、透氣材質
WAACKY 細節、俐落版型、鮮明配色
```

### Why it fails

They are unconnected attributes. They do not explain the wearing moment, a practical consequence, ASH GOLF’s selection value, or why this item differs.

### Corrective action

Write the FED bridge in the brief first:

```yaml
usp_fed:
  - feature: source-backed feature
    evidence: source URL, product text, or supplied creative detail
    desire: concrete on-course or styling outcome for the named golfer
    purchase_reason: why this makes the item or look worth opening
```

If a specific technical claim is missing, use supported selection or styling logic instead of inventing performance language.

## Failure: copy ignores the creative

### Reject

The primary text repeats the visible campaign title, product name, sale line, or a literal description of the model’s outfit without adding a buying reason.

### Corrective action

Map the creative first. If it shows a complete male or female look—including polo, trousers or skirt, cap, and socks—decide whether the copy should add a styling choice, a golf-use benefit, or a browsing route. Do not write an unrelated story that the visual cannot support.

## Failure: AI-sounding surface polish

### Common signals

- abstract statements that could apply to any apparel brand;
- symmetrical slogans with no wearer, friction, or product reason;
- stacked adjectives that replace a concrete benefit;
- a polished line that sounds unlike something a regular golfer would say;
- “style plus function” stated as a conclusion without showing the situation that makes it matter.

### Interception test

Read the first line aloud, then ask:

1. Would the named golfer recognise this as their own clothing choice or frustration?
2. Can a shopper identify the item’s reason to click without decoding a marketing phrase?
3. Is at least one claim grounded in the current product, LP, or creative?
4. Does the line add meaning after the image, rather than paraphrase it?

Any “no” is a revision, not a score deduction.

## Collection-ad specificity gate: translate every category into a golfer's moment

For a full-catalog or multi-category ASH GOLF ad, abstract category language is a rejection trigger unless it is immediately unpacked into a recognisable golf scene.

### Reject or revise when the copy says only:

- 補對裝備
- 實際缺口
- 腳下狀態
- 球袋配置
- 下場需求
- 讓每一支桿都有明確任務
- 一站補齊

These phrases may appear in an internal brief, but they are not sufficient consumer-facing reasons. Replace them with the concrete decision or friction:

- 服飾：上桿、轉身或拉伸時，肩膀與背部是否被衣服拉住。
- 鞋款：下過雨的濕草、斜坡或轉身擊球時，腳底是否失去抓地感；可延伸鞋釘與無鞋釘的選擇，但不能宣稱每雙鞋都能應付所有地形。
- 球桿：兩支球桿打出接近距離，或球袋中間缺少一段實用距離；要維持在選桿問題，不要承諾廣告能直接修正球友的球技。
- 配件：手套磨薄、帽子遮陽需求、球袋或收納用品是否符合實際攜帶方式。

### Accepted hook pattern from Boyi's approved rewrite

Use a sequence of direct golfer questions with concrete friction and a concrete choice:

```text
揮桿時肩膀被衣服扯住？下過雨的濕草斜坡上腳底微微滑掉？還是球袋裡總有兩支打出來距離差不多的球桿？
```

The next sentence should name the practical consequence in plain language, such as interference with the swing or club selection. Do not replace these scenes with polished summaries such as `為下一場補對` or `檢查實際缺口`.

### Accepted body structure for a full-catalog MOFU ad

1. concrete question hook: apparel movement, shoe grip, club-distance overlap;
2. felt consequence: the small annoyance becomes a distraction during the swing or club choice;
3. ASH role: name the actual categories and the multi-brand catalogue;
4. four browsing routes, each tied to a concrete decision;
5. directional catalogue CTA.

Do not expose this structure or the terms `USP`, `FED`, `MOFU`, or `selection logic` in consumer-facing copy.

## Final ASH GOLF gate

An ASH GOLF draft can enter the universal 8/10 quality gate only after it has:

- a specific audience;
- a concrete first-line hook;
- one source-backed FED/USP bridge;
- concrete product-category scenes rather than abstract selection language;
- creative-to-copy role separation; and
- no recorded failure pattern or generic AI phrasing.
