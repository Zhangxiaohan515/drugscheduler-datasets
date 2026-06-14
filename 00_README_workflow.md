# DrugScheduler Dataset Extension — Workflow Overview

This folder contains six independent batch specs. Each one is a self-contained
prompt for extending ONE dataset. Do not mix datasets in a single batch.

## Repository layout
- `curated/` — the authoritative datasets we are extending (the deliverables).
- `candidate database/` — large reference sources used for RECALL only, never
  copied wholesale into curated. Files:
  - `cui_metadata.json` — SUPP.AI CUI dictionary (4,910 CUIs). Used to match
    ingredients to a CUI and to validate any CUI we encounter.
  - `drug-ndc-slim-1/2/3.json` — 128,746 NDC drug records (name, pharm_class,
    active_ingredients, rxcui, unii). No CUI; match via cui_metadata.
  - `ndc-drug-map-1/2.json` — NDC→CUI prematched (complement to slim; ~44% of
    its CUIs validate against cui_metadata, so treat its CUI with caution).
  - `dsld-1/2.jsonl` — 92,041 supplement products → ingredient + CUI (CUIs
    validate 100% against cui_metadata; granularity may still differ from ours).
  - `sentence_dict*` — SUPP.AI evidence sentences for mechanism/extra-effect
    support. (NOT YET UPLOADED — must be slimmed/split first; prerequisite for
    specs 04 and 05.)

## How to start any batch (four-part launch)
When opening a batch, provide:
1. **Target** — which dataset + the exact scope (e.g. "add David Sinclair's stack").
2. **Format anchor** — the relevant spec file + current max ID (see each spec).
3. **Sources** — which URLs / which candidate file to use this batch.
4. **Rules** — already encoded in each spec; restate anything that changed.

## Non-negotiable principles (apply to every batch)
- **Increment, never overwrite.** Output is a NEW incremental JSON (new rows
  only) plus a "needs-your-judgment" list. The user merges into curated.
- **Recall vs judgment split.** Claude does mechanical recall (search, match,
  dedup, format). The user decides granularity, polarity, confidence, and which
  evidence to accept. Higher layers (mechanism, extra-effect) = recall only.
- **ID continuity.** New IDs continue from the current MAX id (IDs may have
  gaps; never use count+1). Current maxima are listed in each spec and must be
  re-checked against the live file at batch start.
- **Copyright.** Extract structured FACTS from web sources; never copy article
  text verbatim. Drugs.com / DrugBank are second-hand & copyrighted — fine for
  recall, but trace to a primary source before citing as strong evidence.
- **Source reachability.** PMC / PubMed / NIH ODS / Oregon State LPI / journal
  sites are usually fetchable. Reddit and Amazon are often NOT (dynamic / anti-
  bot) — treat as fallback; user pastes content if fetch fails.

## Current dataset state (re-verify at batch start)
| dataset | rows | id field | current max |
|---|---|---|---|
| simple_ingredient_updated | 374 | ingredient_id | ING-390 |
| product_ingredient_mapping | 1024 | canonical_product_id | PROD-279 |
| food_component_dataset | 327 | component_id / food_id | (see spec 02) |
| food_component_ingredient_rules | 259 | rule_id (FCIR) | (see spec 06) |
| mechanism_rules | 148 | rule_id | (see spec 04) |
| mechanism_ingredient_map | 409 | mechanism_id | (see spec 04) |
| extra_effect_rules | 196 | effect_rule_id (EEF) | (see spec 05) |
| food_routine | 73 | — | (see spec 03) |

## Layered automation guidance
- **Layer 1 (mechanical, semi-auto OK):** spec 01 (ingredient + product + drug).
- **Layer 2 (structured judgment):** specs 02, 03, 06 (food + food-rules).
- **Layer 3 (recall only, user judges):** specs 04, 05 (mechanism + extra-effect)
  — the academic core; never auto-decide confidence/polarity.
