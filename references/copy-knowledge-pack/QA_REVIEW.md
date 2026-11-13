# QA Review

status: updated_after_source_map_patch
updated_at: 2026-06-23
reviewed_by: Joy

## 結論

這包 `copy-knowledge-pack` 已整理成 21 份標準 Markdown 檔，並已補上暫定版 `00_source_map.md`。

目前可作為 v0.2 內部測試版使用，但還不建議直接視為正式知識庫。

## 已完成

- 標準化 21 份檔案命名。
- 補上 `00_source_map.md`。
- 根據內容反推 `SRC_001` 至 `SRC_006` 的主題角色、適用模組、限制與衝突。
- 標記 `SRC_006` 為 anomaly，因它只在 processing report 中出現一次。
- 保留版權安全提醒：只使用轉譯規則，不保留原文大量內容。

## 仍需 Boyi 補齊

- 每個 source_id 對應的真實電子書／文章／筆記名稱。
- 每個來源是否為你可用於個人內部知識庫的資料。
- `SRC_006` 是否真的是第六個來源，或只是 Gemini 編號錯誤。

## 風險

- 現有部分檔案含 `[cite:*]` 佔位符，但這些不是正式 citation。
- 若導入 Codex，建議先讓它把 `[cite:*]` 移除或改成 source_id 引用。
- 目前規則可用，但來源追溯仍不完整。

## 建議下一步

1. 先用 v0.2 測 3 個任務：TOFU、BOFU、Landing Page。
2. 若文案品質提升，再導入 copywrite-ad-agent references。
3. 正式導入前，補齊真實來源名稱與處理 `SRC_006`。


---

# v0.3 Source Map Update QA

更新結果：已用 Boyi 提供的 `copy-knowledge-pack:00_source_map.md` 覆蓋 `00_source_map.md`，並保留上一版自動反推檔案為：

```text
00_source_map.previous_auto_inferred.md
```

## 判定

- Source map 完整度：提升
- 模組對應：可用
- 真實來源追溯：部分可用，仍需保留原始電子書 / 摘錄檔案
- 可直接導入 Codex：可作為內部參考，但不要讓 Codex 對外輸出 `[cite: x]` 標記

## 需要注意

1. `[cite: 2]` 這類標記不是正式引用格式，應視為 Gemini 的內部來源索引。
2. `SRC_006` 現在明確對應《勾癮》，不再是完全異常來源。
3. 文中提到台灣法律、MarTech、熱度圖、2026 數據等內容，若要作為事實使用，仍需外部查證。
4. 原書案例與銷售數據只能作為說服邏輯背景，不得直接移植成新品牌宣稱。
5. 建議下一版新增 `source_assets/` 或 `source_excerpts/`，保存每個 SRC 的原始書名、章節目錄與你自己的摘要。
