# Spec 06 — food_component_ingredient_rules (FCIR)

**Layer 2 (structured judgment). File:** `curated/food_component_ingredient_rules.json`

## Goal
Create new rules from a food COMPONENT to an INGREDIENT.
- component must match `food_component_dataset.json` (component_id + component_name);
- ingredient must match `simple_ingredient_updated.json` (ingredient_id + name).
Consider how each component affects supplements and drugs.

## Schema (actual fields)
`rule_id, food_component_id, food_component_name, target_ingredient_id,
target_ingredient_name, polarity, rule_type, score, parameter_effect,
evidence_text, source_url` (259 rows; rule_id uses FCIR numbering — re-verify
current max live, e.g. FCIR-XXX).

## Retention criteria (keep a rule if)
- mechanistically plausible, OR
- commonly recommended in nutrition/clinical practice, OR
- supported by high-quality sources (nutrient fact sheets, biomedical reviews,
  drug labels, clinical guidance).

## Family-level expansion
Expand family-level interactions to all relevant ingredient forms when
appropriate — e.g. zinc / magnesium rules expand across their salt forms; vitamin
B12 or omega-3 rules expand across the corresponding variants.

## Classification
- **polarity:** positive | negative.
- **rule_type:** hard | soft. Most rules are SOFT.
  - **soft** = a timing preference / penalty, not an absolute feasibility limit.
  - **hard positive** = ingredient MUST be taken with a specific meal context for
    the rule to hold.
  - **hard negative** = food component must be AVOIDED with the ingredient because
    the interaction creates a clinically meaningful safety risk or badly harms
    drug efficacy.
- **score / parameter_effect:** match the model's food/special-time parameter set.

## Sources (primary, generally fetchable)
NIH ODS factsheets, Oregon State LPI (incl. /mic/dietary-factors/), NCBI Books/PMC,
Mayo Clinic, ScienceDirect, Harvard Nutrition Source, examine.com, medlineplus,
dailymed, NCCIH, ISAPP, journals (AJM, LWW).
Second-hand & copyrighted (recall only): drugs.com/food-interactions/, drugs.com/npp/,
goodrx, singlecare, patient.info, consumerlab, naturemade, nutraingredients,
thepaleomom, livonlabs, apdaparkinson, cyalcohol.

## Output
- `fcir_increment.json` — new rules.
- `needs_review.md` — hard-vs-soft calls, polarity, family-expansion choices.
