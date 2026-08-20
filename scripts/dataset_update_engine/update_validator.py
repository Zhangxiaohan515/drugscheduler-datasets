from __future__ import annotations

from typing import Any

from .normalization import clean_text


ALLOWED_SETTING_TYPES = {
    "meal_preferred",
    "meal_required",
    "wake_empty_preferred",
    "bed_empty_preferred",
    "bed_empty_required",
    "gap_preferred",
    "special_time_required",
    "flexible",
}


PRODUCT_REQUIRED_FIELDS = [
    "canonical_product_id",
    "product_concept",
    "product_brand",
    "setting_type",
    "recommender",
    "expanded_ingredient_name_ofdraft",
    "simple_ingredient_id",
    "simple_ingredient_name",
]

INGREDIENT_FIELDS = ["ingredient_id", "ingredient_name", "category/common_names"]


def validate_special_time(value: Any) -> bool:
    # Mirrors the daily parser's accepted surface enough for preflight checks.
    import re

    text = clean_text(value)
    if not text:
        return False
    return bool(
        re.match(
            r"^\s*(?:(before|after)[ _]?)?\d{1,2}(?::\d{2})?\s*(am|pm)?\s*$",
            text,
            re.IGNORECASE,
        )
    )


def validate_ingredient_row(row: dict[str, Any]) -> list[str]:
    errors = []
    for field in INGREDIENT_FIELDS:
        if not clean_text(row.get(field)):
            errors.append(f"missing {field}")
    extra_review_fields = {"needs_review", "review_status", "approval_status"}
    leaked = sorted(extra_review_fields.intersection(row.keys()))
    if leaked:
        errors.append("review metadata leaked into curated ingredient row: " + ", ".join(leaked))
    return errors


def validate_product_row(row: dict[str, Any], known_or_draft_ingredient_ids: set[str]) -> list[str]:
    errors = []
    for field in PRODUCT_REQUIRED_FIELDS:
        if not clean_text(row.get(field)):
            errors.append(f"missing {field}")

    setting_type = clean_text(row.get("setting_type"))
    if setting_type not in ALLOWED_SETTING_TYPES:
        errors.append(f"invalid setting_type {setting_type!r}")
    if setting_type == "special_time_required" and not validate_special_time(row.get("special_time")):
        errors.append("special_time_required needs valid special_time")

    ingredient_id = clean_text(row.get("simple_ingredient_id"))
    if ingredient_id and ingredient_id not in known_or_draft_ingredient_ids:
        errors.append(f"unknown simple_ingredient_id {ingredient_id}")

    extra_review_fields = {"needs_review", "review_status", "approval_status"}
    leaked = sorted(extra_review_fields.intersection(row.keys()))
    if leaked:
        errors.append("review metadata leaked into curated product row: " + ", ".join(leaked))
    return errors


def run_daily_compile_check(
    product_rows: list[dict[str, Any]],
    ingredient_rows: list[dict[str, Any]],
    existing_ingredient_ids: set[str],
) -> dict[str, Any]:
    draft_ingredient_ids = {clean_text(r.get("ingredient_id")) for r in ingredient_rows}
    known = existing_ingredient_ids | draft_ingredient_ids

    product_errors = [
        {"row_index": idx, "errors": errors}
        for idx, row in enumerate(product_rows)
        if (errors := validate_product_row(row, known))
    ]
    ingredient_errors = [
        {"row_index": idx, "errors": errors}
        for idx, row in enumerate(ingredient_rows)
        if (errors := validate_ingredient_row(row))
    ]
    return {
        "check_name": "daily",
        "enabled": True,
        "passed": not product_errors and not ingredient_errors,
        "product_row_errors": product_errors,
        "ingredient_row_errors": ingredient_errors,
    }
