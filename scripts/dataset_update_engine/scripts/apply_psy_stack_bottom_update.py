from __future__ import annotations

import json
from pathlib import Path


ROOT = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "drug_lists"
    / "Real world experiment"
    / "scenario_files"
    / "Biohacker_dataset"
)


def load_json(name: str):
    with (ROOT / name).open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def dump_json(name: str, data) -> None:
    with (ROOT / name).open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


REF_SYNTHETIC = (
    "Full Synthetic Psychiatric Interaction Stack; source candidate database; "
    "dose omitted from curated product row; timing synthetic"
)


NEW_INGREDIENTS = [
    {
        "ingredient_id": "ING-533",
        "ingredient_name": "Lithium Carbonate",
        "category/common_names": "Sleep, Stress & Mood(drug; mood stabilizer/lithium carbonate)",
        "supp.ai source id": "C0085217",
    },
    {
        "ingredient_id": "ING-534",
        "ingredient_name": "Sertraline",
        "category/common_names": "Sleep, Stress & Mood(drug; SSRI antidepressant)",
        "supp.ai source id": "C0074393",
    },
    {
        "ingredient_id": "ING-535",
        "ingredient_name": "Risperidone",
        "category/common_names": "Sleep, Stress & Mood(drug; atypical antipsychotic)",
        "supp.ai source id": "C0073393",
    },
    {
        "ingredient_id": "ING-536",
        "ingredient_name": "Ibuprofen",
        "category/common_names": "Pain, Inflammation & Recovery(OTC drug; NSAID analgesic/anti-inflammatory)",
        "supp.ai source id": "C0020740",
    },
    {
        "ingredient_id": "ING-537",
        "ingredient_name": "Dextromethorphan",
        "category/common_names": "Respiratory & Allergy Support(OTC drug; antitussive/NMDA antagonist)",
        "supp.ai source id": "C0011816",
    },
    {
        "ingredient_id": "ING-538",
        "ingredient_name": "St John's Wort Extract",
        "category/common_names": "Sleep, Stress & Mood(botanical; St John's wort/hypericin)",
        "supp.ai source id": "C0813171",
    },
    {
        "ingredient_id": "ING-539",
        "ingredient_name": "S-Adenosylmethionine (SAMe)",
        "category/common_names": "Sleep, Stress & Mood(methyl donor; SAMe/S-adenosylmethionine)",
        "supp.ai source id": "C0036002",
    },
]


NEW_PRODUCTS = [
    {
        "canonical_product_id": "PROD-469",
        "conceptual_supplement_group": "Panax ginseng",
        "product_concept": "Panax Korean Ginseng",
        "product_brand": "Viva Vitamins",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_psychiatric_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Ginseng",
        "simple_ingredient_id": "ING-122",
        "simple_ingredient_name": "Panax Ginseng Extract",
        "reference_url": "DSLD label_id 237060; candidate database dsld-1/2.jsonl",
        "Notes": REF_SYNTHETIC + "; PSY-11",
        "Functionality": "botanicals",
    },
    {
        "canonical_product_id": "PROD-470",
        "conceptual_supplement_group": "Lithium carbonate",
        "product_concept": "Lithium Carbonate ER",
        "product_brand": "Lithium Carbonate ER",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_psychiatric_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Lithium carbonate",
        "simple_ingredient_id": "ING-533",
        "simple_ingredient_name": "Lithium Carbonate",
        "reference_url": "NDC 42291-496; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": REF_SYNTHETIC + "; PSY-01; NDC pharm_class Mood Stabilizer [EPC]",
        "Functionality": "regulated drugs",
    },
    {
        "canonical_product_id": "PROD-471",
        "conceptual_supplement_group": "Sertraline",
        "product_concept": "Sertraline",
        "product_brand": "Zoloft",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_psychiatric_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Sertraline hydrochloride",
        "simple_ingredient_id": "ING-534",
        "simple_ingredient_name": "Sertraline",
        "reference_url": "NDC 0049-4910; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": REF_SYNTHETIC + "; PSY-02; NDC pharm_class Serotonin Reuptake Inhibitor [EPC]",
        "Functionality": "regulated drugs",
    },
    {
        "canonical_product_id": "PROD-472",
        "conceptual_supplement_group": "Risperidone",
        "product_concept": "Risperidone",
        "product_brand": "RISPERDAL",
        "setting_type": "flexible",
        "recommender": "synthetic_psychiatric_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Risperidone",
        "simple_ingredient_id": "ING-535",
        "simple_ingredient_name": "Risperidone",
        "reference_url": "NDC 50458-320; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": REF_SYNTHETIC + "; PSY-03; NDC pharm_class Atypical Antipsychotic [EPC]",
        "Functionality": "regulated drugs",
    },
    {
        "canonical_product_id": "PROD-473",
        "conceptual_supplement_group": "Ibuprofen",
        "product_concept": "Ibuprofen",
        "product_brand": "Good Sense ibuprofen",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_psychiatric_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Ibuprofen",
        "simple_ingredient_id": "ING-536",
        "simple_ingredient_name": "Ibuprofen",
        "reference_url": "NDC 0113-0298; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": REF_SYNTHETIC + "; PSY-13; NDC pharm_class Nonsteroidal Anti-inflammatory Drug [EPC]",
        "Functionality": "regulated drugs",
    },
    {
        "canonical_product_id": "PROD-474",
        "conceptual_supplement_group": "Dextromethorphan",
        "product_concept": "Dextromethorphan cough product",
        "product_brand": "ROBITUSSIN LONG-ACTING COUGHGELS",
        "setting_type": "flexible",
        "recommender": "synthetic_psychiatric_interaction_stack",
        "expanded_ingredient_name_ofdraft": "Dextromethorphan hydrobromide",
        "simple_ingredient_id": "ING-537",
        "simple_ingredient_name": "Dextromethorphan",
        "reference_url": "NDC 0031-8743; candidate database drug-ndc-slim/ndc-drug-map",
        "Notes": REF_SYNTHETIC + "; PSY-12; NDC pharm_class Sigma-1 Agonist [EPC]; Uncompetitive NMDA Receptor Antagonist [EPC]",
        "Functionality": "regulated drugs",
    },
    {
        "canonical_product_id": "PROD-475",
        "conceptual_supplement_group": "St John's wort",
        "product_concept": "St John's Wort",
        "product_brand": "Vitamin World",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_psychiatric_interaction_stack",
        "expanded_ingredient_name_ofdraft": "St John's Wort",
        "simple_ingredient_id": "ING-538",
        "simple_ingredient_name": "St John's Wort Extract",
        "reference_url": "DSLD label_id 949; candidate database dsld-1/2.jsonl",
        "Notes": REF_SYNTHETIC + "; PSY-07",
        "Functionality": "botanicals",
    },
    {
        "canonical_product_id": "PROD-476",
        "conceptual_supplement_group": "SAMe",
        "product_concept": "SAM-e",
        "product_brand": "GNC",
        "setting_type": "meal_preferred",
        "recommender": "synthetic_psychiatric_interaction_stack",
        "expanded_ingredient_name_ofdraft": "S-Adenosylmethionine",
        "simple_ingredient_id": "ING-539",
        "simple_ingredient_name": "S-Adenosylmethionine (SAMe)",
        "reference_url": "DSLD label_id 665; candidate database dsld-1/2.jsonl",
        "Notes": REF_SYNTHETIC + "; PSY-10",
        "Functionality": "nootropics",
    },
]


NEW_FOODS = [
    {
        "component_id": "FOODC_CAFFEINE",
        "component_name": "Caffeine",
        "food_id": "FOOD-166",
        "food_name": "Monster Energy",
        "food_category": "drink, caffeinated energy drink",
        "Notes": "Full Synthetic Psychiatric Interaction Stack; PSYFOOD-04; caffeine exposure only",
        "source_url": ["user-provided synthetic psychiatric interaction stack"],
    },
    {
        "component_id": "FOODC_CAFFEINE",
        "component_name": "Caffeine",
        "food_id": "FOOD-167",
        "food_name": "Coca-Cola",
        "food_category": "drink, caffeinated soft drink/cola",
        "Notes": "Full Synthetic Psychiatric Interaction Stack; PSYFOOD-06; caffeine exposure only",
        "source_url": ["user-provided synthetic psychiatric interaction stack"],
    },
]


def ensure_absent(rows, key: str, values: list[str]) -> None:
    existing = {row.get(key) for row in rows}
    overlap = sorted(set(values) & existing)
    if overlap:
        raise SystemExit(f"Refusing to append duplicate {key}: {overlap}")


def main() -> None:
    simple = load_json("simple_ingredient_updated.json")
    products = load_json("product_ingredient_mapping.json")
    foods = load_json("food_component_dataset.json")

    ensure_absent(simple, "ingredient_id", [row["ingredient_id"] for row in NEW_INGREDIENTS])
    ensure_absent(products, "canonical_product_id", [row["canonical_product_id"] for row in NEW_PRODUCTS])
    ensure_absent(foods, "food_id", [row["food_id"] for row in NEW_FOODS])

    simple.extend(NEW_INGREDIENTS)
    products.extend(NEW_PRODUCTS)
    foods.extend(NEW_FOODS)

    dump_json("simple_ingredient_updated.json", simple)
    dump_json("product_ingredient_mapping.json", products)
    dump_json("food_component_dataset.json", foods)

    print(
        json.dumps(
            {
                "added_ingredients": [row["ingredient_id"] for row in NEW_INGREDIENTS],
                "added_products": [row["canonical_product_id"] for row in NEW_PRODUCTS],
                "added_foods": [row["food_id"] for row in NEW_FOODS],
                "counts": {
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
