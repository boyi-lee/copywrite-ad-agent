# 通用 Hook 與注意力引導句型庫 (Hook & Attention Patterns)

## 模組說明
本檔案提供 AI Agent 針對跨平台短文案（如 Meta 廣告、LINE OA 推播、App Push、EDM 主旨、簡報首頁）撰寫前三行 Hook 的底層句型。旨在打斷受眾低涉入處理（Low-Involvement）的刷屏慣性[cite: 2, 3]。

## pattern:
  name: 1秒反常識打斷句型 (The Cognitive Disruption Hook)
  summary: 透過提出與受眾日常既有常識、習慣完全相反的指令或現象，在邊緣系統中製造認知摩擦感，迫使其停下腳步尋找原因[cite: 2, 3, 5]。
  universal_or_contextual: universal
  applies_to: TOFU 冷受眾文案、SEO 文章標題、EDM 主旨、MarTech 社群貼文[cite: 2, 4]。
  not_suitable_for: BOFU 結帳最後一步、B2B 大額採購招標規範書[cite: 2, 7]。
  how_to_apply:
    1. 找出該業界受眾習以為常、視為政治正確的黃金守則（例如：要對每個人好、預算不夠別投廣告、精華液擦越多越好）。
    2. 套用公式：[假性篩選身分] ＋ [做某件常識中正確的事] ＋ 為什麼反而會讓你 [面臨更慘的衝突/代價]？[cite: 4, 5]
  examples:
    - example:
        industry: 線上課程
        platform: Meta Ads
        funnel_stage: TOFU
        copy_task: 廣告大標題
        text: 「【給想把知識變現的創業者】每天花 5 小時寫完美的文章，為什麼反而會讓你一個客戶也找不到？[cite: 2, 4]」
        why_good_or_bad: 成功打斷常識「多寫文章會帶來客戶」，逼出「為什麼」的強烈好奇心[cite: 2, 5]。
        reusable_rule: 顛覆傳統認知，將「努力」的過程反轉為「無效」的代價[cite: 2, 3]。
        caution: 後文 Persuade（說服）區必須立刻給出合理解釋，否則會淪為 Clickbait[cite: 2, 3]。
    - example:
        industry: 醫美保健
        platform: LINE OA 推播
        funnel_stage: TOFU
        copy_task: 推播前言
        text: 「天天敷保濕面膜、狂擦玻尿酸，為什麼你的臉反而越來越乾，甚至成了敏感肌？（皮膚科醫生揭密：問題通常出在潔面後的這 10 秒）[cite: 2, 4, 5]」
        why_good_or_bad: 抓準女性護膚最怕敏感的痛點，以權威醫生的身分引起注意與信任[cite: 2, 4, 5]。
        reusable_rule: 痛點具體化 ＋ 限制時間區隔[cite: 2, 4, 5]。
        caution: 嚴禁使用誇大宣稱，如「臉部會潰爛、得不治之症」[cite: 2, 5]。
  weak_execution: 「【全新上市】最有效率的知識變現與寫作技巧課程，不容錯過！」[cite: 3]
  strong_execution: 「天天日更寫文章（常識），為什麼你的個人品牌還是不慍不火，甚至連一個願意付費的客戶都吸引不到（反常識代價）？[cite: 2, 4]」
  review_check: 第一行是否使用了「全新上市、熱銷、不容錯過」等罐頭詞[cite: 3]？是否成功製造了認知衝突？

## pattern:
  name: 三M內容法錯誤警示句型 (The 3M Error-Warning Hook)
  summary: 人類大腦對「警告（Warning）」和「別犯錯（Avoid Mistakes）」的防禦生理機制，遠強於對於「獲得好處」的追求[cite: 4]。指出特定族群正在犯的隱密錯誤，能瞬間圈定目標[cite: 4]。
  universal_or_contextual: universal
  applies_to: 所有產業、TOFU/MOFU、個人品牌觀點轉化、EDM 序列信、App Push[cite: 2, 4]。
  not_suitable_for: 形象建立完畢後的純感性週年慶謝恩品牌文案[cite: 2, 7]。
  how_to_apply:
    1. 提煉出該產業弗雷德最常犯、且常理下以為沒事的三種「迷思/誤解/錯誤（3M）」[cite: 4]。
    2. 套用公式：警告：[假性篩選身分] 在 [特定場景] 裡最常犯的 [奇數數字] 個致命錯誤（即使你已經很有經驗也一樣）[cite: 4, 5]。
  examples:
    - example:
        industry: B2B SaaS
        platform: Google Ads
        funnel_stage: MOFU
        copy_task: 搜尋廣告標題
        text: 「警告：中小企業會計在月底手動對帳時，最常犯的 3 個財務核對錯誤（即使你再細心也很難避免）[cite: 2, 4, 5]」
        why_good_or_bad: 精準圈住會計與老闆，利用財務出錯的巨大不安全感驅動點擊[cite: 2, 3, 4]。
        reusable_rule: 身份標籤 ＋ 錯誤提示 ＋ 排除其細心防禦（拔刺）[cite: 2, 4]。
        caution: 數據（3個錯誤）必須在內文中一一對應說明。
    - example:
        industry: 金融理財
        platform: Landing Page
        funnel_stage: TOFU
        copy_task: 首屏大標題
        text: 「每個想提早退休的職場人，最容易掉入的 5 大資產配置誤解！在看這份報告前，千萬別把錢放進去……[cite: 2, 3, 4, 5]」
        why_good_or_bad: 利用「可得性直觀推斷」，將資產虧損的恐懼具象化[cite: 3, 4]。
        reusable_rule: 警告 ＋ 資訊差階梯 ＋ 行動限制[cite: 3, 4]。
        caution: 嚴禁亂承諾穩賺不賠，Claim Safety 權重需拉高。
  weak_execution: 「提供您最專業的中小企業自動化對帳與財務系統，歡迎點擊。」[cite: 2, 7]
  strong_execution: 「【會計人請注意】月底熬夜用 Excel 結帳時，最容易讓公司被稅務機關查核的 3 個隱密錯誤（即使你是十幾年老會計也很容易看漏）[cite: 2, 4, 5]」
  review_check: 提問是否平凡無奇（如：你對現在的工作滿意嗎？）？是否建立了資訊階梯（掌握受眾不知道的祕密）[cite: 2, 4]？