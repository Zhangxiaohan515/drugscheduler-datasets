"""Add meal-relative timing bonus windows for selected Biohacker products.

This keeps the coarse setting_type for feasibility/eligibility, but lets the
food-aware scheduler narrow the preferred timing bonus to a specific meal anchor.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAPPING_PATH = (
    ROOT
    / "data"
    / "drug_lists"
    / "Real world experiment"
    / "scenario_files"
    / "Biohacker_dataset"
    / "product_ingredient_mapping.json"
)

BEFORE_FIRST_MEAL = {
    "relation": "before_meal",
    "meal_anchor": "meal_start",
    "meal_scope": "first_meal",
    "lb_offset": -1.0,
    "ub_offset": -0.5,
}

AFTER_LAST_MEAL = {
    "relation": "after_meal",
    "meal_anchor": "meal_end",
    "meal_scope": "last_meal",
    "lb_offset": 0.0,
    "ub_offset": 0.25,
}

BEFORE_FIRST_MEAL_PRODUCTS = {"PROD-003", "PROD-004", "PROD-005", "PROD-246", "PROD-477"}


def set_after(row: dict, after_key: str, key: str, value) -> None:
    """Insert or update key after after_key without disturbing other row fields."""
    items = []
    inserted = False
    for k, v in row.items():
        if k == key:
            continue
        items.append((k, v))
        if k == after_key:
            items.append((key, value))
            inserted = True
    if not inserted:
        items.append((key, value))
    row.clear()
    row.update(items)


def main() -> None:
    rows = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    changed = []

    for row in rows:
        pid = row.get("canonical_product_id")

        # Repair a previous broad edit: PROD-132 should remain bed-empty preferred.
        if pid == "PROD-132" and row.get("setting_type") != "bed_empty_preferred":
            row["setting_type"] = "bed_empty_preferred"
            changed.append((pid, "setting_type=bed_empty_preferred"))

        # Existing duplicate rows for this magnesium product must agree for the
        # product-level timing compiler to run.
        if pid == "PROD-129" and row.get("setting_type") != "bed_empty_preferred":
            row["setting_type"] = "bed_empty_preferred"
            changed.append((pid, "setting_type=bed_empty_preferred"))

        if pid in BEFORE_FIRST_MEAL_PRODUCTS:
            set_after(row, "setting_type", "meal_relationship", dict(BEFORE_FIRST_MEAL))
            changed.append((pid, "meal_relationship=before_first_meal"))

        if pid == "PROD-194":
            if row.get("setting_type") != "gap_preferred":
                row["setting_type"] = "gap_preferred"
                changed.append((pid, "setting_type=gap_preferred"))
            set_after(row, "setting_type", "meal_relationship", dict(AFTER_LAST_MEAL))
            changed.append((pid, "meal_relationship=after_last_meal"))

    MAPPING_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unique = sorted(set(changed))
    print(f"Updated {len(unique)} product-row fields in {MAPPING_PATH}")
    for pid, action in unique:
        print(f"  {pid}: {action}")


if __name__ == "__main__":
    main()
