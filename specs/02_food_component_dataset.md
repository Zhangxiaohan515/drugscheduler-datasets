# Spec 02 — food_component_dataset

**Layer 2 (structured judgment). File:** `curated/food_component_dataset.json`

## Goal
When adding a new food, map it to existing `component_id`s. Add a new component
only if truly necessary — prefer reusing current components. The core logic:
identify what component a food item is mainly rich in.

## Schema (actual fields)
`component_id, component_name, food_id, food_name, food_category, Notes, source_url`
- 327 rows currently. Re-verify current max `component_id` and `food_id` live at
  batch start (both increment from their current maxima; never count+1).

## Sources
Primary (fetchable):
- USDA FoodData Central — https://fdc.nal.usda.gov/
- Harvard Nutrition Source — https://nutritionsource.hsph.harvard.edu/food-features/
  (and /what-should-you-eat/protein/, /healthy-drinks/)
- texasrealfood.com nutritargets, honehealth.com, biohackers.world/blog/biohacking-diet
Fallback (often NOT fetchable): Reddit threads — user pastes if needed.

**Dig deeper:** a hub page like `/food-features/` links to specific items; follow
to e.g. `/food-features/chickpeas-garbanzo-beans/`.

## Retention criteria (a food is kept only if)
- it is a meaningful source of a model-relevant component;
- commonly consumed in normal daily/weekly diets;
- frequently appears in biohackers' meals;
- it can generate a plausible food-ingredient rule.

## Granularity rules
- Use a cleaned, general food name — not a recipe name or a hyper-specific DB
  description. Decompose a compound meal into individual food units; map each
  unit to one or more rule-relevant components.
- The selected component = the most important functional feature of that food
  (e.g. vitamin-C-rich, fat-containing).

## Two special carbohydrate components (important)
- `FOODC_STARCHY_CARBOHYDRATE` — main carbohydrate / staple-food context; decides
  whether the food provides a carbohydrate-containing meal context.
- `FOODC_HIGH_GLYCEMIC` — refined / high-glycemic modifier; discriminates white
  rice, bread, bagel, tortilla, white pasta, etc.

## Output
- `food_component_increment.json` — new rows.
- `needs_review.md` — any new component_id proposals (flag for user approval),
  ambiguous component assignments.
