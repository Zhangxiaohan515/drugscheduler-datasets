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
    "Full Synthetic Serotonergic Stress-Test Stack; source candidate database; "
    "dose omitted from curated product row; timing synthetic"
)


SEROTONERGIC_INGREDIENT_ROWS = [
    {
        "ingredient_id": "ING-541",
        "ingredient_name": "Saffron Extract",
        "category/common_names": "Sleep, Stress & Mood(botanical; saffron/crocin-safranal extract)",
        "supp.ai source id": "C2348128",
    },
    {
        "ingredient_id": "ING-542",
        "ingredient_name": "Sumatriptan",
        "category/common_names": "Pain, Inflammation & Recovery(drug; migraine triptan/5-HT1 receptor agonist)",
        "supp.ai source id": "C0075632",
    },
    {
        "ingredient_id": "ING-543",
        "ingredient_name": "Tramadol",
        "category/common_names": "Pain, Inflammation & Recovery(drug; opioid analgesic with serotonergic activity)",
        "supp.ai source id": "C0040610",
    },
]


SEROTONERGIC_PRODUCT_ROWS = [
    {
        "canonical_product_id": "PROD-484",
        "conceptual_supplement_group": "Saffron",
        "product_concept": "Saffron 15 mg",
        "product_brand": "Exir",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_serotonergic_stress_test_stack",
        "expanded_ingredient_name_ofdraft": "Saffron - Spice",
        "simple_ingredient_id": "ING-541",
        "simple_ingredient_name": "Saffron Extract",
        "reference_url": "DSLD label_id 11780; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; SER-07; DSLD single-ingredient saffron candidate",
        "Functionality": "botanicals",
    },
    {
        "canonical_product_id": "PROD-485",
        "conceptual_supplement_group": "Sumatriptan",
        "product_concept": "Sumatriptan",
        "product_brand": "IMITREX",
        "setting_type": "flexible",
        "recommender": "synthetic_serotonergic_stress_test_stack",
        "expanded_ingredient_name_ofdraft": "Sumatriptan succinate",
        "simple_ingredient_id": "ING-542",
        "simple_ingredient_name": "Sumatriptan",
        "reference_url": "NDC 0173-0736; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": REF_SYNTHETIC + "; SER-12; NDC single-active-ingredient migraine triptan candidate",
        "Functionality": "regulated drugs",
    },
    {
        "canonical_product_id": "PROD-486",
        "conceptual_supplement_group": "Tramadol",
        "product_concept": "Tramadol Hydrochloride",
        "product_brand": "Tramadol Hydrochloride",
        "setting_type": "flexible",
        "recommender": "synthetic_serotonergic_stress_test_stack",
        "expanded_ingredient_name_ofdraft": "Tramadol hydrochloride",
        "simple_ingredient_id": "ING-543",
        "simple_ingredient_name": "Tramadol",
        "reference_url": "NDC 0093-0058; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": REF_SYNTHETIC + "; SER-10; NDC single-active-ingredient analgesic candidate",
        "Functionality": "regulated drugs",
    },
    {
        "canonical_product_id": "PROD-487",
        "conceptual_supplement_group": "5-HTP",
        "product_concept": "5-HTP 50 mg",
        "product_brand": "Jarrow Formulas",
        "setting_type": "bed_empty_preferred",
        "recommender": "synthetic_serotonergic_stress_test_stack",
        "expanded_ingredient_name_ofdraft": "5-Hydroxytryptophan",
        "simple_ingredient_id": "ING-398",
        "simple_ingredient_name": "5-HTP",
        "reference_url": "DSLD label_id 1142; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; SER-03; DSLD single-ingredient 5-HTP candidate",
        "Functionality": "sleep",
    },
    {
        "canonical_product_id": "PROD-488",
        "conceptual_supplement_group": "L-Tryptophan",
        "product_concept": "Best L-Tryptophan 500 mg",
        "product_brand": "Doctor's Best",
        "setting_type": "bed_empty_preferred",
        "recommender": "synthetic_serotonergic_stress_test_stack",
        "expanded_ingredient_name_ofdraft": "Tryptophan",
        "simple_ingredient_id": "ING-228",
        "simple_ingredient_name": "L-Tryptophan",
        "reference_url": "DSLD label_id 1258; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; SER-04; DSLD single-ingredient L-tryptophan candidate",
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


def main() -> None:
    simple = load_json("simple_ingredient_updated.json")
    products = load_json("product_ingredient_mapping.json")

    known_ingredient_ids = {row.get("ingredient_id") for row in simple}
    check = run_daily_compile_check(
        SEROTONERGIC_PRODUCT_ROWS,
        SEROTONERGIC_INGREDIENT_ROWS,
        known_ingredient_ids,
    )
    if not check["passed"]:
        raise SystemExit(json.dumps(check, ensure_ascii=False, indent=2))

    added_ingredients = append_missing(simple, SEROTONERGIC_INGREDIENT_ROWS, "ingredient_id")
    added_products = append_missing(products, SEROTONERGIC_PRODUCT_ROWS, "canonical_product_id")

    dump_json("simple_ingredient_updated.json", simple)
    dump_json("product_ingredient_mapping.json", products)

    print(
        json.dumps(
            {
                "added": {
                    "simple_ingredient_updated": added_ingredients,
                    "product_ingredient_mapping": added_products,
                },
                "new_ingredient_ids": [row["ingredient_id"] for row in SEROTONERGIC_INGREDIENT_ROWS],
                "new_product_ids": [row["canonical_product_id"] for row in SEROTONERGIC_PRODUCT_ROWS],
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
