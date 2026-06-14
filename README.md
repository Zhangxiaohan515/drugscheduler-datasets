# drugscheduler-datasets

Curated datasets and candidate reference databases for **DrugScheduler** — a MILP-based system that optimizes the timing of supplement and drug intake under
mechanism, extra-effect, and food/special-time interaction rules.

This repository is organized into **three folders** that work together as a pipeline: raw reference material (`candidate database/`) is turned into curated
deliverables (`curated/`) under the procedures documented in (`specs/`).

```
candidate database/   →   specs/   →   curated/
   (raw material)        (how-to)      (deliverable)
```

---

## The three folders introduction

| Folder | Role | Edited by |
|---|---|---|
| `curated/` | The datasets we build, extend, and ship | Incremental, reviewed before merge |
| `candidate database/` | Large reference pools used for **recall only** | Read-only reference, not edited |
| `specs/` | The procedures that turn candidates into curated entries | Manually maintained |

---

## 1. `curated/` — the deliverables

These are the datasets the model consumes. They are what we actively **extend and keep complete**. Eight files, organized by layer:

| File | Rows | What it holds |
|---|---|---|
| `simple_ingredient_updated.json` | 374 | Canonical ingredient vocabulary (supplements + drugs share one namespace), with category and SUPP.AI CUI when matched |
| `product_ingredient_mapping.json` | 1024 | Brand product ↔ ingredient relations, with recommender, setting type, and source |
| `mechanism_ingredient_map.json` | 409 | Ingredients mapped to mechanism-level entities (salt forms merged to the active entity) |
| `mechanism_rules.json` | 148 | Mechanism interactions (absorption / exposure / metabolism), with directionality, polarity, strength, confidence |
| `extra_effect_rules.json` | 196 | Physiological-outcome interactions between ingredient pairs, with polarity and confidence |
| `food_component_dataset.json` | 327 | Food items mapped to the components they mainly provide |
| `food_component_ingredient_rules.json` | 259 | Rules from a food component to an ingredient, classified hard/soft + polarity |
| `food_routine.json` | 73 | Meal timing and composition, mapped to food items |

**Not all extension is equal.** Each dataset sits in one of three tiers by how much human judgment it needs:

- **Tier 1 — mechanical (semi-automated):** simple ingredient, product mapping, drug ingestion. Mostly fact collection, CUI matching, and formatting.
- **Tier 2 — structured judgment:** food component, food routine, food-component-ingredient rules. Clear rules, but each entry is reviewed.
- **Tier 3 — recall only, human decides:** mechanism rules, extra-effect rules. These are the academic core; **confidence and polarity are never assigned
  automatically** — the assistant recalls evidence, the curator decides.

The output of any extension is always an **incremental file plus a needs-review list**, merged into `curated/` only after the curator checks it.

---

## 2. `candidate database/` — the reference pools

Large public sources used **only to recall information** — never copied wholesale into `curated/`. They make the back end "knowledgeable" so the assistant can find ingredients, match CUIs, and surface supporting evidence on demand.

| File(s) | Source | Used for |
|---|---|---|
| `cui_metadata.json` | SUPP.AI | CUI dictionary (4,910 CUIs); match ingredients to a CUI and validate any CUI |
| `dsld-1/2.jsonl` | DSLD | 92k supplement products → ingredient + CUI (supplement recall) |
| `drug-ndc-slim-1/2/3.json` | openFDA NDC | 128k drug records (name, pharm_class, ingredients, rxcui, unii) |
| `ndc-drug-map-1/2.json` | openFDA → SUPP.AI | NDC→CUI prematched (drug CUI, complement to slim) |
| `sentence_dict_1/2/3.json` | SUPP.AI | 16k+ CUI-pair evidence sentences with paper IDs (mechanism / extra-effect support) |

**How it affects curated extension:** when we add a new ingredient, product, or rule, the candidate pools provide the starting facts — a supplement's
ingredients (DSLD), a drug's composition (NDC), a CUI (cui_metadata), or supporting sentences for an interaction (sentence_dict). The candidates supply
**facts and evidence**; the curator supplies **judgment**. A candidate value is never trusted blindly — CUIs are validated against `cui_metadata`, and granularity mismatches are flagged for review.

---

## 3. `specs/` — the procedures

Seven Markdown files that define exactly how to extend each dataset. They are the bridge between the other two folders: they tell the assistant which candidate pool to query, which sources to use, what format and ID scheme to follow, and what to output.

| File | Covers |
|---|---|
| `00_README_workflow.md` | Shared rules: folder layout, ID continuity, copyright, recall-vs-judgment, source reachability, current dataset state, the three tiers |
| `01_ingredient_and_product.md` | simple ingredient + product mapping + drug ingestion (Tier 1) |
| `02_food_component_dataset.md` | food component dataset (Tier 2) |
| `03_food_routine.md` | food routine (Tier 2) |
| `04_mechanism_rules.md` | mechanism map + mechanism rules (Tier 3, recall only) |
| `05_extra_effect_rules.md` | extra-effect rules (Tier 3, recall only) |
| `06_food_component_ingredient_rules.md` | food-component-ingredient rules (Tier 2) |

**How specs call the databases:** to run a batch, point the assistant at one spec (e.g. "extend product mapping per `specs/01`"). The spec names the relevant candidate file(s); the assistant fetches them, performs the recall and matching described in the spec, follows the curated format and ID scheme, and returns an increment plus a review list. One batch = one dataset = one spec, keeping each task focused and each result checkable.

---

## How the three folders interact (end to end)

1. A batch starts from a **spec** in `specs/`, which defines the task, format, and which candidate pool to use.
2. The assistant queries the relevant **candidate database** pool to recall facts (ingredients, CUIs) or evidence (sentences), validating CUIs against
   `cui_metadata`.
3. The assistant produces an **increment + needs-review list** in the **curated** format. For Tier 3 (mechanism / extra-effect), it only drafts and
   recalls evidence — confidence and polarity are decided by the curator.
4. The curator reviews, edits, and merges the increment into `curated/`.

This keeps the curated datasets growing steadily while staying accurate: the candidate pools give breadth, the specs give consistency, and human review
guards quality on the judgment-heavy layers.
