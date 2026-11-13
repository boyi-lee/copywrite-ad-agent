# 跨產業通用文案大腦評分量表 (Universal Review Rubric)

## 模組說明
本檔案為整套知識庫的終極防禦關卡（Final Gate）。AI Agent 必須在輸出任何初稿後，嚴格對照以下 14 個維度進行自我評分。未滿 4 分者一律 Block（封鎖），嚴禁進入上稿工作流。

## 1. 滿分 5 分核心維度量表 (Dimension Rubrics)

### 評分定義 (Score Definition)
*   **5 分 (Live-Ready Great)**：文案完美對齊受眾當下的漏斗意圖[cite: 2, 7]；成功將功能特點轉譯為用戶生命的深層意義[cite: 2, 4]；主動化解異議與阻力成本[cite: 3, 4]；語氣流暢且具備台灣社群自然口語，無任何宣稱風險（Claim Safety）[cite: 2, 3, 5]。
*   **4 分 (Workflow Allowed)**：核心利益說明清晰[cite: 7]，語氣通順，符合品牌調性，但「利益到意義的轉譯」稍微生硬，允許進入工作流，但必須提示投手進行人工 Live Check。
*   **3 分 (Maximum Limit Rule)**：**硬性規定！若促銷或銷售文案只寫清楚了方案/Offer（如：現折 200元、買一送一），但「完全沒有」將 Offer 轉譯為 Return-to-buy action（回來帶走的具體生活/打球行動理由），最高只能給 3 分，直接 Block 封鎖[cite: 2, 4, 7]。**
*   **1-2 分 (Automatic Block)**：流於字面自誇與空泛形容詞[cite: 2, 3, 7]；重複素材字卡內容[cite: 7]；具備嚴重的機器人 AI 味口號腔[cite: 3, 5]。

## 2. 14個打分維度指標 (14 Dimensions)
1.  **Brief Fit (需求契合度)**：是否嚴格在 brief 核准的品牌資料與產品規格內寫作，無擅自編造[cite: 2]？
2.  **Funnel Stage Fit (漏斗階段適配)**：是否將 BOFU 語氣誤用到 TOFU（如向冷受眾強推折扣促銷）[cite: 2, 7]？
3.  **Hook Strength (前三行吸睛度)**：第一行是否成功打斷滑手機的機械慣性，引發無意識好奇[cite: 3, 4, 5]？
4.  **Offer Clarity (方案清晰度)**：受眾能否在一秒內看清自己能得到什麼、要付多少錢，無困惑[cite: 4, 7]？
5.  **Shopper Tension (阻力破冰度)**：是否主動指出並化解了顧客加購/抉擇前的心理阻力與隱形疑慮[cite: 4, 7]？
6.  **Offer-to-Action Translation (活動轉譯度)**：是否給出了多買一件、或現在立刻帶走的具體行動理由[cite: 2, 4, 7]？
7.  **Creative Context Fit (素材互補度)**：文案 Headline 是否在補足決策 Cue，而非重複素材字卡廢話[cite: 7]？
8.  **Platform Fit (平台通路適配)**：格式與排版是否符合該平台（如 Meta 3行斷行約束、 LINE 20字元限制）[cite: 3]？
9.  **Brand Fit (品牌調性符合度)**：是否符合指定語氣（如高級感品牌絕不出現廉價促銷詞）[cite: 3, 7]。
10. **Specificity (具體細節度)**：是否用具體的動詞、時間、數字，替換掉了空泛抽象的形容詞[cite: 2, 4, 7]。
11. **Taiwan Social Language (台灣社群語感)**：是否使用了在地、有畫面感的生活與工作流口語（如：出包、雷品）[cite: 5]。
12. **Non-Generic Quality (去 AI 罐頭度)**：是否完全過濾掉了「不僅……更是……、讓我們一起、點燃激情」[cite: 3, 5, 7]。
13. **Claim Safety (宣稱合規安全)**：是否完全排除了假稀缺、假截止日、及違反藥事法/公平法的極端宣稱[cite: 2, 4, 5]。
14. **Actionability (下一步指引性)**：結尾的行動呼籲（CTA）是否明確清晰、從顧客角度出發、簡化行動難度[cite: 3, 4, 7]。

## 3. 終極判定關卡 (Final Gate Mechanism)
```yaml
final_gate:
  score_below_4: 
    status: blocked
    action: "強制打回改寫，對照 16_anti_ai_copy_rules 進行降噪與重寫[cite: 3, 5]。"
  score_4: 
    status: workflow_final_allowed_but_needs_human_live_check
    action: "允許上稿，但必須在後台加註提示：『利益到意義轉譯稍弱，建議投手人工檢核』[cite: 2]。"
  score_5: 
    status: strong_candidate_but_still_requires_claim_and_lp_check
    action: "優秀候選稿件。進入最終 Live-Ready 判定機制。"

live_ready_rules:
  lp_unavailable: false                # 當 Landing Page 無法讀取時，嚴禁 Live-Ready 上稿[cite: 2, 7]
  creative_unavailable: false          # 當未對齊素材圖卡時，嚴禁 Live-Ready 上稿[cite: 7]
  unsupported_claims_present: false   # 只要出現 brief 找不到的未驗證數據，直接判定 Live-Ready = false[cite: 2]
  offer_terms_unverified: false       # 只要活動促銷條款未經法遵/法務核准，直接判定 Live-Ready = false[cite: 2]