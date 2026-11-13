# 跨平台適配與排版規則模組 (Platform Adaptation Rules)

## 模組說明
本檔案為 AI Agent 針對特定網路媒體通路、載具與溝通平台進行「語氣、格式與行數限制」的自動化適配規則。

## rule:
  name: Meta / Facebook / Instagram 社交廣告流量適配
  applies_to: Meta Ads 廣告主文案、社群推播、 MarTech 流量獲取[cite: 7]。
  universal_or_contextual: contextual
  not_suitable_for: B2B 大額採購企劃書、官網正式隱私權條款法務公告。
  how_to_apply:
    1. 社交平台的關鍵詞是「社交（Social）」，受眾處於放鬆、心心不在焉的尋求娛樂狀態[cite: 3]。
    2. 強制執行「小螢幕段落深度約束原則」，一段絕對不超過 3 行，行與行之間必須空一行作為視覺踏腳石[cite: 3]。
    3. 前三行必須在手機首屏摺疊前（See more 之前）完成 Hook（定義問題＋煽動衝突），將最重要的獲得感提到最前面，嚴禁大量文字鋪陳[cite: 3, 4]。
    4. 符號限制：Judicious emoji（每段最多 1 個），且嚴禁使用「打造、不僅……更是……、千萬別錯過」等 AI 感極強的廢話口號[cite: 3, 5, 7]。
  weak_execution: |
    我們是一家致力於數據分析的優質 MarTech SaaS 平台。
    在當今數位轉型的時代，不僅能為您提供最先進的數據串接技術，
    更是您在繁雜商場中點燃激情、迎接每一場挑戰的不二選擇。
    歡迎點擊下方連結加入我們，共創未來的輝煌。
  strong_execution: |
    廣告費丟進去，轉換率卻像黑洞一樣看不見底？

    你每天早上查看廣告後台時，是不是也常常看著數據出神，不知道問題到底出在哪裡？
    
    這套自動化對帳系統，只要 30 秒就能一鍵核對所有異常帳目，幫你搬開月底忙亂的路障。
    
    【點擊現折 100 元，給自己一個無風險試試看的機會】：(連結)
  review_check: 在手機載具預覽時， See more 之前是否有露出核心痛點與獲得感[cite: 3, 4]？是否有超過 4 行以上沒有斷行的文字牆[cite: 3]？

## rule:
  name: LINE OA / App Push / 短信 零空間超簡短文案適配 (Ultra-Brief Copy)
  applies_to: LINE 官方帳號推播首行、手機通知（App Push）、簡訊（SMS）文案[cite: 3, 7]。
  universal_or_contextual: contextual
  not_suitable_for: 中長篇 Landing Page、部落格內容行銷文章[cite: 3]。
  how_to_apply:
    1. 大腦熱度圖（Heatmap）顯示，在極小螢幕與快節奏通知中，受眾只看主題列或通知的前 3 到 4 個字[cite: 3]。
    2. 刪除所有贅字（和、它、如果、本公司、透過），把含意最豐富、最能觸發軀體標記（如：出包、罰款、腰痛、長痘）的字眼強制塞在最前面[cite: 2, 3]。
    3. 行動裝置長度限制：主旨字元控制在 29 到 39 個英文字元（或 15 到 20 個中文字）以內，確保無須點開、在解鎖畫面上即可看清完整利益承諾[cite: 3]。
  weak_execution: 「【最新通知】親愛的顧客您好，本公司特別為您舉辦為期三天的優惠特價活動，歡迎點擊選購……」[cite: 3]
  strong_execution: 「下個月對帳又怕手誤出包？教你 1 招自動省下 80% 月底結帳時間（限時免費試用）：(連結)[cite: 3]」
  review_check: 前 4 個字是否是廢話（如：親愛的、歡迎光臨）[cite: 3]？通知被截斷前，是否有露出最核心的痛苦元凶或獲得感[cite: 2, 3]？