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
    "Full Synthetic Bleeding-Risk Stack; source candidate database; "
    "dose omitted from curated product row; timing synthetic"
)


BLEEDING_INGREDIENT_ROWS = [
    {
        "ingredient_id": "ING-544",
        "ingredient_name": "Warfarin",
        "category/common_names": "Metabolic & Cardiovascular Health(drug; anticoagulant/vitamin K antagonist)",
        "supp.ai source id": "C0043031",
    },
    {
        "ingredient_id": "ING-545",
        "ingredient_name": "Hawthorn Leaf With Flower",
        "category/common_names": "Metabolic & Cardiovascular Health(botanical; hawthorn/crataegus)",
        "supp.ai source id": "C3255598",
    },
    {
        "ingredient_id": "ING-546",
        "ingredient_name": "Palmitic Acid",
        "category/common_names": "Essential Nutrition & General Health(fatty acid; palmitic acid)",
        "supp.ai source id": "C0030234",
    },
]


BLEEDING_PRODUCT_ROWS = [
    {
        "canonical_product_id": "PROD-489",
        "conceptual_supplement_group": "Warfarin",
        "product_concept": "Warfarin Sodium",
        "product_brand": "Warfarin Sodium",
        "setting_type": "flexible",
        "recommender": "synthetic_bleeding_risk_stack",
        "expanded_ingredient_name_ofdraft": "Warfarin sodium",
        "simple_ingredient_id": "ING-544",
        "simple_ingredient_name": "Warfarin",
        "reference_url": "NDC 0093-1721; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": REF_SYNTHETIC + "; BLE-01; NDC single-active-ingredient anticoagulant candidate",
        "Functionality": "regulated drugs",
    },
    {
        "canonical_product_id": "PROD-490",
        "conceptual_supplement_group": "Hawthorn",
        "product_concept": "Astra Garlic",
        "product_brand": "Health Concerns",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_bleeding_risk_stack",
        "expanded_ingredient_name_ofdraft": "Hawthorn Leaf With Flower",
        "simple_ingredient_id": "ING-545",
        "simple_ingredient_name": "Hawthorn Leaf With Flower",
        "reference_url": "DSLD label_id 22689; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; BLE-04; DSLD single-ingredient hawthorn candidate",
        "Functionality": "botanicals",
    },
    {
        "canonical_product_id": "PROD-491",
        "conceptual_supplement_group": "Ginkgo biloba",
        "product_concept": "Ginkgo Biloba",
        "product_brand": "GNC Herbal Plus Standardized",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_bleeding_risk_stack",
        "expanded_ingredient_name_ofdraft": "Ginkgo Biloba Whole",
        "simple_ingredient_id": "ING-125",
        "simple_ingredient_name": "Ginkgo Biloba Extract",
        "reference_url": "DSLD label_id 700; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; BLE-05; DSLD single-ingredient ginkgo candidate",
        "Functionality": "nootropics",
    },
    {
        "canonical_product_id": "PROD-492",
        "conceptual_supplement_group": "Bilberry",
        "product_concept": "Bilberry Fruit 1000 mg",
        "product_brand": "Vitamin World",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_bleeding_risk_stack",
        "expanded_ingredient_name_ofdraft": "Bilberry Extract",
        "simple_ingredient_id": "ING-231",
        "simple_ingredient_name": "bilberry extract",
        "reference_url": "DSLD label_id 578; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; BLE-10; DSLD single-ingredient bilberry candidate",
        "Functionality": "botanicals",
    },
    {
        "canonical_product_id": "PROD-493",
        "conceptual_supplement_group": "Fenugreek",
        "product_concept": "Fenugreek 610 mg",
        "product_brand": "GNC Herbal Plus Whole Herb",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_bleeding_risk_stack",
        "expanded_ingredient_name_ofdraft": "Trigonella Foenum-Graecum",
        "simple_ingredient_id": "ING-460",
        "simple_ingredient_name": "Fenugreek",
        "reference_url": "DSLD label_id 862; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; BLE-11; DSLD single-ingredient fenugreek candidate",
        "Functionality": "botanicals",
    },
]


GREEN_SUPERFOOD_INGREDIENTS = [
    ("Folic Acid", "ING-391", "Folic Acid, Vitamin B9 (synthetic)"),
    ("Iodine", "ING-037", "Iodine"),
    ("Niacin", "ING-006", "Niacin, Vitamin B3"),
    ("Palmitic Acid", "ING-546", "Palmitic Acid"),
    ("Potassium", "ING-194", "potassium"),
    ("Riboflavin", "ING-005", "Riboflavin, Vitamin B2"),
    ("Selenium", "ING-029", "Selenium"),
    ("Vitamin A", "ING-013", "Retinoids, Vitamin A"),
    ("Vitamin B 12", "ING-227", "Cobalamin, Vitamin B12"),
    ("Vitamin K", "ING-011", "Phytonadione, Vitamin K1"),
    ("Lactase", "ING-138", "lactase"),
    ("Vitamin B 6", "ING-093", "pyridoxine HCl, Vitamin B6"),
    ("Iron, Dietary", "ING-153", "Iron"),
    ("Green Tea Extract", "ING-106", "Green tea extract / Camellia sinensis"),
    ("Mn3+", "ING-033", "Manganese"),
    ("Vitamin C", "ING-038", "Ascorbic acid, Vitamin C"),
    ("Calcium Supplement", "ING-030", "Calcium"),
]

for expanded_name, ingredient_id, ingredient_name in GREEN_SUPERFOOD_INGREDIENTS:
    BLEEDING_PRODUCT_ROWS.append(
        {
            "canonical_product_id": "PROD-494",
            "conceptual_supplement_group": "High-vitamin-K greens",
            "product_concept": "Green SuperFood All Natural Drink Powder",
            "product_brand": "Amazing Grass",
            "setting_type": "meal_preferred",
            "recommender": "synthetic_bleeding_risk_stack",
            "expanded_ingredient_name_ofdraft": expanded_name,
            "simple_ingredient_id": ingredient_id,
            "simple_ingredient_name": ingredient_name,
            "reference_url": "DSLD label_id 718; candidate database dsld-1.jsonl",
            "Notes": REF_SYNTHETIC + "; BLE-14; DSLD green powder candidate; preserves high-vitamin-K greens complexity",
            "Functionality": "essential nutrients",
        }
    )


def load_json(name: str) -> list[dict]:
    with (DATASET_ROOT / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(name: str, rows: list[dict]) -> None:
    with (DATASET_ROOT / name).open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        f.write("\n")


def append_missing(rows: list[dict], additions: list[dict], key: str) -> int:
    existing = {row.get(key) for row in rows}
    added = 0
    for row in additions:
        if row.get(key) in existing:
            continue
        rows.append(row)
        existing.add(row.get(key))
        added += 1
    return added


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
    check = run_daily_compile_check(
        BLEEDING_PRODUCT_ROWS,
        BLEEDING_INGREDIENT_ROWS,
        known_ingredient_ids,
    )
    if not check["passed"]:
        raise SystemExit(json.dumps(check, ensure_ascii=False, indent=2))

    added_ingredients = append_missing(simple, BLEEDING_INGREDIENT_ROWS, "ingredient_id")
    added_product_rows = append_missing_product_rows(products, BLEEDING_PRODUCT_ROWS)

    dump_json("simple_ingredient_updated.json", simple)
    dump_json("product_ingredient_mapping.json", products)

    print(
        json.dumps(
            {
                "added": {
                    "simple_ingredient_updated": added_ingredients,
                    "product_ingredient_mapping_rows": added_product_rows,
                },
                "new_ingredient_ids": [row["ingredient_id"] for row in BLEEDING_INGREDIENT_ROWS],
                "new_product_ids": sorted({row["canonical_product_id"] for row in BLEEDING_PRODUCT_ROWS}),
                "totals": {
                    "simple_ingredient_updated": len(simple),
                    "product_ingredient_mapping": len(products),
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
