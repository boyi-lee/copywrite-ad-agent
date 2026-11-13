#!/usr/bin/env python3
"""Collect public product-page evidence with Crawl4AI.

This script performs read-only crawling and deterministic JSON-LD normalization.
It intentionally leaves USP/FED interpretation to the Copywrite Agent and checker.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import ipaddress
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


VOLATILE_FIELDS = {
    "price",
    "price_currency",
    "availability",
    "price_valid_until",
    "rating_value",
    "review_count",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_urls(
    values: Iterable[str], max_urls: int, *, allow_private_network: bool = False
) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for raw in values:
        url = raw.strip()
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"Only absolute HTTP(S) URLs are allowed: {raw}")
        if parsed.username or parsed.password:
            raise ValueError(f"Credentials in URLs are not allowed: {raw}")
        hostname = (parsed.hostname or "").rstrip(".").lower()
        private_target = hostname == "localhost"
        try:
            address = ipaddress.ip_address(hostname)
        except ValueError:
            address = None
        if address is not None and (
            address.is_private
            or address.is_loopback
            or address.is_link_local
            or address.is_multicast
            or address.is_reserved
            or address.is_unspecified
        ):
            private_target = True
        if private_target and not allow_private_network:
            raise ValueError(f"Private or local network URLs are blocked by default: {raw}")
        if url not in seen:
            seen.add(url)
            urls.append(url)
    if not urls:
        raise ValueError("At least one --url is required.")
    if len(urls) > max_urls:
        raise ValueError(f"URL budget exceeded: {len(urls)} > {max_urls}.")
    return urls


class JsonLdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._capturing = False
        self._chunks: list[str] = []
        self.blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "script":
            return
        attr_map = {key.lower(): (value or "") for key, value in attrs}
        if "application/ld+json" in attr_map.get("type", "").lower():
            self._capturing = True
            self._chunks = []

    def handle_data(self, data: str) -> None:
        if self._capturing:
            self._chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._capturing:
            self.blocks.append("".join(self._chunks).strip())
            self._capturing = False
            self._chunks = []


def walk_json(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_json(child)


def is_product_node(node: dict[str, Any]) -> bool:
    raw_type = node.get("@type", "")
    types = raw_type if isinstance(raw_type, list) else [raw_type]
    return any(str(item).lower() == "product" for item in types)


def product_json_ld(html: str) -> list[dict[str, Any]]:
    parser = JsonLdParser()
    parser.feed(html or "")
    products: list[dict[str, Any]] = []
    for block in parser.blocks:
        if not block:
            continue
        try:
            decoded = json.loads(block)
        except json.JSONDecodeError:
            continue
        products.extend(node for node in walk_json(decoded) if is_product_node(node))
    return products


def compact_text(value: Any, limit: int = 500) -> str:
    if isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    else:
        text = str(value)
    return " ".join(text.split())[:limit]


def scalar(value: Any) -> Any:
    if isinstance(value, dict):
        return value.get("name") or value.get("value") or compact_text(value)
    if isinstance(value, list):
        return [scalar(item) for item in value]
    return value


def add_fact(
    facts: list[dict[str, Any]],
    *,
    field: str,
    value: Any,
    source_url: str,
    locator: str,
    captured_at: str,
) -> None:
    if value is None or value == "" or value == []:
        return
    fact_id = "EV-" + hashlib.sha256(
        f"{source_url}|{locator}|{compact_text(value)}".encode("utf-8")
    ).hexdigest()[:12]
    facts.append(
        {
            "id": fact_id,
            "field": field,
            "value": scalar(value),
            "source_url": source_url,
            "source_type": "json_ld",
            "source_locator": locator,
            "evidence_text": compact_text(value),
            "captured_at": captured_at,
            "confidence": "high",
            "volatile": field in VOLATILE_FIELDS,
        }
    )


def normalize_product_nodes(
    nodes: list[dict[str, Any]], source_url: str, captured_at: str
) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    direct_fields = {
        "name": "name",
        "brand": "brand",
        "description": "description",
        "sku": "sku",
        "mpn": "mpn",
        "material": "material",
        "color": "color",
        "category": "category",
    }
    offer_fields = {
        "price": "price",
        "priceCurrency": "price_currency",
        "availability": "availability",
        "priceValidUntil": "price_valid_until",
        "url": "offer_url",
    }
    rating_fields = {"ratingValue": "rating_value", "reviewCount": "review_count"}

    for node_index, node in enumerate(nodes):
        prefix = f"Product[{node_index}]"
        for source_key, field in direct_fields.items():
            add_fact(
                facts,
                field=field,
                value=node.get(source_key),
                source_url=source_url,
                locator=f"{prefix}.{source_key}",
                captured_at=captured_at,
            )
        offers = node.get("offers", [])
        if isinstance(offers, dict):
            offers = [offers]
        for offer_index, offer in enumerate(offers if isinstance(offers, list) else []):
            if not isinstance(offer, dict):
                continue
            for source_key, field in offer_fields.items():
                add_fact(
                    facts,
                    field=field,
                    value=offer.get(source_key),
                    source_url=source_url,
                    locator=f"{prefix}.offers[{offer_index}].{source_key}",
                    captured_at=captured_at,
                )
        rating = node.get("aggregateRating")
        if isinstance(rating, dict):
            for source_key, field in rating_fields.items():
                add_fact(
                    facts,
                    field=field,
                    value=rating.get(source_key),
                    source_url=source_url,
                    locator=f"{prefix}.aggregateRating.{source_key}",
                    captured_at=captured_at,
                )
        properties = node.get("additionalProperty", [])
        if isinstance(properties, dict):
            properties = [properties]
        for prop_index, prop in enumerate(properties if isinstance(properties, list) else []):
            if not isinstance(prop, dict):
                continue
            prop_name = prop.get("name") or f"additional_property_{prop_index}"
            add_fact(
                facts,
                field=f"specification:{prop_name}",
                value=prop.get("value"),
                source_url=source_url,
                locator=f"{prefix}.additionalProperty[{prop_index}]",
                captured_at=captured_at,
            )

    unique: dict[str, dict[str, Any]] = {}
    for fact in facts:
        unique[fact["id"]] = fact
    return list(unique.values())


def markdown_text(result: Any) -> str:
    markdown = getattr(result, "markdown", "")
    return str(getattr(markdown, "raw_markdown", markdown) or "")


def result_to_product(result: Any, requested_url: str, run_dir: Path, index: int) -> dict[str, Any]:
    captured_at = utc_now()
    final_url = str(getattr(result, "redirected_url", "") or getattr(result, "url", "") or requested_url)
    success = bool(getattr(result, "success", False))
    status_code = getattr(result, "status_code", None)
    error = str(getattr(result, "error_message", "") or "")
    if not success:
        blocked = status_code == 403 or "robots.txt" in error.lower()
        return {
            "requested_url": requested_url,
            "source_url": final_url,
            "crawl_status": "blocked" if blocked else "failed",
            "status_code": status_code,
            "title": "",
            "facts": [],
            "raw_markdown_path": None,
            "error": error or "Crawl failed without an error message.",
        }

    raw_markdown = markdown_text(result)
    raw_path = run_dir / f"product-{index:02d}.md"
    raw_path.write_text(raw_markdown, encoding="utf-8")
    nodes = product_json_ld(str(getattr(result, "html", "") or ""))
    facts = normalize_product_nodes(nodes, final_url, captured_at)
    metadata = getattr(result, "metadata", {}) or {}
    title = str(metadata.get("title", "") if isinstance(metadata, dict) else "")
    return {
        "requested_url": requested_url,
        "source_url": final_url,
        "crawl_status": "success",
        "status_code": status_code,
        "title": title,
        "facts": facts,
        "raw_markdown_path": raw_path.name,
        "error": "" if facts else "No Product JSON-LD facts found; semantic page review required.",
    }


async def crawl(urls: list[str], args: argparse.Namespace, run_dir: Path) -> list[dict[str, Any]]:
    # Crawl4AI otherwise writes to ~/.crawl4ai during import. Keep all crawler
    # state inside this run so the write scope remains explicit and reversible.
    os.environ["CRAWL4_AI_BASE_DIRECTORY"] = str(run_dir)
    if args.browser_path:
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(args.browser_path.resolve())
    try:
        from crawl4ai import (
            AsyncWebCrawler,
            BrowserConfig,
            CacheMode,
            CrawlerRunConfig,
            RateLimiter,
        )
        from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher
    except ImportError as exc:
        raise RuntimeError(
            "Crawl4AI is not installed. Install requirements-product-research.txt in an approved environment."
        ) from exc

    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        stream=False,
        check_robots_txt=not args.ignore_robots,
        scan_full_page=args.scan_full_page,
    )
    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=75.0,
        check_interval=1.0,
        max_session_permit=args.max_concurrency,
        memory_wait_timeout=float(args.max_duration),
        rate_limiter=RateLimiter(
            base_delay=(args.min_delay, args.max_delay),
            max_delay=min(30.0, float(args.max_duration)),
            max_retries=max(0, args.max_attempts - 1),
            rate_limit_codes=[429, 503, 504],
        ),
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun_many(urls=urls, config=run_config, dispatcher=dispatcher)
    by_url = {str(getattr(item, "url", "")): item for item in results}
    products: list[dict[str, Any]] = []
    for index, requested_url in enumerate(urls, start=1):
        result = by_url.get(requested_url)
        if result is None:
            products.append(
                {
                    "requested_url": requested_url,
                    "source_url": requested_url,
                    "crawl_status": "failed",
                    "status_code": None,
                    "title": "",
                    "facts": [],
                    "raw_markdown_path": None,
                    "error": "Crawler returned no result for this URL.",
                }
            )
        else:
            products.append(result_to_product(result, requested_url, run_dir, index))
    return products


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="Batch-crawl product pages into a reviewable evidence bundle.")
    value.add_argument("--url", action="append", default=[], help="Product URL; repeat for multiple products.")
    value.add_argument("--output-dir", type=Path, help="Required parent directory for persisted run artifacts.")
    value.add_argument("--max-urls", type=int, default=20)
    value.add_argument("--max-attempts", type=int, default=2)
    value.add_argument("--max-duration", type=int, default=180)
    value.add_argument("--max-concurrency", type=int, default=4)
    value.add_argument("--min-delay", type=float, default=1.0)
    value.add_argument("--max-delay", type=float, default=2.0)
    value.add_argument("--scan-full-page", action="store_true")
    value.add_argument("--browser-path", type=Path, help="Optional approved Playwright browser directory.")
    value.add_argument("--allow-private-network", action="store_true", help="Explicit local-test override.")
    value.add_argument("--ignore-robots", action="store_true", help="Explicit override; not recommended.")
    value.add_argument("--check-dependency", action="store_true")
    return value


def main() -> int:
    args = parser().parse_args()
    if args.check_dependency:
        dependency_state = Path("/tmp/copywrite-crawl4ai-dependency-check")
        dependency_state.mkdir(parents=True, exist_ok=True)
        os.environ["CRAWL4_AI_BASE_DIRECTORY"] = str(dependency_state)
        try:
            import crawl4ai  # noqa: F401
        except ImportError:
            print(json.dumps({"available": False, "dependency": "crawl4ai"}))
            return 1
        print(json.dumps({"available": True, "dependency": "crawl4ai"}))
        return 0

    if args.output_dir is None:
        print("--output-dir is required.", file=sys.stderr)
        return 2
    if args.max_attempts < 1 or args.max_attempts > 2:
        print("--max-attempts must be between 1 and 2.", file=sys.stderr)
        return 2
    if args.max_duration < 1 or args.max_duration > 180:
        print("--max-duration must be between 1 and 180 seconds.", file=sys.stderr)
        return 2
    if args.max_concurrency < 1 or args.max_concurrency > 4:
        print("--max-concurrency must be between 1 and 4.", file=sys.stderr)
        return 2
    if args.min_delay < 0 or args.max_delay < args.min_delay:
        print("Delay range is invalid.", file=sys.stderr)
        return 2

    try:
        urls = validate_urls(
            args.url, args.max_urls, allow_private_network=args.allow_private_network
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    started_at = utc_now()
    started_clock = time.monotonic()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    run_dir = args.output_dir.resolve() / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    products: list[dict[str, Any]] = []
    terminal_status = "blocked"
    unresolved: list[str] = ["USP/FED enrichment and independent checker review are pending."]
    runtime_error = ""
    try:
        products = asyncio.run(
            asyncio.wait_for(crawl(urls, args, run_dir), timeout=float(args.max_duration))
        )
    except asyncio.TimeoutError:
        runtime_error = "Wall-clock budget exhausted."
        terminal_status = "failed"
    except Exception as exc:
        runtime_error = f"{type(exc).__name__}: {exc}"
        terminal_status = "blocked" if isinstance(exc, RuntimeError) else "failed"

    if not products:
        products = [
            {
                "requested_url": url,
                "source_url": url,
                "crawl_status": "failed",
                "status_code": None,
                "title": "",
                "facts": [],
                "raw_markdown_path": None,
                "error": runtime_error or "No crawl result.",
            }
            for url in urls
        ]
    if runtime_error:
        unresolved.append(runtime_error)
    failed_count = sum(item["crawl_status"] != "success" for item in products)
    if failed_count:
        unresolved.append(f"{failed_count} of {len(products)} requested URLs were not successfully crawled.")

    ended_at = utc_now()
    duration = round(time.monotonic() - started_clock, 3)
    artifact = {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "status": terminal_status,
        "started_at": started_at,
        "ended_at": ended_at,
        "requested_urls": urls,
        "products": products,
        "usp_candidates": [],
        "blocked_claims": [],
        "budgets": {
            "max_urls": args.max_urls,
            "max_attempts_per_url": args.max_attempts,
            "max_duration_seconds": args.max_duration,
            "max_concurrency": args.max_concurrency,
            "attempts_used_upper_bound": len(urls) * args.max_attempts,
            "duration_seconds": duration,
        },
        "unresolved_risks": unresolved,
        "live_ready": False,
        "manual_check_required": True,
    }
    artifact_path = run_dir / "product-research.json"
    artifact_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    run_record = {
        "run_id": run_id,
        "loop_id": "copywrite-product-research",
        "loop_version": "1.0.0",
        "task_id": run_id,
        "started_at": started_at,
        "ended_at": ended_at,
        "trigger": {"type": "explicit_user_request"},
        "input_snapshot": {"urls": urls},
        "source_evidence": [fact["id"] for product in products for fact in product["facts"]],
        "attempts": [
            {
                "requested_url": product["requested_url"],
                "status": product["crawl_status"],
                "status_code": product["status_code"],
                "error": product["error"],
            }
            for product in products
        ],
        "final_verdict": {
            "status": terminal_status,
            "score": 0,
            "failed_criteria": ["USP/FED and checker pending"],
            "human_review_required": True,
        },
        "budgets": artifact["budgets"],
        "artifacts": [str(artifact_path)] + [
            str(run_dir / product["raw_markdown_path"])
            for product in products
            if product["raw_markdown_path"]
        ],
        "unresolved_risks": unresolved,
        "learning_note": "",
        "rule_update_proposal": "",
        "live_ready": False,
        "manual_check_required": True,
    }
    (run_dir / "run-record.json").write_text(
        json.dumps(run_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"run_id": run_id, "status": terminal_status, "artifact": str(artifact_path)}, ensure_ascii=False))
    return 0 if not runtime_error else 1


if __name__ == "__main__":
    raise SystemExit(main())
