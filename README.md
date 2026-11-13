# copywrite-ad-agent

[繁體中文（預設）](README.md) ｜ [English](README.en.md)

以證據為先的電商文案 Skill，支援 Meta 廣告文案、創意 Brief、商品研究與文案審核。它會結合品牌與商品資料，透過結構化規劃、確定性檢查與獨立審核，協助產出可追溯的工作成果。

## 下載與安裝

將 repo 直接複製到 Codex Skills 資料夾：

```bash
git clone https://github.com/boyi-lee/copywrite-ad-agent.git ~/.codex/skills/copywrite-ad-agent
```

也可以在 GitHub 選擇 **Code → Download ZIP**，解壓後將整個 repo 放入 `~/.codex/skills/copywrite-ad-agent/`。repo 根目錄就是 Skill 根目錄，請保留 `SKILL.md`、`agents/`、`knowledge/`、`references/`、`schemas/`、`scripts/`、`templates/` 與 `tests/`。

Skill 名稱為 `copywrite-ad-agent`，呼叫中繼資料位於 `agents/openai.yaml`。請先閱讀 [SKILL.md](SKILL.md)：它是正式流程與權限邊界的主要文件。

## 功能與流程

### 電商文案撰寫、改寫與審核

1. 蒐集當前商品、活動、著陸頁與素材證據。
2. 建立受眾與購買角度假設，清楚區分假設和已驗證事實。
3. 依任務與流程需要，先預覽策略並取得角度確認。
4. 針對選定角度撰寫文案，再檢查宣稱及平台、漏斗要求。
5. 將當前草稿、證據與評分規準交由獨立審核；確認審核流程完成後再交付。

策略預覽不是可直接上線的文案。流程檢查通過也不代表廣告成效、平台政策核准或已發布。

### Google 試算表用 Meta 創意 Brief

這是與成品廣告文案分開的流程。Skill 會建立結構化 Brief、檢查完整資料集，並在寫入試算表前進行審核。只有通過檢查且目的地已獲授權後才會寫入；完成後會讀回資料列驗證結果。

## 採用的行銷原理

這個 Skill 把行銷原理作為**分析與規劃工具**，依任務選用，不會要求每篇文案套用同一個公式。

| 原理類別 | README 導覽 | 用途 |
|---|---|---|
| 受眾意圖與基本文案原則 | [通用文案原則](references/copy-knowledge-pack/01_universal_copywriting_principles.md) | 從受眾當下的意圖、問題或阻力出發；把產品特點連到利益與顧客在意的結果；辨認並回應疑慮。 |
| 說服與訊息框架 | [說服框架](references/copy-knowledge-pack/02_persuasion_frameworks.md)、[訊息結構](references/copy-knowledge-pack/06_message_structure_patterns.md) | 包含 TIPS、PAS、BAB、FAB 等框架，以及異議處理結構；用來整理訊息，不是必須照抄的固定模板。 |
| 受眾動機與心理 | [受眾意圖與心理](references/copy-knowledge-pack/03_audience_intent_and_psychology.md)、[角度矩陣](references/creative-angle-matrix.md) | 探索購買動機、使用情境、顧客張力、預期進展與不同購買理由；受眾推論須標示為假設。 |
| 價值、優惠與 USP | [價值與方案轉譯](references/copy-knowledge-pack/04_offer_and_value_translation.md)、[USP 轉譯規則](references/usp-translation-rules.md)、[電商文案指南](knowledge/ecommerce-copywriting-playbook.md) | 把特點連到功能利益、使用情境、可能的感受與購買理由；優惠與急迫性必須有當前來源支持。 |
| 注意力與開場 | [Hook 與注意力模式](references/copy-knowledge-pack/05_hook_and_attention_patterns.md) | 提供提問、情境、反差與警示等開場選項；是否使用要看受眾、素材和證據，不以吸睛為由誇大。 |
| 漏斗與渠道情境 | [漏斗文案規則](references/copy-knowledge-pack/07_funnel_copy_rules.md)、[平台適配](references/copy-knowledge-pack/08_platform_adaptation_rules.md)、[產業適配](references/copy-knowledge-pack/09_industry_adaptation_rules.md) | 依 TOFU／MOFU／BOFU 等決策階段及平台版位，調整資訊深度、證據與下一步行動。 |
| 素材與欄位分工 | [Meta 格式指南](references/meta-formats.md)、[視覺流程規則](references/visual-flow-rules.md) | 讓素材、主文案、標題、說明和 CTA 接續溝通，減少重複訊息。 |

### 使用原理時的界線

- 框架名稱本身不代表有證據，也不證明某角度有效；[角度矩陣](references/creative-angle-matrix.md)要求以實際購買理由判斷角度差異。
- 心理、受眾、需求和購買動機若未由顧客資料證實，應保持為假設，不可寫成市場事實。
- 商品規格、優惠、庫存、見證、比較及成效宣稱都要回到當前來源；一般行銷原理不能補足缺少的商品證據。
- 知識包提供跨產業範例和候選做法，需依品牌、商品、平台與法規情境判斷適用性；不適用的框架可以不用。

## 資料來源與使用界線

- 當前來源證據優先於歷史範例與品牌學習內容。
- [creative-angle-matrix.md](references/creative-angle-matrix.md) 是角度定義、數量處理、差異性與確認流程的唯一依據；相容性文件應回指此文件。
- `references/brands/` 存放維護中的品牌資料；`knowledge/` 存放電商指引與品牌失誤模式學習。
- 機器檢查可驗證結構、雜湊與必要欄位，但不能單獨證明宣稱真實或審核者身分。
- 本 Skill 不會發布廣告、不會寫入廣告帳戶，也不會寫入 Shopify。

此 repo 含品牌專屬資料與歷史學習內容。採用前，請先檢視這些材料，並確認適合你的組織與用途。

## 依任務找到檔案

| 任務 | 從這裡開始 | 相關文件 |
|---|---|---|
| 電商廣告文案 | [SKILL.md](SKILL.md) | [電商文案指南](knowledge/ecommerce-copywriting-playbook.md)、[角度矩陣](references/creative-angle-matrix.md)、`references/copy-knowledge-pack/` 的漏斗與平台規則、[品質契約](references/creative-quality-contract.md)、[驗證契約](references/validation-contract.md) |
| Meta 文案與改寫 | [SKILL.md](SKILL.md) | [Meta 審核循環](references/meta-conversion-review-loop.md)、[格式指南](references/meta-formats.md) |
| 品牌專屬文案 | `references/brands/<brand>.md` | `knowledge/` 中相應的失誤模式筆記；所有宣稱仍須用當前證據確認 |
| 商品研究與 USP 證據 | [商品研究流程](references/product-research-loop.md) | [驗證規準](references/product-research-verification-rubric.md)、`schemas/product-research-output.schema.json`、`scripts/validate_product_research.py` |
| Meta 創意 Brief | [SKILL.md](SKILL.md) 的 Brief 流程 | [Brief 審核規則](references/creative-brief-review-adaptation.md)、`schemas/creative-brief-set.schema.json`、`schemas/creative-brief-review.schema.json`、`scripts/validate_creative_brief.py` |
| Google RSA 文案 | [Google RSA 指引](references/google-rsa.md) | `references/copy-knowledge-pack/08_platform_adaptation_rules.md`、`scripts/validate_copy.py` |
| 維護工作流程 | [流程協調器](scripts/copy_orchestrator.py) | `schemas/`、`templates/` 及 `tests/` 中相對應的回歸測試 |

## 資料夾結構

```text
copywrite-ad-agent/
├── SKILL.md       # 流程入口與使用界線
├── agents/        # Skill 呼叫中繼資料
├── knowledge/     # 電商指引與品牌學習
├── references/    # 品牌、平台、研究與品質規則
├── schemas/       # 機器可讀的資料契約
├── scripts/       # 流程協調、研究與驗證器
├── templates/     # 執行紀錄起始範本
├── tests/         # 回歸測試與測試資料
├── README.md      # 繁體中文主文件
└── README.en.md   # 英文版說明
```

## 驗證套件

在 repo 根目錄執行：

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts tests
for f in schemas/*.json; do python3 -m json.tool "$f" >/dev/null || exit 1; done
python3 scripts/review_quality_upgrade.py standards
python3 scripts/review_quality_upgrade.py spec
```

預期結果：所有單元測試通過、Python 編譯成功、每個 schema 都能解析為 JSON，且兩個 review 指令都回報 `"verdict": "pass"`。這些檢查涵蓋本機結構與回歸要求，不會驗證線上商品宣稱、廣告成效、平台政策核准或發布狀態。

## 版本與發布狀態

此 repo 同步目前已安裝的 Skill 快照。尚無已驗證的版本標籤，因此它是未編號的來源副本，不代表正式穩定版本。建立或散布新版本前，請閱讀[版本識別與回復說明](references/candidate-release-and-rollback.md)。

---

[English documentation](README.en.md)
