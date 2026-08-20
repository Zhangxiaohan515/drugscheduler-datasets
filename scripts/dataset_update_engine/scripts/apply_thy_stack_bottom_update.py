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

from dataset_update_engine.update_validator import run_daily_compile_check


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


def append_missing_food_component(rows: list[dict], additions: list[dict]) -> int:
    existing = {(row.get("food_id"), row.get("component_id")) for row in rows}
    added = 0
    for row in additions:
        key = (row.get("food_id"), row.get("component_id"))
        if key in existing:
            continue
        rows.append(row)
        existing.add(key)
        added += 1
    return added


THYROID_INGREDIENT_ROWS = [
    {
        "ingredient_id": "ING-540",
        "ingredient_name": "Aluminum Hydroxide",
        "category/common_names": "Gut & Digestive Health(OTC drug; antacid/aluminum hydroxide)",
        "supp.ai source id": "C0002371",
    }
]


THYROID_PRODUCT_ROWS = [
    {
        "canonical_product_id": "PROD-477",
        "conceptual_supplement_group": "Levothyroxine",
        "product_concept": "Levothyroxine Sodium",
        "product_brand": "Synthroid",
        "setting_type": "wake_empty_preferred",
        "recommender": "synthetic_levothyroxine_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Levothyroxine sodium",
        "simple_ingredient_id": "ING-256",
        "simple_ingredient_name": "Levothyroxine",
        "reference_url": "NDC 0074-6624; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": "Full Synthetic Levothyroxine Interaction Stack; source candidate database; dose omitted from curated product row; timing synthetic; THY-01; NDC pharm_class Thyroxine [CS]; l-Thyroxine [EPC]",
        "Functionality": "regulated drugs",
    },
    {
        "canonical_product_id": "PROD-478",
        "conceptual_supplement_group": "Calcium carbonate",
        "product_concept": "Calcium Carbonate",
        "product_brand": "TUMS",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_levothyroxine_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Calcium carbonate",
        "simple_ingredient_id": "ING-030",
        "simple_ingredient_name": "Calcium",
        "reference_url": "NDC 0135-0070; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": "Full Synthetic Levothyroxine Interaction Stack; source candidate database; dose omitted from curated product row; timing synthetic; THY-02; NDC active ingredient calcium carbonate",
        "Functionality": "regulated drugs",
    },
    {
        "canonical_product_id": "PROD-479",
        "conceptual_supplement_group": "Ferrous sulfate",
        "product_concept": "Ferrous Sulfate",
        "product_brand": "Clinical Solutions Wholesale",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_levothyroxine_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Ferrous sulfate",
        "simple_ingredient_id": "ING-153",
        "simple_ingredient_name": "Iron",
        "reference_url": "DSLD label_id 263428; candidate database dsld-1/2.jsonl",
        "Notes": "Full Synthetic Levothyroxine Interaction Stack; source candidate database; dose omitted from curated product row; timing synthetic; THY-03; DSLD single-ingredient ferrous sulfate candidate",
        "Functionality": "essential nutrients",
    },
    {
        "canonical_product_id": "PROD-480",
        "conceptual_supplement_group": "Magnesium antacid",
        "product_concept": "Magnesium Hydroxide",
        "product_brand": "Milk of Magnesia",
        "setting_type": "flexible",
        "recommender": "synthetic_levothyroxine_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Magnesium hydroxide",
        "simple_ingredient_id": "ING-302",
        "simple_ingredient_name": "Magnesium (unspecified form)",
        "reference_url": "NDC 0121-0431; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": "Full Synthetic Levothyroxine Interaction Stack; source candidate database; dose omitted from curated product row; timing synthetic; THY-05; NDC active ingredient magnesium hydroxide",
        "Functionality": "regulated drugs",
    },
    {
        "canonical_product_id": "PROD-481",
        "conceptual_supplement_group": "Aluminum antacid",
        "product_concept": "Aluminum Hydroxide",
        "product_brand": "Aluminum Hydroxide",
        "setting_type": "flexible",
        "recommender": "synthetic_levothyroxine_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Aluminum hydroxide",
        "simple_ingredient_id": "ING-540",
        "simple_ingredient_name": "Aluminum Hydroxide",
        "reference_url": "NDC 0536-0091; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": "Full Synthetic Levothyroxine Interaction Stack; source candidate database; dose omitted from curated product row; timing synthetic; THY-06; NDC active ingredient aluminum hydroxide",
        "Functionality": "regulated drugs",
    },
    {
        "canonical_product_id": "PROD-482",
        "conceptual_supplement_group": "Chromium picolinate",
        "product_concept": "Ultra Chromium Picolinate",
        "product_brand": "Vitamin World",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_levothyroxine_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Chromium picolinate",
        "simple_ingredient_id": "ING-034",
        "simple_ingredient_name": "Chromium",
        "reference_url": "DSLD label_id 620; candidate database dsld-1/2.jsonl",
        "Notes": "Full Synthetic Levothyroxine Interaction Stack; source candidate database; dose omitted from curated product row; timing synthetic; THY-07; DSLD single-ingredient chromium picolinate candidate",
        "Functionality": "essential nutrients",
    },
    {
        "canonical_product_id": "PROD-483",
        "conceptual_supplement_group": "Kelp iodine",
        "product_concept": "Sea Kelp",
        "product_brand": "Vitamin World",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_levothyroxine_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Iodine",
        "simple_ingredient_id": "ING-037",
        "simple_ingredient_name": "Iodine",
        "reference_url": "DSLD label_id 1173; candidate database dsld-1/2.jsonl",
        "Notes": "Full Synthetic Levothyroxine Interaction Stack; source candidate database; dose omitted from curated product row; timing synthetic; THY-10; DSLD single-ingredient sea kelp/iodine candidate",
        "Functionality": "essential nutrients",
    },
]


THYROID_FOOD_ROWS = [
    {
        "component_id": "FOODC_PROTEIN",
        "component_name": "High-protein meal",
        "food_id": "FOOD-168",
        "food_name": "Soy protein shake",
        "food_category": "drink, protein, soy",
        "Notes": "Full Synthetic Levothyroxine Interaction Stack; THY-12; soy protein exposure represented with existing coarse food components",
        "source_url": ["user-provided synthetic levothyroxine interaction stack"],
    },
    {
        "component_id": "FOODC_PHYTATE",
        "component_name": "Phytate",
        "food_id": "FOOD-168",
        "food_name": "Soy protein shake",
        "food_category": "drink, protein, soy",
        "Notes": "Full Synthetic Levothyroxine Interaction Stack; THY-12; soy protein exposure represented with existing coarse food components",
        "source_url": ["user-provided synthetic levothyroxine interaction stack"],
    },
    {
        "component_id": "FOODC_FIBER",
        "component_name": "High-fiber food",
        "food_id": "FOOD-169",
        "food_name": "Chai spice overnight oats",
        "food_category": "breakfast meal, oats, fiber",
        "Notes": "Full Synthetic Levothyroxine Interaction Stack; THY-14; high-fiber breakfast meal from recipe candidates",
        "source_url": ["https://www.thedailymeal.com/1115707/chai-spice-overnight-oats-recipe/"],
    },
    {
        "component_id": "FOODC_PHYTATE",
        "component_name": "Phytate",
        "food_id": "FOOD-169",
        "food_name": "Chai spice overnight oats",
        "food_category": "breakfast meal, oats, fiber",
        "Notes": "Full Synthetic Levothyroxine Interaction Stack; THY-14; high-fiber breakfast meal from recipe candidates",
        "source_url": ["https://www.thedailymeal.com/1115707/chai-spice-overnight-oats-recipe/"],
    },
]


def main() -> None:
    simple = load_json("simple_ingredient_updated.json")
    products = load_json("product_ingredient_mapping.json")
    foods = load_json("food_component_dataset.json")

    known_ingredient_ids = {row.get("ingredient_id") for row in simple}
    check = run_daily_compile_check(THYROID_PRODUCT_ROWS, THYROID_INGREDIENT_ROWS, known_ingredient_ids)
    if not check["passed"]:
        raise SystemExit(json.dumps(check, ensure_ascii=False, indent=2))

    added_ingredients = append_missing(simple, THYROID_INGREDIENT_ROWS, "ingredient_id")
    added_products = append_missing(products, THYROID_PRODUCT_ROWS, "canonical_product_id")
    added_food_rows = append_missing_food_component(foods, THYROID_FOOD_ROWS)

    dump_json("simple_ingredient_updated.json", simple)
    dump_json("product_ingredient_mapping.json", products)
    dump_json("food_component_dataset.json", foods)

    print(
        json.dumps(
            {
                "added": {
                    "simple_ingredient_updated": added_ingredients,
                    "product_ingredient_mapping": added_products,
                    "food_component_dataset": added_food_rows,
                },
                "totals": {
                    "simple_ingredient_updated": len(simple),
                    "product_ingredient_mapping": len(products),
                    "food_component_dataset": len(foods),
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
