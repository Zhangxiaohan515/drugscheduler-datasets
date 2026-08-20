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
    "Full Synthetic Hepatotoxic-Burden Stack; source candidate database; "
    "dose omitted from curated product row; timing synthetic"
)


HEP_INGREDIENT_ROWS = [
    {
        "ingredient_id": "ING-547",
        "ingredient_name": "Garcinia Cambogia Extract",
        "category/common_names": "Metabolic & Cardiovascular Health(botanical; garcinia/hydroxycitric-acid extract)",
        "supp.ai source id": "C2983133",
    },
    {
        "ingredient_id": "ING-548",
        "ingredient_name": "Black Cohosh Extract",
        "category/common_names": "Hormonal, Reproductive & Sexual Health(botanical; black cohosh/cimicifuga extract)",
        "supp.ai source id": "C0771967",
    },
    {
        "ingredient_id": "ING-549",
        "ingredient_name": "Comfrey",
        "category/common_names": "Immune & Organ Support(botanical; comfrey/pyrrolizidine-alkaloid exposure)",
        "supp.ai source id": "C0522466",
    },
    {
        "ingredient_id": "ING-550",
        "ingredient_name": "Epigallocatechin Gallate",
        "category/common_names": "Longevity & Healthy Aging(polyphenol; EGCG/green-tea catechin)",
        "supp.ai source id": "C0059438",
    },
    {
        "ingredient_id": "ING-551",
        "ingredient_name": "Tea, Black Extract",
        "category/common_names": "Cognitive Performance & Energy(botanical; black-tea extract/theaflavins)",
        "supp.ai source id": "C1572543",
    },
    {
        "ingredient_id": "ING-552",
        "ingredient_name": "Acetaminophen",
        "category/common_names": "Pain, Inflammation & Recovery(drug; acetaminophen/paracetamol analgesic)",
        "supp.ai source id": "C0000970",
    },
]


HEP_PRODUCT_ROWS = [
    {
        "canonical_product_id": "PROD-495",
        "conceptual_supplement_group": "Green tea extract",
        "product_concept": "EGCg Green Tea Extract",
        "product_brand": "NOW",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Green Tea Extract",
        "simple_ingredient_id": "ING-106",
        "simple_ingredient_name": "Green tea extract / Camellia sinensis",
        "reference_url": "DSLD label_id 13654; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-03; DSLD single-ingredient green-tea/EGCG candidate",
        "Functionality": "botanicals",
    },
    {
        "canonical_product_id": "PROD-496",
        "conceptual_supplement_group": "Garcinia cambogia",
        "product_concept": "Garcinia cambogia Extract",
        "product_brand": "TerraVita Premium Collection",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Garcinia Cambogia Extract",
        "simple_ingredient_id": "ING-547",
        "simple_ingredient_name": "Garcinia Cambogia Extract",
        "reference_url": "DSLD label_id 286612; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-05; DSLD single-ingredient garcinia/HCA candidate",
        "Functionality": "botanicals",
    },
    {
        "canonical_product_id": "PROD-497",
        "conceptual_supplement_group": "Red yeast rice",
        "product_concept": "Red Yeast Rice",
        "product_brand": "NOW",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Red Yeast Rice",
        "simple_ingredient_id": "ING-181",
        "simple_ingredient_name": "Monacolin K, Red Yeast Rice",
        "reference_url": "DSLD label_id 15287; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-06; DSLD red-yeast-rice product candidate; mapped to existing monacolin K/red yeast rice ingredient",
        "Functionality": "cardiometabolic",
    },
    {
        "canonical_product_id": "PROD-498",
        "conceptual_supplement_group": "Black cohosh",
        "product_concept": "Black Cohosh Root",
        "product_brand": "Gaia Herbs",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Black Cohosh Extract",
        "simple_ingredient_id": "ING-548",
        "simple_ingredient_name": "Black Cohosh Extract",
        "reference_url": "DSLD label_id 10203; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-07; DSLD single-ingredient black-cohosh candidate",
        "Functionality": "botanicals",
    },
    {
        "canonical_product_id": "PROD-499",
        "conceptual_supplement_group": "Comfrey",
        "product_concept": "Comfrey Leaf",
        "product_brand": "TerraVita Premium Collection",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Comfrey",
        "simple_ingredient_id": "ING-549",
        "simple_ingredient_name": "Comfrey",
        "reference_url": "DSLD label_id 286677; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-10; DSLD single-ingredient comfrey candidate",
        "Functionality": "botanicals",
    },
    {
        "canonical_product_id": "PROD-504",
        "conceptual_supplement_group": "Kratom",
        "product_concept": "Zenith NANO Liquid Kratom Extract",
        "product_brand": "Kraken Kratom",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Kratom / Mitragyna speciosa",
        "simple_ingredient_id": "ING-268",
        "simple_ingredient_name": "Kratom / Mitragyna speciosa",
        "reference_url": "DSLD label_id 298015; candidate database dsld-2.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-09; DSLD product-name kratom candidate; mapped manually to existing kratom ingredient because structured DSLD ingredients only captured nutrition-facts minerals/vitamins",
        "Functionality": "botanicals",
    },
    {
        "canonical_product_id": "PROD-500",
        "conceptual_supplement_group": "Hydroxycut",
        "product_concept": "Hydroxycut",
        "product_brand": "Hydroxycut",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Caffeine",
        "simple_ingredient_id": "ING-108",
        "simple_ingredient_name": "Caffeine",
        "reference_url": "DSLD label_id 3296; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-11; DSLD multi-ingredient Hydroxycut candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-500",
        "conceptual_supplement_group": "Hydroxycut",
        "product_concept": "Hydroxycut",
        "product_brand": "Hydroxycut",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Potassium",
        "simple_ingredient_id": "ING-194",
        "simple_ingredient_name": "potassium",
        "reference_url": "DSLD label_id 3296; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-11; DSLD multi-ingredient Hydroxycut candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-500",
        "conceptual_supplement_group": "Hydroxycut",
        "product_concept": "Hydroxycut",
        "product_brand": "Hydroxycut",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Epigallocatechin Gallate",
        "simple_ingredient_id": "ING-550",
        "simple_ingredient_name": "Epigallocatechin Gallate",
        "reference_url": "DSLD label_id 3296; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-11; DSLD multi-ingredient Hydroxycut candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-500",
        "conceptual_supplement_group": "Hydroxycut",
        "product_concept": "Hydroxycut",
        "product_brand": "Hydroxycut",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Ginger",
        "simple_ingredient_id": "ING-133",
        "simple_ingredient_name": "ginger root",
        "reference_url": "DSLD label_id 3296; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-11; DSLD multi-ingredient Hydroxycut candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-500",
        "conceptual_supplement_group": "Hydroxycut",
        "product_concept": "Hydroxycut",
        "product_brand": "Hydroxycut",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Chromium Picolinate",
        "simple_ingredient_id": "ING-034",
        "simple_ingredient_name": "Chromium",
        "reference_url": "DSLD label_id 3296; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-11; DSLD multi-ingredient Hydroxycut candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-500",
        "conceptual_supplement_group": "Hydroxycut",
        "product_concept": "Hydroxycut",
        "product_brand": "Hydroxycut",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Green Tea Extract",
        "simple_ingredient_id": "ING-106",
        "simple_ingredient_name": "Green tea extract / Camellia sinensis",
        "reference_url": "DSLD label_id 3296; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-11; DSLD multi-ingredient Hydroxycut candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-500",
        "conceptual_supplement_group": "Hydroxycut",
        "product_concept": "Hydroxycut",
        "product_brand": "Hydroxycut",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Quercetin Dihydrate",
        "simple_ingredient_id": "ING-051",
        "simple_ingredient_name": "Quercetin",
        "reference_url": "DSLD label_id 3296; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-11; DSLD multi-ingredient Hydroxycut candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-500",
        "conceptual_supplement_group": "Hydroxycut",
        "product_concept": "Hydroxycut",
        "product_brand": "Hydroxycut",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Garcinia Cambogia Extract",
        "simple_ingredient_id": "ING-547",
        "simple_ingredient_name": "Garcinia Cambogia Extract",
        "reference_url": "DSLD label_id 3296; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-11; DSLD multi-ingredient Hydroxycut candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-500",
        "conceptual_supplement_group": "Hydroxycut",
        "product_concept": "Hydroxycut",
        "product_brand": "Hydroxycut",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Calcium Supplement",
        "simple_ingredient_id": "ING-030",
        "simple_ingredient_name": "Calcium",
        "reference_url": "DSLD label_id 3296; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-11; DSLD multi-ingredient Hydroxycut candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-501",
        "conceptual_supplement_group": "Herbalife multi-ingredient product",
        "product_concept": "Total Control",
        "product_brand": "Herbalife",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Caffeine",
        "simple_ingredient_id": "ING-108",
        "simple_ingredient_name": "Caffeine",
        "reference_url": "DSLD label_id 3980; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-12; DSLD multi-ingredient Herbalife candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-501",
        "conceptual_supplement_group": "Herbalife multi-ingredient product",
        "product_concept": "Total Control",
        "product_brand": "Herbalife",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Ginger",
        "simple_ingredient_id": "ING-133",
        "simple_ingredient_name": "ginger root",
        "reference_url": "DSLD label_id 3980; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-12; DSLD multi-ingredient Herbalife candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-501",
        "conceptual_supplement_group": "Herbalife multi-ingredient product",
        "product_concept": "Total Control",
        "product_brand": "Herbalife",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Tea, Black Extract",
        "simple_ingredient_id": "ING-551",
        "simple_ingredient_name": "Tea, Black Extract",
        "reference_url": "DSLD label_id 3980; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-12; DSLD multi-ingredient Herbalife candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-501",
        "conceptual_supplement_group": "Herbalife multi-ingredient product",
        "product_concept": "Total Control",
        "product_brand": "Herbalife",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Green Tea Extract",
        "simple_ingredient_id": "ING-106",
        "simple_ingredient_name": "Green tea extract / Camellia sinensis",
        "reference_url": "DSLD label_id 3980; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-12; DSLD multi-ingredient Herbalife candidate",
        "Functionality": "weight management",
    },
    {
        "canonical_product_id": "PROD-502",
        "conceptual_supplement_group": "Niacin",
        "product_concept": "Real Niacin (As Nicotinic Acid)",
        "product_brand": "Doctor's Best",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Niacin",
        "simple_ingredient_id": "ING-006",
        "simple_ingredient_name": "Niacin, Vitamin B3",
        "reference_url": "DSLD label_id 25013; candidate database dsld-1.jsonl",
        "Notes": REF_SYNTHETIC + "; HEP-13; DSLD single-ingredient nicotinic-acid candidate",
        "Functionality": "essential nutrients",
    },
    {
        "canonical_product_id": "PROD-503",
        "conceptual_supplement_group": "Acetaminophen",
        "product_concept": "Tylenol Extra Strength Caplet",
        "product_brand": "Tylenol",
        "setting_type": "flexible",
        "recommender": "synthetic_hepatotoxic_burden_stack",
        "expanded_ingredient_name_ofdraft": "Acetaminophen",
        "simple_ingredient_id": "ING-552",
        "simple_ingredient_name": "Acetaminophen",
        "reference_url": "NDC 67414-449; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": REF_SYNTHETIC + "; HEP-14; NDC single-active-ingredient acetaminophen candidate",
        "Functionality": "regulated drugs",
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
        HEP_PRODUCT_ROWS,
        HEP_INGREDIENT_ROWS,
        known_ingredient_ids,
    )
    if not check["passed"]:
        raise SystemExit(json.dumps(check, ensure_ascii=False, indent=2))

    added_ingredients = append_missing(simple, HEP_INGREDIENT_ROWS, "ingredient_id")
    added_product_rows = append_missing_product_rows(products, HEP_PRODUCT_ROWS)

    dump_json("simple_ingredient_updated.json", simple)
    dump_json("product_ingredient_mapping.json", products)

    print(
        json.dumps(
            {
                "added": {
                    "simple_ingredient_updated": added_ingredients,
                    "product_ingredient_mapping_rows": added_product_rows,
                },
                "new_ingredient_ids": [row["ingredient_id"] for row in HEP_INGREDIENT_ROWS],
                "new_product_ids": sorted({row["canonical_product_id"] for row in HEP_PRODUCT_ROWS}),
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
