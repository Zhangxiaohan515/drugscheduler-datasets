# Spec 01 — simple_ingredient + product_ingredient_mapping (+ drug ingestion)

**Layer 1 (mechanical, semi-automatable). Files:**
`curated/simple_ingredient_updated.json`, `curated/product_ingredient_mapping.json`

## Goal
Collect a recommender's (biohacker's) supplement/drug stack, then:
1. add each brand product to `product_ingredient_mapping.json`;
2. add any not-yet-present ingredients to `simple_ingredient_updated.json`.
Many famous biohackers are not yet in the dataset — follow this logic to extend.

## Source priority (changed from original — candidate-first)
1. **DSLD candidate** (`dsld-1/2.jsonl`) — first stop for a supplement's
   ingredients + CUI. 92k products.
2. **NDC candidates** (`drug-ndc-slim*`, `ndc-drug-map*`) — for drugs.
3. **Biohacker list pages** (fetchable, primary recall for "who takes what"):
   - fastlifehacks.com (Ferriss, Huberman, Attia, Rogan, Patrick, Sinclair, B. Johnson)
   - geneusdna.com (Brecka), drhyman.com (Hyman), mynucleus.com / omre.co (B. Johnson)
   - routines.club, humantonik.com, novoslabs.com (Asprey)
   - honehealth.com, wellnesspulse.com, brainflow.co, jrelibrary.com, nmn.com
   - For a specific brand, dig the anchor link, e.g.
     `fastlifehacks.com/tim-ferriss-supplements-what-he-takes-and-why/#Magnesium_L-Threonate`
4. **Brand official site** (supplement facts page) — when DSLD lacks it.
5. **Amazon / sellers** — LAST resort only; usually NOT fetchable. User pastes.

Extract structured facts only (brand, ingredient, dose, form, source URL). No verbatim text.

## product_ingredient_mapping — schema & rules
Fields: `canonical_product_id, conceptual_supplement_group, product_concept,
product_brand, setting_type, recommender, expanded_ingredient_name_ofdraft,
simple_ingredient_id, simple_ingredient_name, reference_url, Notes, Functionality`

- **One product per brand.** Two fish oils from different brands (Carlson vs
  Momentous) are two distinct products, even if the ingredient is the same.
- **One row per ingredient** in a product (multi-ingredient product → multiple
  rows sharing the same `canonical_product_id`).
- **Current max:** `PROD-279`. New products continue from PROD-280 (re-verify live).
- **setting_type** comes from the supplement's food/time context:
  - soft: `meal_preferred, wake_empty_preferred, bed_empty_preferred, gap_preferred, flexible` (tune gamma/eta)
  - hard: `meal_required, wake_empty_required, bed_empty_required, gap_required, special_time_required` (tune alpha_meal/alpha_gap)
- **Field provenance:** `product_brand, product_concept, expanded_ingredient_name,
  reference_url` come from the web. `setting_type, Functionality, Notes,
  recommender` are curation judgments — fill from context or leave for user.

## simple_ingredient — schema & rules
Fields: `ingredient_id, ingredient_name, category/common_names, supp.ai source id`
- **Dedup first:** check each candidate ingredient against existing 374 rows
  (programmatic normalize-and-compare, not by eye) before assigning a new ID.
- **Current max:** `ING-390`. New ingredients continue from ING-391 (re-verify live).
- **CUI matching:** match name (and synonyms) against `cui_metadata.json`.
  - exact / synonym hit → fill `supp.ai source id`.
  - **no match → OMIT the field entirely** (do not write null/empty).
  - ambiguous granularity (e.g. "Magnesium" → element vs salt forms) → DO NOT
    auto-pick; list candidates for the user to choose.
- **category/common_names format:** `BigClass(subclass; common_names)`.
  - supplements: e.g. `Essential(vitamin; B12/cobalamin)`. Categories include
    essential nutrients, longevity compounds, nootropics, performance, gut-health,
    botanicals, regulated drugs, others.
  - **drugs (prescription drugs use the SAME ING numbering):** BigClass = `Drug`,
    subclass = the EPC tag from NDC `pharm_class`, common = functional descriptor.
    e.g. `Drug(SSRI; antidepressant)`. Drugs match CUI the same way (many drugs
    ARE in cui_metadata, e.g. Escitalopram = C1099456).

## Output of a batch
- `mapping_increment_<recommender>.json` — new mapping rows (curation fields may be blank).
- `ingredient_increment_<recommender>.json` — new ingredient rows.
- `needs_review_<recommender>.md` — CUI granularity choices, dedup near-matches,
  blanks needing the user's curation judgment.
