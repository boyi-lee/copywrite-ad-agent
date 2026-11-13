from pathlib import Path
import importlib.util
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_copy.py"
SPEC = importlib.util.spec_from_file_location("validate_copy", MODULE_PATH)
VALIDATE_COPY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATE_COPY)


def payload(primary_text: str) -> dict:
    return {
        "campaign_brief": {"platform": "meta", "ad_format": "feed"},
        "meta_copies": [
            {
                "variant_name": "A",
                "angle_id": "angle-01",
                "primary_text": primary_text,
                "headline": "夏季球裝",
                "description": "查看系列",
                "call_to_action": "Shop Now",
                "destination_button_text": "",
            }
        ],
    }


def ash_payload(primary_text: str) -> dict:
    value = payload(primary_text)
    value["campaign_brief"].update(
        {
            "brand": "ASH GOLF",
            "audience": {
                "identity": "固定下場的球友",
                "situation": "夏季下場",
                "dissatisfaction": "不想穿得制式",
                "purchase_motivation": "兼顧活動需求與造型",
                "product_expectation": "看出值得點進去的理由",
            },
            "usp_fed": [
                {
                    "feature": "活動彈性版型",
                    "evidence": "商品頁",
                    "desire": "揮桿時活動自在",
                    "purchase_reason": "外型與實穿性兼顧",
                }
            ],
        }
    )
    return value


def ecommerce_payload(primary_text: str) -> dict:
    value = payload(primary_text)
    value["campaign_brief"].update(
        {
            "funnel_stage": "MOFU",
            "audience_state": "正在比較補水用品的消費者",
            "buying_task": "比較商品差異並決定是否替換現有水壺",
        }
    )
    value["meta_copies"][0].update(
        {
            "funnel_stage": "MOFU",
            "shopper_tension": "不確定是否值得替換現有水壺",
            "comparison_standard": "比較攜帶便利性與實際使用情境",
            "product_feature": "可隨身攜帶",
            "feature_translation": "讓外出補水更容易安排",
            "objection_handling": "先查看商品細節再決定",
            "proof_available": [{"type": "product_page", "source": "https://example.com/product"}],
            "offer_reason": "查看商品選項後再比較",
            "next_action": "查看商品細節",
            "scene_anchor": {"scene_text": "出門補水", "copy_quote": "出門補水"},
            "plain_language_product_help": "查看商品細節",
            "technical_term_translations": [],
        }
    )
    value["meta_copies"][0]["primary_text"] = primary_text + "\n\n查看商品細節。\n\n再決定是否替換。"
    value["campaign_brief"].update(
        {
            "task_type": "ecommerce_product_copy",
            "ecommerce_copy_check": {
                "audience_problem": "夏季出門時不想帶著厚重水壺",
                "use_moment": "通勤與外出補水",
                "product_help": "讓補水用品更容易隨手帶著",
                "proof_available": [
                    {"type": "product_page", "source": "https://example.com/product"}
                ],
                "objection": "不確定是否值得替換現有水壺",
                "next_action": "查看商品細節",
            },
        }
    )
    return value


def collection_payload(primary_text: str) -> dict:
    value = payload(primary_text)
    value["campaign_brief"].update(
        {
            "task_type": "ecommerce_collection_ad",
            "ad_format": "collection",
            "collection_ad_evidence": {
                "asset_to_products": [
                    {
                        "asset_id": "creative-01",
                        "product_anchor": "涼感運動上衣",
                        "source_url": "https://example.com/cooling-top",
                        "source_excerpt": "涼感運動上衣商品頁",
                    }
                ],
                "conversion_lever": {
                    "type": "use_case",
                    "source": "https://example.com/cooling-top",
                    "evidence": "夏季活動時穿著的涼感系列",
                },
                "shopper_tension": "天熱活動時不想讓衣服黏在身上",
                "decision_to_make": "挑選夏季活動會穿的上衣",
                "angle_groups": [{
                    "angle_id": "angle-01",
                    "product_anchor": "涼感運動上衣",
                    "source_evidence": [{"source_url": "https://example.com/cooling-top", "locator": "商品頁", "excerpt": "涼感運動上衣商品頁"}],
                    "shopper_problem": "天熱活動時不想讓衣服黏在身上",
                    "use_moment": "夏季活動時穿著",
                    "product_feature": "涼感運動上衣",
                    "felt_outcome": "更容易挑選夏季活動上衣",
                    "purchase_reason": "查看涼感運動上衣商品細節",
                    "brand_removed_copy": "查看涼感運動上衣商品細節",
                    "could_fit_another_brand": False,
                    "distinct_from_other_angles": True
                }]
            },
        }
    )
    value["campaign_brief"].update(
        {
            "funnel_stage": "MOFU",
            "audience_state": "正在比較夏季活動服裝的消費者",
            "buying_task": "比較商品差異並挑選適合的上衣",
        }
    )
    value["meta_copies"][0].update(
        {
            "funnel_stage": "MOFU",
            "shopper_tension": "天熱活動時不想讓衣服黏在身上",
            "comparison_standard": "比較夏季活動時的穿著需求",
            "product_feature": "涼感運動上衣",
            "feature_translation": "作為夏季活動時的選擇依據",
            "objection_handling": "先查看商品細節再決定",
            "proof_available": [{"type": "product_page", "source": "https://example.com/cooling-top"}],
            "offer_reason": "查看商品選項後再比較",
            "next_action": "查看商品細節",
            "scene_anchor": {"scene_text": "天熱", "copy_quote": "天熱"},
            "plain_language_product_help": "查看商品細節",
            "technical_term_translations": [],
        }
    )
    value["meta_copies"][0]["primary_text"] = primary_text + "\n\n查看商品細節。\n\n再決定是否挑選。"
    return value


def staged_payload(stage: str, primary_text: str = "第一行。\n\n第二行。\n\n第三行。") -> dict:
    value = payload(primary_text)
    value["campaign_brief"].update(
        {
            "task_type": "ecommerce_product_copy",
            "funnel_stage": stage,
            "audience_state": "正在比較商品的消費者",
            "buying_task": "比較商品差異並決定下一步",
            "ecommerce_copy_check": {
                "audience_problem": "需要做出商品選擇",
                "use_moment": "實際使用時",
                "product_help": "提供選擇依據",
                "proof_available": [{"type": "product_page", "source": "https://example.com/product"}],
                "objection": "不確定是否值得購買",
                "next_action": "查看商品細節",
            },
        }
    )
    fields = {
        "TOFU": {
            "problem_scene": "遇到需要解決的使用情境",
            "hook_tension": "想知道問題是否與自己有關",
            "initial_product_help": "提供初步選擇方向",
            "soft_next_action": "查看使用情境",
        },
        "MOFU": {
            "shopper_tension": "正在比較不同商品",
            "comparison_standard": "比較商品差異與使用情境",
            "product_feature": "可驗證的商品特徵",
            "feature_translation": "把特徵轉成選擇依據",
            "objection_handling": "先查看細節再決定",
            "proof_available": "商品頁證據",
            "offer_reason": "查看商品選項後再比較",
            "next_action": "查看商品細節",
        },
        "BOFU": {
            "known_product_or_intent": "已經看過這項商品",
            "decision_blocker": "仍在猶豫是否現在購買",
            "verified_offer": "已驗證的活動內容",
            "risk_reducer": "先確認商品與購買條件",
            "reason_to_act_now": "現在查看已驗證的活動選項",
            "purchase_action": "進入商品頁購買",
        },
    }[stage]
    value["meta_copies"][0].update({"funnel_stage": stage, **fields, "scene_anchor": {"scene_text": "第一行", "copy_quote": "第一行"}, "plain_language_product_help": "第一行", "technical_term_translations": []})
    return value


class ApparelWordingTests(unittest.TestCase):
    def test_blocks_hard_supporting_wording(self) -> None:
        issues = VALIDATE_COPY.validate(payload("不用一雙鞋硬撐所有日常。"))
        self.assertTrue(any("硬撐" in issue for issue in issues))

    def test_blocks_stiff_apparel_wording(self) -> None:
        issues = VALIDATE_COPY.validate(payload("透氣孔幫助空氣流通。"))
        self.assertTrue(any("stiff or high-risk apparel wording" in issue for issue in issues))

    def test_allows_felt_and_motion_outcome(self) -> None:
        issues = VALIDATE_COPY.validate(payload("背部透氣孔讓熱氣散開，揮桿時少一層悶住的干擾。"))
        self.assertEqual([], issues)


class TaiwanConversionHardConstraintTests(unittest.TestCase):
    def test_blocks_newly_recorded_banned_terms(self) -> None:
        for term in ("無縫接軌", "俐落", "跟上行程", "為您帶來", "完美結合", "撐", "卡卡"):
            with self.subTest(term=term):
                self.assertTrue(VALIDATE_COPY.validate(payload(f"這段文案含有{term}。")))

    def test_blocks_whether_or_sentence_frame(self) -> None:
        issues = VALIDATE_COPY.validate(payload("無論是通勤還是出遊，這件都能穿。"))
        self.assertTrue(any("無論是…還是…" in issue for issue in issues))


class AshGolfValidationTests(unittest.TestCase):
    def test_requires_specific_audience_and_fed(self) -> None:
        value = payload("夏季下場，球衣要能活動，外型也要乾淨有型。")
        value["campaign_brief"]["brand"] = "ASH GOLF"
        issues = VALIDATE_COPY.validate(value)
        self.assertTrue(any("campaign_brief.audience" in issue for issue in issues))
        self.assertTrue(any("usp_fed" in issue for issue in issues))

    def test_blocks_recorded_weak_ash_hook(self) -> None:
        issues = VALIDATE_COPY.validate(ash_payload("球衣別讓你分心。"))
        self.assertTrue(any("ASH GOLF weak opening" in issue for issue in issues))

    def test_allows_specific_ash_hook_with_brief(self) -> None:
        issues = VALIDATE_COPY.validate(ash_payload("夏季下場，球衣要能活動，外型也要乾淨有型。"))
        self.assertEqual([], issues)


class EcommerceCopyValidationTests(unittest.TestCase):
    def test_requires_ecommerce_product_to_shopper_bridge(self) -> None:
        value = payload("出門補水，不想再把包包塞得很重。")
        value["campaign_brief"]["task_type"] = "ecommerce_product_copy"
        issues = VALIDATE_COPY.validate(value)
        self.assertTrue(any("ecommerce_copy_check is required" in issue for issue in issues))

    def test_requires_traceable_ecommerce_proof_pointer(self) -> None:
        value = ecommerce_payload("出門補水，不想再把包包塞得很重。")
        value["campaign_brief"]["ecommerce_copy_check"]["proof_available"] = [{"type": "product_page"}]
        issues = VALIDATE_COPY.validate(value)
        self.assertTrue(any("proof pointer needs type and source" in issue for issue in issues))

    def test_allows_complete_ecommerce_product_to_shopper_bridge(self) -> None:
        issues = VALIDATE_COPY.validate(ecommerce_payload("出門補水，不想再把包包塞得很重。"))
        self.assertEqual([], issues)


class CollectionAdValidationTests(unittest.TestCase):
    def test_requires_asset_product_mapping_and_conversion_lever(self) -> None:
        value = payload("展開精選集，看看新品。")
        value["campaign_brief"].update({"task_type": "ecommerce_collection_ad", "ad_format": "collection"})
        issues = VALIDATE_COPY.validate(value)
        self.assertTrue(any("collection_ad_evidence is required" in issue for issue in issues))

    def test_blocks_navigation_only_collection_copy_without_anchor(self) -> None:
        issues = VALIDATE_COPY.validate(collection_payload("展開精選集，把今天要穿的衣服一次選好。"))
        self.assertTrue(any("lacks a mapped product/category anchor" in issue for issue in issues))

    def test_allows_evidence_anchored_collection_copy(self) -> None:
        issues = VALIDATE_COPY.validate(
            collection_payload("天熱還要出門活動，先看涼感運動上衣，挑今天會穿到的那一件。")
        )
        self.assertEqual([], issues)


class FunnelStageValidationTests(unittest.TestCase):
    def test_scene_must_appear_in_consumer_copy(self) -> None:
        value = staged_payload("MOFU")
        value["meta_copies"][0]["scene_anchor"]["copy_quote"] = "球場上"
        issues = VALIDATE_COPY.validate(value)
        self.assertTrue(any("scene_anchor must appear" in issue for issue in issues))

    def test_technical_term_requires_plain_language_translation(self) -> None:
        value = staged_payload("MOFU")
        value["meta_copies"][0]["primary_text"] = "第一行彈道。\n\n第二行。\n\n第三行。"
        value["meta_copies"][0]["scene_anchor"] = {"scene_text": "第一行", "copy_quote": "第一行彈道"}
        value["meta_copies"][0]["plain_language_product_help"] = "第一行"
        issues = VALIDATE_COPY.validate(value)
        self.assertTrue(any("technical term '彈道'" in issue for issue in issues))

    def test_all_funnel_stages_require_stage_specific_fields(self) -> None:
        required = {
            "TOFU": "problem_scene",
            "MOFU": "comparison_standard",
            "BOFU": "decision_blocker",
        }
        for stage, field in required.items():
            with self.subTest(stage=stage):
                value = staged_payload(stage)
                value["meta_copies"][0].pop(field)
                issues = VALIDATE_COPY.validate(value)
                self.assertTrue(any("variant missing fields" in issue for issue in issues))

    def test_stage_contract_rejects_single_line_primary_text(self) -> None:
        issues = VALIDATE_COPY.validate(staged_payload("MOFU", "只有一句話的短文案。"))
        self.assertTrue(any("at least three scanable" in issue for issue in issues))

    def test_complete_tofu_mofu_bofu_contracts_pass(self) -> None:
        for stage in ("TOFU", "MOFU", "BOFU"):
            with self.subTest(stage=stage):
                self.assertEqual([], VALIDATE_COPY.validate(staged_payload(stage)))


if __name__ == "__main__":
    unittest.main()
