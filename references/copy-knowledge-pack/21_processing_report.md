# 處理報告與導入建議 (Processing Report)

## 1. 已處理文獻與核心模組 (Processed Sources & Active Modules)
本套「通用文案能力知識庫」已完整掃描並精煉了以下 5 本經典著作與實戰筆記精華（SRC_001 至 SRC_005），完全拋棄了空泛的讀書心得，成功將其轉譯為 21 個可供 AI Agent 代碼級調用的底層通用原則與套用句型[cite: 2, 4, 7]。

### 提煉出的最強通用底層模組：
*   **受眾意圖與無意識心理模組**：成功將弗雷德 10 大購買動機、 PQR2 懸崖模型抽象化為通用心理學機制，克服受眾的反駁心理（Counter-argument）[cite: 2, 3, 4]。
*   **價值與方案轉譯模組**：提煉出 3+5 超級賣點直白轉譯、費時費力代價原則與心理帳戶偷換模型，將冷冰冰的規格翻譯為深層生命意義[cite: 2, 3, 4, 7]。
*   **全漏斗與跨平台適配模組**：建立了通用 TOFU/MOFU/BOFU 的受眾狀態矩陣，並對齊了手機小螢幕超簡短文案（UBC）的硬性斷行與行數限制約束[cite: 3, 7]。
*   **合規安全與去 AI 味過濾器**：建立了可用於任何產業的 Claim Safety 防火牆與負向文字限制規則（嚴禁使用「不僅……更是……、打造、不二選擇」）[cite: 2, 3, 5, 7]。

## 2. 發現的文獻衝突點 (Conflicts Found)
*   **衝突 1 (直效推銷強度 vs. 品牌高級感調性)**：SRC_001 與 SRC_003 擁護極強的直效宣稱、紅利買贈與價格平分法；而 SRC_002 與 SRC_006 則強調過度的廣告痕跡與強迫推銷（如直接喊驚爆特價、買到賺到）會激發大腦的防禦機制，減損高單價品牌的溢價資產[cite: 2, 3, 4, 6, 7]。
    *   *知識庫解決方案*：在 `00_source_map.md` 與 `10_tone_and_voice_rules.md` 中設立「調性權重過濾器」。當任務標記為「高級感/品牌文案」時，AI Agent 會自動將直效催單權重調低，改為調用「費時費力代價原則」與「完形整體美學描述」[cite: 2, 3, 4, 6]。
*   **衝突 2 (精簡字數 vs. 長文案說服力)**：SRC_004 與平台通路適配規則強調行動裝置的簡潔是關鍵（UBC原則）；但 SRC_002 與歷史經典案例則提出，當受眾面對高價或需要充分資訊才能決策的產品時，長文案的轉換率（CVR）遠高於短文案[cite: 3, 4, 5, 7]。
    *   *知識庫解決方案*：在 `07_funnel_copy_rules.md` 與 `08_platform_adaptation_rules.md` 中設立「長度因時制宜規則」。短通知、 LINE 推播與手機解鎖畫面強制簡潔；中長篇銷售頁與 B2B SaaS 產品頁則允許使用精煉、無贅字的長文案層層遞進說服[cite: 2, 3, 4, 7]。

## 3. 下一步如何導入 Codex / copywrite-ad-agent 建議
為了讓這套通用知識庫真正落地，成為您日常廣告投放與文案優化的 MarTech 利器，建議您按照以下步驟進行工程化配置：

*   **第一步：架構 System Instructions (系統指令封裝)**
    將 `01_universal_copywriting_principles.md`、`03_audience_intent_and_psychology.md` 與 `16_anti_ai_copy_rules.md` 的文字內容，直接複製並黏貼到 ChatGPT GPTs 的 System Prompt 或自建 Agent 的核心代碼約束區。作為 Agent 每次生成文字時必須遵循的「底層靈魂與行為框架」[cite: 3, 5]。
*   **第二步：配置 RAG 知識庫 (向量檢索掛載)**
    將 `02_persuasion_frameworks.md`、`07_funnel_copy_rules.md`、`08_platform_adaptation_rules.md`、以及所有句型庫（11_headline, 12_body, 13_cta, 14_objection）打包成知識庫文檔，上傳到 Agent 的儲存空間中。當您在前端輸入指令「任務：撰寫 B2B SaaS 的 MOFU 產品頁文案」時，Agent 會自動向量檢索並精準對齊相關規則與句型，進行變數替換[cite: 2, 4, 7]。
*   **第三步：開啟自我審查代碼循環 (Self-Correction Code Block)**
    在系統的最後一個步驟中，強制嵌入 `15_claim_safety_rules.md` 與 `17_review_rubric.md`。要求 Agent 在交付稿件給您（投手）之前，必須先在後台對自己寫的初稿進行 14 個維度的嚴格打分[cite: 7]。如果評分出現「只寫了活動折扣但沒有轉譯為行動理由」，大腦評分量表會自動觸發硬性最大 3 分限制規則，系統將自動 Block 稿件，並逼迫 AI 重新調用 `16_anti_ai_copy_rules` 進行自我優化降噪，直到打分大於 4 分時，才允許Live-Ready核准上稿，從此徹底解放投手的人工審稿時間[cite: 3, 4, 5, 7]！