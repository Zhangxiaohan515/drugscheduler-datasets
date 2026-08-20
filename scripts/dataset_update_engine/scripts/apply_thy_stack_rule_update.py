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

LEVOTHYROXINE_DAILYMED = "https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=2883127f-0a2f-492d-a6cb-27ee14de0932"
LEVOTHYROXINE_REVIEW = "https://pmc.ncbi.nlm.nih.gov/articles/PMC8002057/"


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


def update_by_id(rows: list[dict], key: str, updates: dict[str, dict]) -> int:
    updated = 0
    for row in rows:
        row_id = row.get(key)
        if row_id not in updates:
            continue
        changed = False
        for field, value in updates[row_id].items():
            if row.get(field) != value:
                row[field] = value
                changed = True
        if changed:
            updated += 1
    return updated


MECHANISM_MAP_ROWS = [
    {
        "mechanism_id": "MID-AL-ANTACID",
        "mechanism_name": "Aluminum-containing antacid",
        "ingredient_id": "ING-540",
        "ingredient_name": "Aluminum Hydroxide",
    },
]


MECHANISM_RULE_UPDATES = {
    "MEC-119": {
        "evidence_text": "Calcium carbonate reduces levothyroxine absorption by forming insoluble complexes in the gut; the levothyroxine label directs administration at least 4 hours apart from calcium carbonate, and review evidence supports a 2-4 hour separation for calcium formulations.",
        "evidence_scope": "prescription levothyroxine label / human absorption evidence",
        "scheduling_implication": "Hard-separate calcium-containing products or calcium-rich food from levothyroxine / desiccated thyroid by at least 4 hours.",
        "source_url": [LEVOTHYROXINE_DAILYMED, LEVOTHYROXINE_REVIEW],
    },
    "MEC-120": {
        "evidence_text": "Ferrous sulfate likely forms a ferric-thyroxine complex and reduces levothyroxine absorption; the levothyroxine label directs administration at least 4 hours apart from ferrous sulfate, with review evidence also associating iron supplementation with increased TSH.",
        "evidence_scope": "prescription levothyroxine label / human absorption evidence",
        "scheduling_implication": "Hard-separate iron salts from levothyroxine / desiccated thyroid by at least 4 hours.",
        "source_urls": [LEVOTHYROXINE_DAILYMED, LEVOTHYROXINE_REVIEW],
    },
    "MEC-121": {
        "evidence_text": "Magnesium-containing antacid or laxative preparations can reduce levothyroxine absorption in formulation-specific contexts. The levothyroxine label identifies aluminum- and magnesium-containing hydroxide antacids as agents that can alter gastric acidity and reduce absorption; the broad magnesium mechanism remains minor because ordinary magnesium supplement forms are less certain than antacid preparations.",
        "evidence_scope": "prescription levothyroxine label plus formulation-specific antacid/laxative evidence",
        "scheduling_implication": "Soft separation rule from levothyroxine, especially for magnesium-containing antacids, laxatives, carbonate, or high-dose mineral preparations.",
        "source_urls": [LEVOTHYROXINE_DAILYMED, "https://pubmed.ncbi.nlm.nih.gov/10193669/", "https://pmc.ncbi.nlm.nih.gov/articles/PMC12605969/"],
    },
}


MECHANISM_RULE_ROWS = [
    {
        "rule_id": "MEC-226",
        "from_id": "MID-AL-ANTACID",
        "from_mechanism_name": "Aluminum-containing antacid",
        "to_id": "MID-THYROID-HORMONE",
        "to_mechanism_name": "Thyroid hormone replacement (T4 / desiccated)",
        "directionality": "directional",
        "polarity": "negative",
        "strength": "moderate",
        "mechanism_type": "gastric pH alteration / antacid-associated levothyroxine absorption reduction",
        "evidence_text": "Aluminum-containing antacid preparations can impair levothyroxine efficacy. The levothyroxine label lists aluminum hydroxide antacids among agents that may reduce absorption by altering gastric acidity, and review evidence reports impaired efficacy with aluminum hydroxide preparations.",
        "evidence_confidence": "medium",
        "evidence_scope": "prescription levothyroxine label / systematic-review antacid evidence",
        "scheduling_implication": "Separate aluminum-containing antacids from levothyroxine / desiccated thyroid; the label's general absorption-interfering-drug interval is at least 4 hours.",
        "source_url": [LEVOTHYROXINE_DAILYMED, LEVOTHYROXINE_REVIEW],
    },
    {
        "rule_id": "MEC-227",
        "from_id": "MID-CR",
        "from_mechanism_name": "Chromium",
        "to_id": "MID-THYROID-HORMONE",
        "to_mechanism_name": "Thyroid hormone replacement (T4 / desiccated)",
        "directionality": "directional",
        "polarity": "negative",
        "strength": "moderate",
        "mechanism_type": "adsorption or poorly soluble complex formation reducing levothyroxine absorption",
        "evidence_text": "Chromium picolinate may reduce levothyroxine bioavailability, plausibly through adsorption or poorly soluble complex formation. Evidence is limited relative to calcium and iron, with the review identifying a small non-randomized crossover study and recommending delayed chromium administration.",
        "evidence_confidence": "medium",
        "evidence_scope": "limited human crossover evidence summarized in systematic review",
        "scheduling_implication": "Separate chromium picolinate from levothyroxine / desiccated thyroid; the review suggests delaying chromium by 3-4 hours.",
        "source_url": [LEVOTHYROXINE_REVIEW],
    },
    {
        "rule_id": "MEC-228",
        "from_id": "MID-PSYLLIUM",
        "from_mechanism_name": "Psyllium husk soluble fiber",
        "to_id": "MID-THYROID-HORMONE",
        "to_mechanism_name": "Thyroid hormone replacement (T4 / desiccated)",
        "directionality": "directional",
        "polarity": "negative",
        "strength": "minor",
        "mechanism_type": "fiber adsorption / modest levothyroxine absorption reduction",
        "evidence_text": "Psyllium may modestly reduce levothyroxine absorption through fiber adsorption. The review describes broader fiber-associated levothyroxine efficacy concerns, while a small psyllium study found only a limited decrease that was considered unlikely to be clinically significant.",
        "evidence_confidence": "medium",
        "evidence_scope": "low-medium clinical relevance represented as medium so mechanism aggregation retains the rule",
        "scheduling_implication": "Record a weak separation signal for psyllium and levothyroxine; optimizer impact is intentionally minimal because negative minor currently has zero utility penalty.",
        "source_url": [LEVOTHYROXINE_REVIEW],
    },
]


FOOD_COMPONENT_RULE_UPDATES = {
    "FCIR-019": {
        "evidence_text": "Calcium-rich foods and calcium-containing products can reduce levothyroxine absorption; the levothyroxine label directs separation from absorption-interfering agents, and milk evidence in the systematic review showed reduced T4 exposure when levothyroxine was taken with calcium-containing cow milk.",
        "source_url": [LEVOTHYROXINE_DAILYMED, LEVOTHYROXINE_REVIEW],
    },
    "FCIR-044": {
        "evidence_text": "Soy protein and other meal protein contexts can reduce levothyroxine exposure or efficacy. The levothyroxine label cautions against administration in soybean-based infant formula, and systematic-review evidence describes soy protein interactions and normalization after separating soy intake from levothyroxine.",
        "source_url": [LEVOTHYROXINE_DAILYMED, LEVOTHYROXINE_REVIEW],
    },
    "FCIR-070": {
        "evidence_text": "Dietary fiber can bind or adsorb levothyroxine and reduce treatment efficacy; the systematic review summarizes fiber-associated reductions in levothyroxine effectiveness, so high-fiber meals remain hard-separated from levothyroxine.",
        "source_url": [LEVOTHYROXINE_REVIEW],
    },
    "FCIR-119": {
        "evidence_text": "Coffee is represented through FOODC_POLYPHENOL_TANNIN for levothyroxine. Systematic-review evidence reports reduced and delayed T4 exposure when levothyroxine tablets were taken with coffee, with case evidence improving after separating coffee by about 1 hour.",
        "source_url": [LEVOTHYROXINE_REVIEW],
    },
}


def main() -> None:
    mechanism_rules = load_json("mechanism_rules.json")
    mechanism_map = load_json("mechanism_ingredient_map.json")
    food_component_rules = load_json("food_component_ingredient_rules.json")

    added_map = append_missing_mechanism_map(mechanism_map, MECHANISM_MAP_ROWS)
    updated_mechanism = update_by_id(mechanism_rules, "rule_id", MECHANISM_RULE_UPDATES)
    added_mechanism = append_missing(mechanism_rules, MECHANISM_RULE_ROWS, "rule_id")
    updated_food = update_by_id(food_component_rules, "rule_id", FOOD_COMPONENT_RULE_UPDATES)

    dump_json("mechanism_rules.json", mechanism_rules)
    dump_json("mechanism_ingredient_map.json", mechanism_map)
    dump_json("food_component_ingredient_rules.json", food_component_rules)

    print(
        json.dumps(
            {
                "added": {
                    "mechanism_ingredient_map": added_map,
                    "mechanism_rules": added_mechanism,
                },
                "updated": {
                    "mechanism_rules": updated_mechanism,
                    "food_component_ingredient_rules": updated_food,
                },
                "ids": {
                    "mechanism_ingredient_map": [
                        f"{row['mechanism_id']} -> {row['ingredient_id']}" for row in MECHANISM_MAP_ROWS
                    ],
                    "mechanism_rules_added": [row["rule_id"] for row in MECHANISM_RULE_ROWS],
                    "mechanism_rules_updated": sorted(MECHANISM_RULE_UPDATES),
                    "food_component_ingredient_rules_updated": sorted(FOOD_COMPONENT_RULE_UPDATES),
                },
                "totals": {
                    "mechanism_ingredient_map": len(mechanism_map),
                    "mechanism_rules": len(mechanism_rules),
                    "food_component_ingredient_rules": len(food_component_rules),
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
