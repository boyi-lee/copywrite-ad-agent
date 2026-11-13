# FILE: copy-knowledge-pack/00_source_map.md

# Source Map

status: needs_source_detail

## QA 結論

原始壓縮檔內沒有獨立完整的 `00_source_map.md`。現有模組使用 `SRC_001`、`SRC_002`、`SRC_003`、`SRC_004`、`SRC_005` 等來源代號，但未提供代號與實際書名／文章／筆記的對照。

這份檔案是整理後補上的待補模板，不應視為已完成 source map。

## 待補格式

```yaml
source:
  source_id:
  source_name:
  source_type: book / ebook / article / note / case / other
  main_topics:
  useful_for:
  limitations:
  extracted_modules:
  copyright_safety_note:
```

## 目前已偵測到的來源代號

- SRC_001
- SRC_002
- SRC_003
- SRC_004
- SRC_005

## 為什麼一定要補

沒有 source map，知識庫短期仍可拿來測試，但長期會有三個問題：

1. 規則無法追溯來源。
2. 衝突規則無法判斷該信哪一套。
3. 未來要更新、刪除、合併規則時會很痛苦。
