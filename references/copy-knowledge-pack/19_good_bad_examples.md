# 跨產業好壞文案案例庫 (Good & Bad Examples)

## 模組說明
本檔案提供 AI Agent 針對各種文案任務（Hooks, BOFU lines, Promos, Descriptions, Headlines）進行自我審核與比對的對照標準。

## 1. Good & Bad Hooks (開場前三行對照)

### example:
  type: Bad hook
  industry: 醫美保健
  platform: Meta Ads
  funnel_stage: TOFU
  copy_task: 廣告主文案開場
  text: 「【熱銷推薦】我們為您提供最專業、效果最明顯的保濕原液，採用頂級原料，能完美融合肌膚，是您護膚的不二選擇。」[cite: 3, 7]
  why_good_or_bad: 典型的 AI 味官網腔[cite: 3, 5, 7]；充斥著「最專業、完美融合、不二選擇」等無法驗證的空泛形容詞，讀者大腦會直接將其判定為廢話直接略過[cite: 2, 3, 7]。
  applicable_context: 無（此為負面典型）。
  caution: 嚴禁 AI 在任何 TOFU 文案中生成此類句型[cite: 2, 7]。

### example:
  type: Good hook
  industry: 美妝時尚
  platform: Meta Ads
  funnel_stage: TOFU
  copy_task: 廣告主文案開場
  text: 「熬夜加班到深夜，隔天早起照鏡子，皮膚暗沉鬆弛得像老了十歲？（皮膚科醫生：盲目擦面霜沒用，你臉上的精華有 90% 都因為毛孔鈍感而白用了）[cite: 2, 4, 5]」
  why_good_or_bad: 運用「假性篩選法」與非常有畫面感的動詞描述（照鏡子、暗沉鬆弛得像老了十歲），一針見血地指出痛苦元凶，成功引發強烈共鳴與邊緣系統恐懼[cite: 4, 5]。
  applicable_context: 所有美妝、保健、功能型快消品的冷受眾開場文案[cite: 2, 4, 7]。
  caution: 後方必須立刻用科學原理解釋「為什麼有90%白用了」，建立專家人設[cite: 2, 4]。

## 2. Good & Bad BOFU lines (再行銷與猶豫處理對照)

### example:
  type: Bad BOFU line
  industry: 線上課程
  platform: Landing Page
  funnel_stage: BOFU
  copy_task: 催單段落
  text: 「【限時促銷】您放入購物車的寫作課程正在舉辦感恩特價優惠中！錯過不再，趕快點擊下方網址進行購買吧！」[cite: 2, 3, 7]
  why_good_or_bad: 觸犯了最高扣分規則（Max 3分限制）：只生硬地公告了活動折扣 Offer，卻完全沒有將優惠轉譯為「現在立刻回歸帶走的具體行動理由」，無法消除花錢罪惡感[cite: 2, 4, 7]。
  applicable_context: 無（此為負面典型）。
  caution: AI 在審查 BOFU 文案時，若發現此類純公告語氣，必須強制打回改寫。

### example:
  type: Good BOFU line
  industry: 線上課程
  platform: Landing Page
  funnel_stage: BOFU
  copy_task: 催單段落
  text: 「【尺寸/更換免費保證】你上週留在購物車裡的那堂寫作課，是不是還在讓你猶豫？別擔心，不該讓顧客承擔風險。我們提供 30 天不滿意全額退款保證。也就少吃一頓火鍋的代價，現在帶走，剛好利用這週末的空閒時間把個人品牌的第一個藍圖無風險補齊[cite: 2, 3, 4, 5, 7]。」
  why_good_or_bad: 嚴格執行了 4R 成交準則[cite: 3]：主動拔刺指出猶豫（是不是還在讓你猶豫？），給予無風險退款承諾降低決策成本，並用心理帳戶偷換（少吃一頓火鍋對比個人品牌藍圖）消除了花錢罪惡感[cite: 3, 4, 5]。
  applicable_context: 所有高/低單價數位產品、教育課程、或訂閱制服務的再行銷與加購催單文案[cite: 2, 4, 7]。
  caution: 必須確認後台是否有提供對應的退換貨或退款服務事實支持（Claim Safety）。

## 3. Good & Bad Descriptions (說明與規格轉譯對照)

### example:
  type: Bad description
  industry: B2B SaaS
  platform: 商品頁
  funnel_stage: MOFU
  copy_task: 產品特點功能說明
  text: 「本軟體內置高速雲端運算架構與 AI 智能數據分析模組，系統穩定、安全性高，是企業數位轉型不可或缺的卓越利器。」[cite: 3, 7]
  why_good_or_bad: 嚴重的專家盲點（知識的詛詛）：通篇死板地羅列技術名詞（雲端運算架構、智能數據分析模組），卻完全不肯告訴受眾這個技術在具體工作流中能幫其解決什麼困難，聽起來非常乾巴無趣[cite: 2, 4, 7]。
  applicable_context: 無（此為負面典型）。
  caution: 嚴禁 AI 直接將 Brief 中的硬核規格死板貼出。

### example:
  type: Good description
  industry: B2B SaaS
  platform: 商品頁
  funnel_stage: MOFU
  copy_task: 產品特點功能說明
  text: 「你不需要自己去想辦法、也不需要懂任何一條代碼（降低行動成本）[cite: 4, 7]。研發團隊在冷氣房裡研究了市面上 100 多款對帳軟體，打樣了 100 多次，才定下這個高分子自動化算法（費時費力代價）[cite: 2, 4]。月底結帳時，原本需要會計人工核對 3 天的繁雜帳目，系統會在 30 秒內自動比對完成，這意味著你的經理有空專注在真正能幫公司獲利的業務上（利益/意義雙重轉譯）[cite: 2, 4, 5, 7]。」
  why_good_or_bad: 嚴格執行了「3+5賣點直白翻譯模型」與「費時費力代價原則」，用大白話和具體的生活/工作場景描述（對帳 3 天縮短為 30 秒），成功將生硬的規格轉化為極強的組織效率獲得感[cite: 2, 4, 7]。
  applicable_context: 所有軟體、系統、 MarTech 數位產品或專業技術服務的功能價值轉譯文案[cite: 2, 4, 7]。
  caution: 獲得感描述必須精準對齊目標客群（弗雷德）在意的點[cite: 4]。