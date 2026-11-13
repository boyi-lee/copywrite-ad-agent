#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


AI_GENERIC_TERMS = [
    "打造質感生活",
    "升級你的日常",
    "升級你的運動日常",
    "展現你的風格",
    "專屬於你的",
    "不容錯過",
    "立即入手",
    "質感首選",
    "完美結合",
    "舒適與時尚兼具",
    "每一步都精彩",
    "每一步都自在",
    "你的最佳選擇",
    "無縫接軌",
    "俐落",
    "跟上行程",
    "為您帶來",
]
APPAREL_STIFF_PHRASES = [
    "每一項都在考驗衣服",
    "幫助空氣流通",
    "接住日常穿搭",
    "接住球場後的行程",
    "微蓬鬆版型",
]

DEFAULT_BANNED_PATTERNS = [
    ("最怕…", re.compile(r"最怕")),
    ("硬撐", re.compile(r"硬撐")),
    (
        "不是…是…",
        re.compile(r"不是[^\n。！？]{0,60}[，,；;]?\s*(?:而)?是"),
    ),
    (
        "無論是…還是…",
        re.compile(r"無論是[^\n。！？]{0,60}(?:，|,)?\s*還是"),
    ),
]

DEFAULT_BANNED_TERMS = ["撐", "卡卡"]

CONSUMER_META_COMMENTARY_PATTERNS = [
    re.compile(r"(?:不用|不必|別)看(?:一堆|一串|一長串)?(?:產品)?(?:規格|布料名稱|專業名詞|技術名詞)"),
    re.compile(r"(?:不用懂|不必懂|不用了解|不必了解)(?:產品)?(?:規格|布料名稱|專業名詞|技術名詞)"),
    re.compile(r"(?:先不談|不談)(?:產品)?(?:規格|布料名稱|專業名詞|技術名詞)"),
]

SCARCITY_TERMS = [
    "所剩無幾",
    "最後庫存",
    "庫存告急",
    "即將售罄",
    "售完不補",
    "斷碼",
    "搶完",
]
CAROUSEL_FORMATS = {"carousel", "catalog", "carousel/catalog", "輪播", "目錄"}
COLLECTION_FORMATS = {
    "collection",
    "instant experience",
    "instant_experience",
    "精選集",
    "即時體驗",
}
ASH_GOLF_BRAND_NAMES = {"ash golf", "ashgolf"}
ASH_REQUIRED_AUDIENCE_FIELDS = {
    "identity",
    "situation",
    "dissatisfaction",
    "purchase_motivation",
    "product_expectation",
}
ASH_WEAK_OPENINGS = [
    "打完一場，今天的行程還沒結束。",
    "太陽正曬，球衣更要穿得輕。",
    "球衣別讓你分心。",
    "悶熱比體力更早拖慢節奏。",
    "夏天打球，穿著狀態也很重要。",
]
ECOMMERCE_TASK_TYPES = {"ecommerce_product_copy", "ecommerce"}
COLLECTION_AD_TASK_TYPES = {"ecommerce_collection_ad", "collection_ad"}
ECOMMERCE_CHECK_FIELDS = {
    "audience_problem",
    "use_moment",
    "product_help",
    "proof_available",
    "objection",
    "next_action",
}
COLLECTION_AD_EVIDENCE_FIELDS = {
    "asset_to_products",
    "conversion_lever",
    "shopper_tension",
    "decision_to_make",
}
COLLECTION_ANGLE_FIELDS = {
    "angle_id",
    "product_anchor",
    "source_evidence",
    "shopper_problem",
    "use_moment",
    "product_feature",
    "felt_outcome",
    "purchase_reason",
    "brand_removed_copy",
    "could_fit_another_brand",
    "distinct_from_other_angles",
}
FUNNEL_STAGES = {"TOFU", "MOFU", "BOFU"}
FUNNEL_BRIEF_FIELDS = {"funnel_stage", "audience_state", "buying_task"}
FUNNEL_VARIANT_FIELDS = {
    "TOFU": {"problem_scene", "hook_tension", "initial_product_help", "soft_next_action"},
    "MOFU": {
        "shopper_tension", "comparison_standard", "product_feature", "feature_translation",
        "objection_handling", "proof_available", "offer_reason", "next_action",
    },
    "BOFU": {
        "known_product_or_intent", "decision_blocker", "verified_offer", "risk_reducer",
        "reason_to_act_now", "purchase_action",
    },
}
TECHNICAL_TERMS = ("尾部配重", "配重模組", "桿面角度", "著地角度", "可調式桿頸", "Ai10x", "彈道")


def is_ash_golf(brief: dict[str, Any]) -> bool:
    return str(brief.get("brand", brief.get("brand_name", ""))).strip().lower() in ASH_GOLF_BRAND_NAMES


def is_ecommerce_product_copy(brief: dict[str, Any]) -> bool:
    return str(brief.get("task_type", "")).strip().lower() in ECOMMERCE_TASK_TYPES


def is_ecommerce_collection_ad(brief: dict[str, Any]) -> bool:
    return str(brief.get("task_type", "")).strip().lower() in COLLECTION_AD_TASK_TYPES


def validate_collection_ad_evidence(brief: dict[str, Any]) -> list[str]:
    evidence = brief.get("collection_ad_evidence")
    if not isinstance(evidence, dict):
        return ["Ecommerce Collection ad: campaign_brief.collection_ad_evidence is required."]

    issues: list[str] = []
    missing = sorted(
        field
        for field in COLLECTION_AD_EVIDENCE_FIELDS
        if field not in {"asset_to_products", "conversion_lever"} and not str(evidence.get(field, "")).strip()
    )
    if missing:
        issues.append(f"Ecommerce Collection ad: missing evidence fields: {', '.join(missing)}.")

    mappings = evidence.get("asset_to_products")
    if not isinstance(mappings, list) or not mappings:
        issues.append("Ecommerce Collection ad: at least one asset_to_products mapping is required.")
    elif not any(
        isinstance(item, dict)
        and all(str(item.get(field, "")).strip() for field in ("asset_id", "product_anchor", "source_url", "source_excerpt"))
        for item in mappings
    ):
        issues.append("Ecommerce Collection ad: each usable mapping needs asset_id, product_anchor, source_url, and source_excerpt.")

    lever = evidence.get("conversion_lever")
    if not isinstance(lever, dict) or not all(
        str(lever.get(field, "")).strip() for field in ("type", "source", "evidence")
    ):
        issues.append("Ecommerce Collection ad: conversion_lever needs type, source, and evidence.")

    angles = evidence.get("angle_groups")
    if not isinstance(angles, list) or not angles:
        issues.append("Ecommerce Collection ad: angle_groups with product-level USP evidence is required.")
    else:
        seen_ids: set[str] = set()
        seen_reasons: set[str] = set()
        for index, angle in enumerate(angles, start=1):
            if not isinstance(angle, dict):
                issues.append(f"Ecommerce Collection ad: angle_groups item {index} must be an object.")
                continue
            missing = sorted(field for field in COLLECTION_ANGLE_FIELDS if field not in angle)
            if missing:
                issues.append(f"Ecommerce Collection ad: angle {index} missing fields: {', '.join(missing)}.")
                continue
            angle_id = str(angle.get("angle_id", "")).strip()
            if not angle_id or angle_id in seen_ids:
                issues.append(f"Ecommerce Collection ad: angle {index} needs a unique angle_id.")
            seen_ids.add(angle_id)
            if not isinstance(angle.get("source_evidence"), list) or not angle["source_evidence"]:
                issues.append(f"Ecommerce Collection ad: angle {angle_id} needs source_evidence.")
            if angle.get("could_fit_another_brand") is not False:
                issues.append(f"Ecommerce Collection ad: angle {angle_id} fails brand-distinctiveness check.")
            if angle.get("distinct_from_other_angles") is not True:
                issues.append(f"Ecommerce Collection ad: angle {angle_id} is not marked distinct from other angles.")
            reason = str(angle.get("purchase_reason", "")).strip()
            if not reason:
                issues.append(f"Ecommerce Collection ad: angle {angle_id} needs a specific purchase_reason.")
            elif reason in seen_reasons:
                issues.append(f"Ecommerce Collection ad: angle {angle_id} repeats another angle's purchase_reason.")
            seen_reasons.add(reason)
    return issues


def validate_ecommerce_copy_check(brief: dict[str, Any]) -> list[str]:
    check = brief.get("ecommerce_copy_check")
    if not isinstance(check, dict):
        return ["Ecommerce product copy: campaign_brief.ecommerce_copy_check is required."]

    missing = sorted(
        field
        for field in ECOMMERCE_CHECK_FIELDS
        if field != "proof_available" and not str(check.get(field, "")).strip()
    )
    issues: list[str] = []
    if missing:
        issues.append(f"Ecommerce product copy: missing copy-check fields: {', '.join(missing)}.")

    proof_available = check.get("proof_available")
    if not isinstance(proof_available, list) or not proof_available:
        issues.append("Ecommerce product copy: at least one proof_available evidence pointer is required.")
    elif not any(
        isinstance(item, dict)
        and str(item.get("type", "")).strip()
        and str(item.get("source", "")).strip()
        for item in proof_available
    ):
        issues.append("Ecommerce product copy: each usable proof pointer needs type and source.")
    return issues


def validate_ash_golf_brief(brief: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    audience = brief.get("audience")
    if not isinstance(audience, dict):
        issues.append("ASH GOLF: campaign_brief.audience must provide the named golfer and buying context.")
    else:
        missing = sorted(field for field in ASH_REQUIRED_AUDIENCE_FIELDS if not str(audience.get(field, "")).strip())
        if missing:
            issues.append(f"ASH GOLF: audience is too broad; missing fields: {', '.join(missing)}.")

    usp_fed = brief.get("usp_fed")
    if not isinstance(usp_fed, list) or not usp_fed:
        issues.append("ASH GOLF: at least one source-backed usp_fed entry is required.")
    elif not any(
        isinstance(item, dict)
        and all(str(item.get(field, "")).strip() for field in ("feature", "evidence", "desire", "purchase_reason"))
        for item in usp_fed
    ):
        issues.append("ASH GOLF: each usable usp_fed entry needs feature, evidence, desire, and purchase_reason.")
    return issues


def validate_funnel_contract(brief: dict[str, Any], variant: dict[str, Any]) -> list[str]:
    """Require stage-specific reasoning for ecommerce outputs without conflating it with platform length."""
    task_type = str(brief.get("task_type", "")).strip().lower()
    stage = str(variant.get("funnel_stage") or brief.get("funnel_stage") or "").strip().upper()
    if task_type not in ECOMMERCE_TASK_TYPES and not stage:
        return []

    issues: list[str] = []
    if stage not in FUNNEL_STAGES:
        issues.append("Funnel contract: funnel_stage must be TOFU, MOFU, or BOFU.")
        return issues

    if task_type in ECOMMERCE_TASK_TYPES:
        missing_brief = sorted(field for field in FUNNEL_BRIEF_FIELDS if not str(brief.get(field, "")).strip())
        if missing_brief:
            issues.append(f"Funnel {stage}: campaign_brief missing fields: {', '.join(missing_brief)}.")

    def missing_value(field: str) -> bool:
        value = variant.get(field)
        if isinstance(value, list):
            return not value
        return not str(value or "").strip()

    missing_variant = sorted(field for field in FUNNEL_VARIANT_FIELDS[stage] if missing_value(field))
    if missing_variant:
        issues.append(f"Funnel {stage}: variant missing fields: {', '.join(missing_variant)}.")

    primary = str(variant.get("primary_text", "")).strip()
    scene = variant.get("scene_anchor")
    if not isinstance(scene, dict) or not str(scene.get("scene_text", "")).strip() or not str(scene.get("copy_quote", "")).strip():
        issues.append(f"Funnel {stage}: scene_anchor requires scene_text and copy_quote.")
    elif scene["copy_quote"] not in primary or scene["scene_text"] not in primary:
        issues.append(f"Funnel {stage}: scene_anchor must appear in primary_text.")
    plain_help = str(variant.get("plain_language_product_help", "")).strip()
    if not plain_help or plain_help not in primary:
        issues.append(f"Funnel {stage}: plain_language_product_help must appear in primary_text.")
    translations = variant.get("technical_term_translations")
    if not isinstance(translations, list):
        issues.append(f"Funnel {stage}: technical_term_translations must be a list.")
        translations = []
    for term in TECHNICAL_TERMS:
        if term in primary and not any(
            isinstance(item, dict)
            and item.get("term") == term
            and str(item.get("plain_language", "")).strip()
            and item.get("plain_language") != term
            and str(item.get("copy_quote", "")).strip() in primary
            for item in translations
        ):
            issues.append(f"Funnel {stage}: technical term '{term}' needs an in-copy plain-language translation.")
    non_empty_lines = [line.strip() for line in primary.splitlines() if line.strip()]
    if len(non_empty_lines) < 3:
        issues.append(f"Funnel {stage}: primary_text needs at least three scanable content lines or blocks.")
    return issues


def first_non_empty_lines(text: str, count: int = 3) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines[:count])


def includes_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def validate_meta(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    brief = payload.get("campaign_brief", {})
    variants = payload.get("meta_copies", [])
    ad_format = str(brief.get("ad_format", "")).lower().strip()
    verified = " ".join(str(item) for item in brief.get("reason_to_act_now", []))
    visible_text = [str(item).strip() for item in brief.get("asset_visible_text", []) if str(item).strip()]
    phrases_to_avoid = [
        str(item).strip()
        for item in brief.get("phrases_to_avoid", [])
        if str(item).strip()
    ]

    if is_ash_golf(brief):
        issues.extend(validate_ash_golf_brief(brief))
    if is_ecommerce_product_copy(brief):
        issues.extend(validate_ecommerce_copy_check(brief))
    if is_ecommerce_collection_ad(brief):
        issues.extend(validate_collection_ad_evidence(brief))

    if not variants:
        issues.append("Meta output is missing.")
        return issues

    for index, variant in enumerate(variants, start=1):
        label = str(variant.get("variant_name") or index)
        issues.extend(validate_funnel_contract(brief, variant))
        primary = str(variant.get("primary_text", "")).strip()
        headline = str(variant.get("headline", "")).strip()
        description = str(variant.get("description", "")).strip()
        cta = str(variant.get("call_to_action", "")).strip()
        button = str(variant.get("destination_button_text", "")).strip()
        combined = " ".join([primary, headline, description, cta, button])

        if is_ecommerce_collection_ad(brief):
            mappings = brief.get("collection_ad_evidence", {}).get("asset_to_products", [])
            anchors = [
                str(item.get("product_anchor", "")).strip()
                for item in mappings
                if isinstance(item, dict) and str(item.get("product_anchor", "")).strip()
            ]
            if anchors and not any(anchor in f"{primary} {headline}" for anchor in anchors):
                issues.append(
                    f"Meta {label}: Collection ad lacks a mapped product/category anchor in primary_text or headline."
                )
            angle_id = str(variant.get("angle_id", "")).strip()
            angles = brief.get("collection_ad_evidence", {}).get("angle_groups", [])
            angle = next((item for item in angles if isinstance(item, dict) and item.get("angle_id") == angle_id), None)
            if angle is None:
                issues.append(f"Meta {label}: Collection ad variant must reference a valid angle_id.")
            else:
                anchor = str(angle.get("product_anchor", "")).strip()
                if anchor and anchor not in f"{primary} {headline}":
                    issues.append(f"Meta {label}: copy does not name its angle product/category anchor: {anchor}.")

        if not primary:
            issues.append(f"Meta {label}: primary_text is empty.")
        if is_ash_golf(brief):
            opening = first_non_empty_lines(primary, count=1)
            rejected_openings = [phrase for phrase in ASH_WEAK_OPENINGS if phrase in opening]
            if rejected_openings:
                issues.append(
                    f"Meta {label}: ASH GOLF weak opening detected: {', '.join(rejected_openings)}."
                )
        if len(headline) > 40:
            issues.append(f"Meta {label}: headline exceeds 40 characters ({len(headline)}).")

        unsupported = [term for term in SCARCITY_TERMS if term in combined and term not in verified]
        if unsupported:
            issues.append(f"Meta {label}: unverified scarcity claim: {', '.join(unsupported)}.")

        repeated = [text for text in visible_text if text and (text == headline or text == description)]
        if repeated:
            issues.append(f"Meta {label}: headline or description repeats visible asset text exactly.")

        primary_repeated = [text for text in visible_text if text and text in primary]
        if primary_repeated:
            issues.append(f"Meta {label}: primary_text contains visible asset text; ensure it adds a new buying reason: {', '.join(primary_repeated)}.")

        generic_terms = [term for term in AI_GENERIC_TERMS if term in combined]
        if generic_terms:
            issues.append(f"Meta {label}: high-risk AI/generic phrase detected: {', '.join(generic_terms)}.")

        banned_terms = [term for term in DEFAULT_BANNED_TERMS if term in combined]
        if banned_terms:
            issues.append(f"Meta {label}: banned Taiwan conversion term detected: {', '.join(banned_terms)}.")

        stiff_apparel_terms = [term for term in APPAREL_STIFF_PHRASES if term in combined]
        if stiff_apparel_terms:
            issues.append(
                f"Meta {label}: stiff or high-risk apparel wording detected: {', '.join(stiff_apparel_terms)}."
            )

        user_banned = [term for term in phrases_to_avoid if term in combined]
        if user_banned:
            issues.append(
                f"Meta {label}: user-banned phrase detected: {', '.join(user_banned)}."
            )

        banned_structures = [
            label_text
            for label_text, pattern in DEFAULT_BANNED_PATTERNS
            if pattern.search(combined)
        ]
        if banned_structures:
            issues.append(
                f"Meta {label}: banned sentence structure detected: {', '.join(banned_structures)}."
            )

        if any(pattern.search(combined) for pattern in CONSUMER_META_COMMENTARY_PATTERNS):
            issues.append(
                f"Meta {label}: consumer-facing writing or technical-strategy commentary detected."
            )

        if ad_format in CAROUSEL_FORMATS and not includes_any(
            combined, ["滑", "比較", "逐款", "一格一格", "依序", "目錄"]
        ):
            issues.append(f"Meta {label}: carousel/catalog copy lacks swipe or comparison guidance.")

        if ad_format in COLLECTION_FORMATS and not includes_any(
            combined, ["精選", "逛", "打開", "往下", "挑", "一次看"]
        ):
            issues.append(f"Meta {label}: collection copy lacks curated browsing guidance.")

    return issues


def validate_google(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    rsa = payload.get("google_rsa", {}) or {}
    headlines = rsa.get("headlines", [])
    descriptions = rsa.get("descriptions", [])

    if len(headlines) != 15:
        issues.append(f"Google RSA requires exactly 15 headlines; got {len(headlines)}.")
    if len(descriptions) != 4:
        issues.append(f"Google RSA requires exactly 4 descriptions; got {len(descriptions)}.")
    for index, value in enumerate(headlines, start=1):
        if len(str(value)) > 30:
            issues.append(f"Google headline {index} exceeds 30 characters ({len(str(value))}).")
    for index, value in enumerate(descriptions, start=1):
        if len(str(value)) > 90:
            issues.append(f"Google description {index} exceeds 90 characters ({len(str(value))}).")
    if len(set(str(value).strip() for value in headlines)) != len(headlines):
        issues.append("Google RSA contains duplicate headlines.")
    return issues


def validate(payload: dict[str, Any]) -> list[str]:
    platform = str(payload.get("campaign_brief", {}).get("platform", "both")).lower()
    issues: list[str] = []
    if platform in {"meta", "facebook", "both", ""}:
        issues.extend(validate_meta(payload))
    if platform in {"google", "google ads", "rsa", "both", ""}:
        issues.extend(validate_google(payload))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Copywrite Skill JSON output.")
    parser.add_argument("input", type=Path, help="Path to generated JSON.")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    issues = validate(payload)
    print(json.dumps({"passed": not issues, "issues": issues}, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
