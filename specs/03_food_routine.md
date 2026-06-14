# Spec 03 — food_routine

**Layer 2 (structured judgment). File:** `curated/food_routine.json`

## Goal
A food routine focuses on MEAL TIMING and what is in each meal. For each meal:
split it into food items; map each food item to its `food_id` in
`food_component_dataset.json`. If a food item in a meal is not yet in
food_component_dataset, ADD it there first (name + id + main component), then
reference it here. (So spec 03 and spec 02 are linked — adding a routine may
require adding foods upstream.)

## Structure
Currently 73 entries (list). Re-verify structure live at batch start; follow the
exact existing format for routine entries and their meal/timing fields.

## Sources
Biohacker style:
- https://www.biohackers.world/blog/biohacking-diet/
- https://honehealth.com/edge/bryan-johnson-diet/
Non-biohacker style (often NOT fetchable — user pastes if needed):
- taste.com.au galleries, Reddit (r/easyrecipes, r/DinnerTonight)

For more sources: biohacker meal patterns → biohacker sites; non-biohacker →
Reddit meal threads.

## Output
- `food_routine_increment.json` — new routine entries.
- `food_component_increment.json` — any new foods that had to be added upstream.
- `needs_review.md` — meal-to-food-unit splits that need confirmation.
