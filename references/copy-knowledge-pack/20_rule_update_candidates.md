# 模組規則更新候選清單 (Rule Update Candidates)

## 模組說明
本檔案列出未來建議加入 `Codex Skill / copywrite-ad-agent` 的動態規則更新候選。所有規則目前狀態皆為 `Pending（等待審查與核准）`，必須標記潛在風險與人工核准要求[cite: 2]。

## rule_update_candidate:
  id: UC_001
  rule: 「小螢幕斷落深度約束規則」從 4 行限制縮短為「硬性 2.5 行斷行」[cite: 3]。
  reason: 根據最新 2026 年行動裝置熱度圖（MarTech Heatmap） MarTech 數據顯示，消費者在手機智慧型手機上的滑屏速度再次加快，超過 2.5 行沒有斷行的文字方塊，跳出率（Bounce Rate）會增加 15%[cite: 3, 7]。
  evidence_from_sources: 參考 SRC_002 第三章關於「大腦熱度圖覆蓋在手機收件匣」的論述，受眾只看前幾個字，段落已徹底演變為視覺深度單元，而非文法單元[cite: 3]。
  suggested_destination: copywrite-ad-agent 核心限制指令模組
  priority: HIGH
  risk: 可能會限制部分需要堆疊極度細膩、深層情感共鳴的中長篇故事型廣告文案的流暢展開[cite: 2, 3]。
  requires_human_approval: true

## rule_update_candidate:
  id: UC_002
  rule: 將「三M內容法」中的錯誤警示，強制與台灣《公平交易法》極限詞過濾清單進行代碼級聯動[cite: 5]。
  reason: 當 AI 調用「錯誤/警告」開場時，極易在直效銷售文案中生成帶有驚悚、嚇阻、或無法驗證的醫學與財務宣稱（如：盲目記帳會導致破產、用錯洗面乳會導致皮膚潰爛），違反 Claim Safety 宣稱安全規則[cite: 2, 4, 5]。
  evidence_from_sources: 參考 SRC_001 與 SRC_005 關於台灣《公平交易法》及衛福部法規對於化妝品、健康食品不得提及療效或虛偽不實之誇大表示的實戰筆記[cite: 2, 5]。
  suggested_destination: claim_safety_rules 合規防護過濾器
  priority: CRITICAL
  risk: 可能會降低 TOFU 冷受眾文案第一行的 Hook 情感衝擊力與吸睛度，需要更精細地平衡「摩擦感」與「合規安全」[cite: 2, 3]。
  requires_human_approval: true