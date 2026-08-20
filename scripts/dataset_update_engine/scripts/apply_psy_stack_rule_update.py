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

LITHIUM_DAILYMED = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=d20ed2aa-aa56-4709-9e7a-9243c71465c9"
SERTRALINE_DAILYMED = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=205ecf52-8138-44a7-ad9a-b3aa7f4fa11a"
CAFFEINE_LITHIUM_CASE = "https://www.psychiatrist.com/pcc/sudden-reduction-in-caffeine-intake-increases-serum-lithium-concentration-to-supratherapeutic-level-a-case-report/"


def load_json(name: str) -> list[dict]:
    with (ROOT / name).open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def dump_json(name: str, rows: list[dict]) -> None:
    with (ROOT / name).open("w", encoding="utf-8") as f:
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


def append_missing_mechanism_map(rows: list[dict], additions: list[dict]) -> int:
    existing = {(row.get("mechanism_id"), row.get("ingredient_id")) for row in rows}
    added = 0
    for row in additions:
        key = (row.get("mechanism_id"), row.get("ingredient_id"))
        if key in existing:
            continue
        rows.append(row)
        existing.add(key)
        added += 1
    return added


def append_missing_food_component_rule(rows: list[dict], additions: list[dict]) -> int:
    existing = {
        (row.get("food_component_id"), row.get("target_ingredient_id"), row.get("polarity"), row.get("rule_type"))
        for row in rows
    }
    added = 0
    for row in additions:
        key = (row.get("food_component_id"), row.get("target_ingredient_id"), row.get("polarity"), row.get("rule_type"))
        if key in existing:
            continue
        rows.append(row)
        existing.add(key)
        added += 1
    return added


MECHANISM_MAP_ROWS = [
    {
        "mechanism_id": "MID-LI",
        "mechanism_name": "Lithium",
        "ingredient_id": "ING-533",
        "ingredient_name": "Lithium Carbonate",
    },
    {
        "mechanism_id": "MID-NSAID",
        "mechanism_name": "Nonsteroidal anti-inflammatory drug (NSAID)",
        "ingredient_id": "ING-536",
        "ingredient_name": "Ibuprofen",
    },
]


MECHANISM_RULE_ROWS = [
    {
        "rule_id": "MEC-225",
        "from_id": "MID-NSAID",
        "from_mechanism_name": "Nonsteroidal anti-inflammatory drug (NSAID)",
        "to_id": "MID-LI",
        "to_mechanism_name": "Lithium",
        "directionality": "directional",
        "polarity": "negative",
        "strength": "major",
        "mechanism_type": "NSAID-mediated reduction in renal lithium clearance",
        "evidence_text": "NSAIDs decrease renal blood flow, resulting in decreased renal lithium clearance and increased serum lithium concentrations.",
        "evidence_confidence": "high",
        "evidence_scope": "prescription lithium label / renal clearance interaction",
        "scheduling_implication": "Avoid optional ibuprofen co-use with lithium when possible; consider alternative analgesic or serum lithium monitoring if clinically necessary.",
        "source_url": LITHIUM_DAILYMED,
    },
]


EXTRA_EFFECT_RULE_ROWS = [
    {
        "effect_rule_id": "EFF282",
        "ingredient_pair_id": "ING-533 * ING-534",
        "ingredient_pair_name": "Lithium Carbonate * Sertraline",
        "ingredient_A_id": "ING-533",
        "ingredient_A_name": "Lithium Carbonate",
        "ingredient_B_id": "ING-534",
        "ingredient_B_name": "Sertraline",
        "polarity": "negative",
        "evidence_text": "Lithium can precipitate serotonin syndrome, and risk is increased with concomitant serotonergic drugs such as SSRIs; sertraline labeling also lists lithium among serotonergic drugs that increase serotonin-syndrome risk.",
        "Confidence": "high",
        "source_url": [LITHIUM_DAILYMED, SERTRALINE_DAILYMED],
        "If undefined, then features. Different cases description.": None,
    },
    {
        "effect_rule_id": "EFF283",
        "ingredient_pair_id": "ING-533 * ING-538",
        "ingredient_pair_name": "Lithium Carbonate * St John's Wort Extract",
        "ingredient_A_id": "ING-533",
        "ingredient_A_name": "Lithium Carbonate",
        "ingredient_B_id": "ING-538",
        "ingredient_B_name": "St John's Wort Extract",
        "polarity": "negative",
        "evidence_text": "Lithium labeling warns that serotonin-syndrome risk is increased with concomitant serotonergic drugs and specifically lists St. John's Wort.",
        "Confidence": "high",
        "source_url": [LITHIUM_DAILYMED],
        "If undefined, then features. Different cases description.": None,
    },
    {
        "effect_rule_id": "EFF284",
        "ingredient_pair_id": "ING-533 * ING-228",
        "ingredient_pair_name": "Lithium Carbonate * L-Tryptophan",
        "ingredient_A_id": "ING-533",
        "ingredient_A_name": "Lithium Carbonate",
        "ingredient_B_id": "ING-228",
        "ingredient_B_name": "L-Tryptophan",
        "polarity": "negative",
        "evidence_text": "Lithium labeling warns that serotonin-syndrome risk is increased with concomitant serotonergic drugs and specifically lists tryptophan.",
        "Confidence": "high",
        "source_url": [LITHIUM_DAILYMED],
        "If undefined, then features. Different cases description.": None,
    },
    {
        "effect_rule_id": "EFF285",
        "ingredient_pair_id": "ING-533 * ING-535",
        "ingredient_pair_name": "Lithium Carbonate * Risperidone",
        "ingredient_A_id": "ING-533",
        "ingredient_A_name": "Lithium Carbonate",
        "ingredient_B_id": "ING-535",
        "ingredient_B_name": "Risperidone",
        "polarity": "negative",
        "evidence_text": "Lithium labeling describes neurotoxic reactions with concomitant antipsychotic drugs, ranging from extrapyramidal symptoms to neuroleptic malignant syndrome and encephalopathic syndrome. Risperidone is modeled as the atypical antipsychotic exposure in this synthetic stack.",
        "Confidence": "medium",
        "source_url": [LITHIUM_DAILYMED],
        "If undefined, then features. Different cases description.": None,
    },
    {
        "effect_rule_id": "EFF286",
        "ingredient_pair_id": "ING-534 * ING-536",
        "ingredient_pair_name": "Sertraline * Ibuprofen",
        "ingredient_A_id": "ING-534",
        "ingredient_A_name": "Sertraline",
        "ingredient_B_id": "ING-536",
        "ingredient_B_name": "Ibuprofen",
        "polarity": "negative",
        "evidence_text": "Sertraline labeling warns of increased bleeding risk with drugs that interfere with hemostasis, including NSAIDs.",
        "Confidence": "high",
        "source_url": [SERTRALINE_DAILYMED],
        "If undefined, then features. Different cases description.": None,
    },
    {
        "effect_rule_id": "EFF287",
        "ingredient_pair_id": "ING-534 * ING-537",
        "ingredient_pair_name": "Sertraline * Dextromethorphan",
        "ingredient_A_id": "ING-534",
        "ingredient_A_name": "Sertraline",
        "ingredient_B_id": "ING-537",
        "ingredient_B_name": "Dextromethorphan",
        "polarity": "negative",
        "evidence_text": "Sertraline labeling warns that other serotonergic drugs increase serotonin-syndrome risk and lists dextromethorphan as a CYP2D6 substrate whose exposure may be increased by sertraline.",
        "Confidence": "high",
        "source_url": [SERTRALINE_DAILYMED],
        "If undefined, then features. Different cases description.": None,
    },
]


FOOD_COMPONENT_INGREDIENT_RULE_ROWS = [
    {
        "rule_id": "FCIR-430",
        "food_component_id": "FOODC_CAFFEINE",
        "food_component_name": "Caffeine",
        "target_ingredient_id": "ING-533",
        "target_ingredient_name": "Lithium Carbonate",
        "polarity": "negative",
        "rule_type": "soft",
        "score": -1,
        "parameter_effect": "gamma_adjust",
        "evidence_text": "Caffeine may increase renal lithium excretion through diuretic and renal hemodynamic effects; abrupt caffeine reduction has been associated with supratherapeutic lithium concentrations, so caffeine exposure is modeled as a lithium-stability concern rather than a simple nutrient support.",
        "source_url": [CAFFEINE_LITHIUM_CASE],
    },
]


def main() -> None:
    mechanism_rules = load_json("mechanism_rules.json")
    mechanism_map = load_json("mechanism_ingredient_map.json")
    extra_effect_rules = load_json("extra_effect_rules.json")
    food_component_rules = load_json("food_component_ingredient_rules.json")

    added_map = append_missing_mechanism_map(mechanism_map, MECHANISM_MAP_ROWS)
    added_mechanism = append_missing(mechanism_rules, MECHANISM_RULE_ROWS, "rule_id")
    added_extra = append_missing(extra_effect_rules, EXTRA_EFFECT_RULE_ROWS, "effect_rule_id")
    added_food = append_missing_food_component_rule(food_component_rules, FOOD_COMPONENT_INGREDIENT_RULE_ROWS)

    dump_json("mechanism_rules.json", mechanism_rules)
    dump_json("mechanism_ingredient_map.json", mechanism_map)
    dump_json("extra_effect_rules.json", extra_effect_rules)
    dump_json("food_component_ingredient_rules.json", food_component_rules)

    print(
        json.dumps(
            {
                "added": {
                    "mechanism_ingredient_map": added_map,
                    "mechanism_rules": added_mechanism,
                    "extra_effect_rules": added_extra,
                    "food_component_ingredient_rules": added_food,
                },
                "ids": {
                    "mechanism_rules": [row["rule_id"] for row in MECHANISM_RULE_ROWS],
                    "extra_effect_rules": [row["effect_rule_id"] for row in EXTRA_EFFECT_RULE_ROWS],
                    "food_component_ingredient_rules": [row["rule_id"] for row in FOOD_COMPONENT_INGREDIENT_RULE_ROWS],
                },
                "totals": {
                    "mechanism_ingredient_map": len(mechanism_map),
                    "mechanism_rules": len(mechanism_rules),
                    "extra_effect_rules": len(extra_effect_rules),
                    "food_component_ingredient_rules": len(food_component_rules),
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
