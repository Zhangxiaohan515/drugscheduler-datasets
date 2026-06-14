# Spec 04 — mechanism_ingredient_map + mechanism_rules

**Layer 3 (RECALL ONLY — user decides directionality/polarity/strength/confidence).**
**Files:** `curated/mechanism_ingredient_map.json`, `curated/mechanism_rules.json`
**Prerequisite:** `sentence_dict*` must be uploaded to candidate database first.

## Goal
1. Map new ingredients to an existing `mechanism_id` via mechanism_ingredient_map;
   if none fits, propose a NEW mechanism_id (flag for user) and record it.
2. Find candidate interaction rules between two ingredients / two mechanism_ids;
   gather supporting info from the sources below; Claude recalls and drafts,
   the USER sets polarity/strength/confidence and accepts/rejects.

## mechanism_ingredient_map — schema & granularity
Fields: `mechanism_id, mechanism_name, ingredient_id, ingredient_name` (409 rows).
- **Mechanism-layer granularity = the active molecular entity** that directly
  participates in the interaction. Merge different salts / forms / delivery
  systems when they provide the same active entity and there is no form-specific
  interaction evidence. (e.g. Mg glycinate / L-threonate / citrate / oxide /
  malate / chloride → one magnesium-ion family.)
- **IMPORTANT double granularity:** the SAME new ingredient is recorded at FINE
  granularity in simple_ingredient (e.g. "Magnesium L-Threonate, Magtein") but at
  FAMILY granularity here (e.g. "Magnesium ion"). Keep both layers consistent
  with their own rule. Probiotic strains may stay more specific.

## mechanism_rules — schema
Fields: `rule_id, from_id, from_mechanism_name, to_id, to_mechanism_name,
directionality, polarity, strength, mechanism_type, evidence_text,
evidence_confidence, evidence_scope, scheduling_implication, source_url,
supp.ai support` (148 rows; re-verify max rule_id live).

## Mechanism layer scope (what qualifies)
Changes in solution, absorption, exposure, concentration, processing. A affects B
via physical/chemical/biological means, altering exposure/concentration/
absorption/transport/metabolism/clearance of B. Examples: physical/chemical
binding; chelation/complex formation; dissolution/solubility change; intestinal
permeability/uptake; gastric pH / gastric emptying; absorption/bioavailability;
exposure (AUC, Cmax) change; enzyme induction/inhibition (CYP); transporter
modulation (P-gp).

## Confidence labels (USER assigns — do not auto-set)
- **High:** strong clinical/authoritative evidence, fairly direct conclusion.
- **Medium:** multiple supporting studies, often in vivo/animal, clinical not fully established.
- **Low-medium:** some support, much in vitro / indirect; may include hints it
  doesn't clearly appear in vivo.
- **Low:** weak, indirect, or very sparse.

## supp.ai support (confidence adjustment)
SUPP.AI is a candidate pool that can RAISE or LOWER a rule's confidence. After
drafting a rule from the web sources, query `sentence_dict*` for evidence on the
same pair; if found and consistent/conflicting, adjust confidence accordingly and
note it in `supp.ai support`. Use `cui_metadata` to resolve the pair's CUIs.

## Sources (primary, generally fetchable)
Oregon State LPI (lpi.oregonstate.edu/mic/ — dig e.g. /minerals/magnesium,
/vitamins/vitamin-K), PMC, NCBI Books, PubMed, ScienceDirect, jn.nutrition.org,
AHA journals, medRxiv, OUP JCEM, MDPI, Cambridge BJN.
Second-hand & copyrighted (recall only, trace to primary): drugs.com/drug-interactions/,
go.drugbank.com/drugs/. medsafe.govt.nz.

## Output
- `mechanism_rules_increment.json` (DRAFT — confidence/polarity/strength left for user).
- `mechanism_ingredient_map_increment.json` (new mappings; new mechanism_ids flagged).
- `needs_review.md` — every rule's evidence summary + Claude's tentative read +
  the specific judgment the user must make. This file is the heart of the batch.
