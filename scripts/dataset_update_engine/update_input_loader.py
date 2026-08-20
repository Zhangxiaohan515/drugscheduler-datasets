from __future__ import annotations

import csv
import json
from collections import OrderedDict
from pathlib import Path
from typing import Any

from .normalization import clean_text


CANONICAL_TOP_LEVEL = (
    "products",
    "food_routines",
    "food_items",
    "components",
    "mechanism_rules",
    "extra_effect_rules",
    "food_component_ingredient_rules",
)


def parse_update_file(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return normalize_package(json.loads(path.read_text(encoding="utf-8")))
    if suffix == ".csv":
        return rows_to_package(read_csv_rows(path))
    if suffix in {".md", ".markdown"}:
        return rows_to_package(read_markdown_table_rows(path))
    if suffix in {".xlsx", ".xls"}:
        return rows_to_package(read_excel_rows(path))
    raise ValueError(f"Unsupported update input format: {path.suffix}")


def normalize_package(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Canonical update package must be a JSON object")

    out = {key: payload.get(key, []) for key in CANONICAL_TOP_LEVEL}
    for key in CANONICAL_TOP_LEVEL:
        if out[key] is None:
            out[key] = []
        if not isinstance(out[key], list):
            raise ValueError(f"Canonical field {key!r} must be a list")
    return out


def read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def read_markdown_table_rows(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    table_lines = [line.strip() for line in lines if line.strip().startswith("|") and line.strip().endswith("|")]
    if len(table_lines) < 2:
        return []

    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, Any]] = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def read_excel_rows(path: Path) -> list[dict[str, Any]]:
    try:
        import openpyxl  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Excel parsing requires openpyxl to be installed") from exc

    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows: list[dict[str, Any]] = []
    for sheet in workbook.worksheets:
        iterator = sheet.iter_rows(values_only=True)
        headers = next(iterator, None)
        if not headers:
            continue
        header_values = [clean_text(h) for h in headers]
        if not any(header_values):
            continue
        for values in iterator:
            row = {header_values[i]: values[i] if i < len(values) else None for i in range(len(header_values))}
            if any(clean_text(v) for v in row.values()):
                row["_sheet"] = sheet.title
                rows.append(row)
    return rows


def rows_to_package(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Convert flat tabular rows into the canonical JSON package."""
    products: "OrderedDict[tuple[str, str, str], dict[str, Any]]" = OrderedDict()
    food_routines: list[dict[str, Any]] = []
    food_items: list[dict[str, Any]] = []
    components: list[dict[str, Any]] = []

    for row in rows:
        section = clean_text(row.get("section") or row.get("type") or row.get("_sheet")).lower()
        if section in {"food_routines", "food routine", "food_routine", "routine"}:
            food_routines.append(row)
            continue
        if section in {"food_items", "food item", "food_item", "foods"}:
            food_items.append(row)
            continue
        if section in {"components", "component", "food components"}:
            components.append(row)
            continue

        brand = clean_text(row.get("product_brand") or row.get("brand"))
        concept = clean_text(row.get("product_concept") or row.get("concept") or row.get("product"))
        recommender = clean_text(row.get("recommender"))
        ingredient_name = clean_text(
            row.get("ingredient_name")
            or row.get("ingredient")
            or row.get("name")
            or row.get("expanded_ingredient_name_ofdraft")
        )
        if not (brand or concept or ingredient_name):
            continue

        key = (brand, concept, recommender)
        product = products.setdefault(
            key,
            {
                "product_brand": brand,
                "product_concept": concept,
                "category": clean_text(row.get("category") or row.get("functional_category")),
                "recommender": recommender,
                "setting_type": clean_text(row.get("setting_type")),
                "special_time": clean_text(row.get("special_time")),
                "reference_url": clean_text(row.get("reference_url") or row.get("url") or row.get("URL")),
                "notes": clean_text(row.get("notes") or row.get("Notes")),
                "functionality": clean_text(row.get("functionality") or row.get("Functionality")),
                "ingredients": [],
            },
        )
        if ingredient_name:
            product["ingredients"].append(
                {
                    "name": ingredient_name,
                    "category": clean_text(row.get("ingredient_category") or row.get("category")),
                    "mechanism_family": clean_text(row.get("mechanism_family") or row.get("mechanism_id")),
                    "amount": clean_text(row.get("amount")),
                    "unit": clean_text(row.get("unit")),
                }
            )

    return normalize_package(
        {
            "products": list(products.values()),
            "food_routines": food_routines,
            "food_items": food_items,
            "components": components,
        }
    )
