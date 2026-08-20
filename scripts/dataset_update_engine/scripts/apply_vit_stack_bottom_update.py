from __future__ import annotations

import json
import sys
from pathlib import Path


DATASET_ROOT = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "drug_lists"
    / "Real world experiment"
    / "scenario_files"
    / "Biohacker_dataset"
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dataset_update_engine.update_validator import run_daily_compile_check  # noqa: E402


REF_SYNTHETIC = (
    "Full Synthetic Vitamin-and-Mineral Stack; source candidate database; "
    "dose omitted from curated product row; timing synthetic"
)


VIT_PRODUCT_ROWS = [
    {
        "canonical_product_id": "PROD-505",
        "conceptual_supplement_group": "B-complex",
        "product_concept": "B-Complex Plus",
        "product_brand": "Pure Encapsulations",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Biotin",
        "simple_ingredient_id": "ING-007",
        "simple_ingredient_name": "Biotin, Vitamin B7",
        "reference_url": "DSLD label_id 183885; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-02; DSLD B-complex candidate covering B1/B2/B3/B5/B6/B7/B9/B12",
        "Functionality": "essential nutrients",
    },
    {
        "canonical_product_id": "PROD-505",
        "conceptual_supplement_group": "B-complex",
        "product_concept": "B-Complex Plus",
        "product_brand": "Pure Encapsulations",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Niacin",
        "simple_ingredient_id": "ING-006",
        "simple_ingredient_name": "Niacin, Vitamin B3",
        "reference_url": "DSLD label_id 183885; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-02; DSLD B-complex candidate covering B1/B2/B3/B5/B6/B7/B9/B12",
        "Functionality": "essential nutrients",
    },
    {
        "canonical_product_id": "PROD-505",
        "conceptual_supplement_group": "B-complex",
        "product_concept": "B-Complex Plus",
        "product_brand": "Pure Encapsulations",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Pantothenic Acid",
        "simple_ingredient_id": "ING-008",
        "simple_ingredient_name": "Pantothenic acid, Vitamin B5",
        "reference_url": "DSLD label_id 183885; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-02; DSLD B-complex candidate covering B1/B2/B3/B5/B6/B7/B9/B12",
        "Functionality": "essential nutrients",
    },
    {
        "canonical_product_id": "PROD-505",
        "conceptual_supplement_group": "B-complex",
        "product_concept": "B-Complex Plus",
        "product_brand": "Pure Encapsulations",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Riboflavin",
        "simple_ingredient_id": "ING-005",
        "simple_ingredient_name": "Riboflavin, Vitamin B2",
        "reference_url": "DSLD label_id 183885; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-02; DSLD B-complex candidate covering B1/B2/B3/B5/B6/B7/B9/B12",
        "Functionality": "essential nutrients",
    },
    {
        "canonical_product_id": "PROD-505",
        "conceptual_supplement_group": "B-complex",
        "product_concept": "B-Complex Plus",
        "product_brand": "Pure Encapsulations",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Thiamine",
        "simple_ingredient_id": "ING-004",
        "simple_ingredient_name": "Thiamin, Vitamin B1",
        "reference_url": "DSLD label_id 183885; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-02; DSLD B-complex candidate covering B1/B2/B3/B5/B6/B7/B9/B12",
        "Functionality": "essential nutrients",
    },
    {
        "canonical_product_id": "PROD-505",
        "conceptual_supplement_group": "B-complex",
        "product_concept": "B-Complex Plus",
        "product_brand": "Pure Encapsulations",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Vitamin B 12",
        "simple_ingredient_id": "ING-227",
        "simple_ingredient_name": "Cobalamin, Vitamin B12",
        "reference_url": "DSLD label_id 183885; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-02; DSLD B-complex candidate covering B1/B2/B3/B5/B6/B7/B9/B12",
        "Functionality": "essential nutrients",
    },
    {
        "canonical_product_id": "PROD-505",
        "conceptual_supplement_group": "B-complex",
        "product_concept": "B-Complex Plus",
        "product_brand": "Pure Encapsulations",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Vitamin B 6",
        "simple_ingredient_id": "ING-093",
        "simple_ingredient_name": "pyridoxine HCl, Vitamin B6",
        "reference_url": "DSLD label_id 183885; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-02; DSLD B-complex candidate covering B1/B2/B3/B5/B6/B7/B9/B12",
        "Functionality": "essential nutrients",
    },
    {
        "canonical_product_id": "PROD-505",
        "conceptual_supplement_group": "B-complex",
        "product_concept": "B-Complex Plus",
        "product_brand": "Pure Encapsulations",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Folate",
        "simple_ingredient_id": "ING-115",
        "simple_ingredient_name": "folate",
        "reference_url": "DSLD label_id 183885; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-02; DSLD B-complex candidate covering B1/B2/B3/B5/B6/B7/B9/B12",
        "Functionality": "essential nutrients",
    },
    {
        "canonical_product_id": "PROD-506",
        "conceptual_supplement_group": "Energy/pre-workout formula",
        "product_concept": "Red Bull Energy Drink",
        "product_brand": "Red Bull",
        "setting_type": "special_time_required",
        "special_time": "before_4pm",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Niacin",
        "simple_ingredient_id": "ING-006",
        "simple_ingredient_name": "Niacin, Vitamin B3",
        "reference_url": "DSLD label_id 33224; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-04; DSLD low-expansion energy formula candidate",
        "Functionality": "energy",
    },
    {
        "canonical_product_id": "PROD-506",
        "conceptual_supplement_group": "Energy/pre-workout formula",
        "product_concept": "Red Bull Energy Drink",
        "product_brand": "Red Bull",
        "setting_type": "special_time_required",
        "special_time": "before_4pm",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Pantothenic Acid",
        "simple_ingredient_id": "ING-008",
        "simple_ingredient_name": "Pantothenic acid, Vitamin B5",
        "reference_url": "DSLD label_id 33224; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-04; DSLD low-expansion energy formula candidate",
        "Functionality": "energy",
    },
    {
        "canonical_product_id": "PROD-506",
        "conceptual_supplement_group": "Energy/pre-workout formula",
        "product_concept": "Red Bull Energy Drink",
        "product_brand": "Red Bull",
        "setting_type": "special_time_required",
        "special_time": "before_4pm",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Vitamin B 12",
        "simple_ingredient_id": "ING-227",
        "simple_ingredient_name": "Cobalamin, Vitamin B12",
        "reference_url": "DSLD label_id 33224; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-04; DSLD low-expansion energy formula candidate",
        "Functionality": "energy",
    },
    {
        "canonical_product_id": "PROD-506",
        "conceptual_supplement_group": "Energy/pre-workout formula",
        "product_concept": "Red Bull Energy Drink",
        "product_brand": "Red Bull",
        "setting_type": "special_time_required",
        "special_time": "before_4pm",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Vitamin B 6",
        "simple_ingredient_id": "ING-093",
        "simple_ingredient_name": "pyridoxine HCl, Vitamin B6",
        "reference_url": "DSLD label_id 33224; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-04; DSLD low-expansion energy formula candidate",
        "Functionality": "energy",
    },
    {
        "canonical_product_id": "PROD-507",
        "conceptual_supplement_group": "Sleep magnesium+B6 formula",
        "product_concept": "Magnesium Plus B6",
        "product_brand": "Bluebonnet",
        "setting_type": "bed_empty_preferred",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Magnesium",
        "simple_ingredient_id": "ING-302",
        "simple_ingredient_name": "Magnesium (unspecified form)",
        "reference_url": "DSLD label_id 178460; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-05; DSLD two-ingredient magnesium plus vitamin B6 sleep candidate",
        "Functionality": "sleep",
    },
    {
        "canonical_product_id": "PROD-507",
        "conceptual_supplement_group": "Sleep magnesium+B6 formula",
        "product_concept": "Magnesium Plus B6",
        "product_brand": "Bluebonnet",
        "setting_type": "bed_empty_preferred",
        "recommender": "synthetic_vitamin_mineral_stack",
        "expanded_ingredient_name_ofdraft": "Vitamin B 6",
        "simple_ingredient_id": "ING-093",
        "simple_ingredient_name": "pyridoxine HCl, Vitamin B6",
        "reference_url": "DSLD label_id 178460; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; VIT-05; DSLD two-ingredient magnesium plus vitamin B6 sleep candidate",
        "Functionality": "sleep",
    },
]


def load_json(name: str) -> list[dict]:
    with (DATASET_ROOT / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(name: str, rows: list[dict]) -> None:
    with (DATASET_ROOT / name).open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        f.write("\n")


def append_missing_product_rows(rows: list[dict], additions: list[dict]) -> int:
    existing = {
        (row.get("canonical_product_id"), row.get("simple_ingredient_id"), row.get("expanded_ingredient_name_ofdraft"))
        for row in rows
    }
    added = 0
    for row in additions:
        key = (row.get("canonical_product_id"), row.get("simple_ingredient_id"), row.get("expanded_ingredient_name_ofdraft"))
        if key in existing:
            continue
        rows.append(row)
        existing.add(key)
        added += 1
    return added


def main() -> None:
    simple = load_json("simple_ingredient_updated.json")
    products = load_json("product_ingredient_mapping.json")

    known_ingredient_ids = {row.get("ingredient_id") for row in simple}
    check = run_daily_compile_check(VIT_PRODUCT_ROWS, [], known_ingredient_ids)
    if not check["passed"]:
        raise SystemExit(json.dumps(check, ensure_ascii=False, indent=2))

    added_product_rows = append_missing_product_rows(products, VIT_PRODUCT_ROWS)
    dump_json("product_ingredient_mapping.json", products)

    print(
        json.dumps(
            {
                "added": {"product_ingredient_mapping_rows": added_product_rows},
                "new_product_ids": sorted({row["canonical_product_id"] for row in VIT_PRODUCT_ROWS}),
                "totals": {"product_ingredient_mapping": len(products)},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
