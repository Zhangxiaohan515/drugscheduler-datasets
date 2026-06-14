# Spec 05 — extra_effect_rules

**Layer 3 (RECALL ONLY — user decides polarity/confidence).**
**File:** `curated/extra_effect_rules.json`
**Prerequisite:** `sentence_dict*` must be uploaded to candidate database first.

## Goal
Based on `simple_ingredient_updated.json`, create new extra-effect rules between
ingredient pairs. Recall supporting evidence from the sources below; if it can be
formed into an ingredient-pair rule, draft it — USER sets polarity & confidence.

## Schema (actual fields)
`effect_rule_id, ingredient_pair_id, ingredient_pair_name, ingredient_A_id,
ingredient_A_name, ingredient_B_id, ingredient_B_name, polarity, evidence_text,
Confidence, source_url, "If undefined, then features. Different cases description."`
(196 rows; re-verify max effect_rule_id / EEF numbering live.)

## Extra-effects layer scope (what qualifies)
Physiological response and outcome. A and B act jointly on the host (human/animal/
cell), inducing substantial change in physiological function, disease status,
clinical manifestation, or biomarker level. Examples: toxicity; adverse effects;
tissue damage/protection; survival/recovery; synergistic efficacy; antagonism /
abolished benefit; BP or glucose change; inflammatory markers (IL-6, TNF-alpha);
oxidative-stress markers; apoptosis; clinical biomarkers (IL-6, TNF-alpha, CRP,
LDH, disease-specific).

## Polarity (USER assigns)
Three options: positive, negative, undefined.
- positive extra effect AND positive-inclined → **positive**.
- negative AND negative-inclined → **negative**.
- **undefined** ONLY when both sides can genuinely co-exist under DIFFERENT
  contexts. If negative in some contexts and merely neutral in others → classify
  as **negative** (not undefined). When undefined, fill the
  "different cases description" field with the context split.

## Confidence labels (USER assigns — do not auto-set)
Same four levels as spec 04: High / Medium / Low-medium / Low.

## supp.ai support (confidence adjustment)
Same as spec 04: after drafting from web sources, check `sentence_dict*` for the
same pair; consistent/conflicting evidence raises/lowers confidence. Resolve CUIs
via `cui_metadata`.

## Sources (primary, generally fetchable)
PMC, PubMed, NIH ODS factsheets (ods.od.nih.gov/factsheets/, /pubs/), MSKCC,
NCCIH (nccih.nih.gov/health/), gov.uk drug-safety-update, FDA drug safety,
Frontiers in Neuroscience, AHA journals.
Second-hand & copyrighted (recall only): drugs.com/npp/, drugs.com/drug-interactions/.

## Output
- `extra_effect_rules_increment.json` (DRAFT — polarity/Confidence left for user).
- `needs_review.md` — per-rule evidence summary + tentative read + the exact
  polarity/confidence call the user must make (esp. the undefined-vs-negative test).
