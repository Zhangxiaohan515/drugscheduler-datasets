from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from dataset_update_engine.config import EngineConfig
from dataset_update_engine.project_paths import DatasetPaths
from dataset_update_engine.update_pipeline import UpdateEngine


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


class EngineFixture:
    def __init__(self, root: Path, config: EngineConfig | None = None):
        self.root = root
        self.curated = root / "curated"
        self.candidate = root / "candidate"
        self.specs = root / "specs"
        self.runs = root / "runs"
        self.experiment = root / "experiment_curated"
        self.paths = DatasetPaths(root, root, self.curated, self.candidate, self.specs, self.runs, self.experiment)
        self.config = config or EngineConfig(
            category_to_setting_type={
                "multivitamin": "meal_preferred",
                "mineral": "meal_preferred",
                "probiotic": "wake_empty_preferred",
                "nootropic": "special_time_required",
                "sleep_support": "bed_empty_preferred",
            },
            category_defaults={
                "mineral": {"setting_type": "meal_preferred", "special_time": None, "functionality": "essential nutrients"},
                "nootropic": {"setting_type": "special_time_required", "special_time": "before_4pm", "functionality": "cognitive support"},
            },
            mechanism_aliases=[],
            compile_checks={"daily": {"enabled": True}},
            suppai_matching_policy={"semantic_similarity": "disabled"},
        )
        self._write_curated()

    def _write_curated(self) -> None:
        write_json(
            self.paths.simple_ingredients,
            [
                {
                    "ingredient_id": "ING-001",
                    "ingredient_name": "Magnesium",
                    "category/common_names": "mineral",
                }
            ],
        )
        write_json(
            self.paths.product_ingredient_mapping,
            [
                {
                    "canonical_product_id": "PROD-001",
                    "conceptual_supplement_group": "Existing Product",
                    "product_concept": "Existing Product",
                    "product_brand": "Existing Brand",
                    "setting_type": "meal_preferred",
                    "recommender": "Tim",
                    "expanded_ingredient_name_ofdraft": "Magnesium",
                    "simple_ingredient_id": "ING-001",
                    "simple_ingredient_name": "Magnesium",
                    "reference_url": "",
                    "Notes": "",
                    "Functionality": "mineral",
                }
            ],
        )
        write_json(self.paths.mechanism_ingredient_map, [])
        write_json(self.paths.mechanism_rules, [])
        write_json(self.paths.extra_effect_rules, [])
        write_json(self.paths.food_component_dataset, [])
        write_json(self.paths.food_component_ingredient_rules, [])
        write_json(self.paths.food_routine, [])
        write_json(
            self.paths.cui_metadata,
            {
                "C1234567": {
                    "preferred_name": "New Exact Ingredient",
                    "definition": "A supplement ingredient.",
                    "synonyms": ["Exact Ingredient Alias"],
                    "tradenames": [],
                }
            },
        )

    def engine(self) -> UpdateEngine:
        return UpdateEngine(paths=self.paths, config=self.config)


class DatasetUpdateEngineTests(unittest.TestCase):
    def test_plan_update_dry_run_keeps_bottom_layer_out_of_curated(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fixture = EngineFixture(Path(td))
            update_path = Path(td) / "update.json"
            write_json(
                update_path,
                {
                    "products": [
                        {
                            "product_brand": "FocusBrand",
                            "product_concept": "Focus Stack",
                            "category": "nootropic",
                            "recommender": "Tim",
                            "ingredients": [{"name": "New Exact Ingredient"}],
                        }
                    ]
                },
            )

            run_dir = fixture.engine().plan_update(update_path, run_id="run1")
            bottom = json.loads((run_dir / "bottom_layer_dry_run.json").read_text(encoding="utf-8"))
            candidates = json.loads((run_dir / "review_candidates.json").read_text(encoding="utf-8"))
            daily = json.loads((run_dir / "daily_compile_check.json").read_text(encoding="utf-8"))

            product_row = bottom["product_ingredient_mapping"][0]
            ingredient_row = bottom["simple_ingredient_updated"][0]
            self.assertEqual(product_row["setting_type"], "special_time_required")
            self.assertEqual(product_row["special_time"], "before_4pm")
            self.assertNotIn("needs_review", product_row)
            self.assertNotIn("review_status", product_row)
            self.assertNotIn("needs_review", ingredient_row)
            self.assertEqual(ingredient_row["supp.ai source id"], "C1234567")
            self.assertEqual(candidates["new_mechanism_families"][0]["review_status"], "needs_review")
            self.assertTrue(daily["passed"])
            self.assertEqual(len(json.loads(fixture.paths.product_ingredient_mapping.read_text(encoding="utf-8"))), 1)

    def test_auto_update_directly_appends_bottom_layer_rows(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fixture = EngineFixture(Path(td))
            update_path = Path(td) / "update.json"
            write_json(
                update_path,
                {
                    "products": [
                        {
                            "product_brand": "MineralBrand",
                            "product_concept": "Trace Mineral",
                            "category": "mineral",
                            "recommender": "Tim",
                            "ingredients": [{"name": "New Exact Ingredient", "category": "mineral"}],
                        }
                    ]
                },
            )
            run_dir = fixture.engine().auto_update(update_path, run_id="run2")

            report = json.loads((run_dir / "bottom_layer_apply_report.json").read_text(encoding="utf-8"))
            product_rows = json.loads(fixture.paths.product_ingredient_mapping.read_text(encoding="utf-8"))
            ingredient_rows = json.loads(fixture.paths.simple_ingredients.read_text(encoding="utf-8"))

            self.assertEqual(report["mode"], "bottom_layer_auto_applied")
            self.assertEqual(report["applied_counts"]["product_ingredient_mapping"], 1)
            self.assertEqual(report["applied_counts"]["simple_ingredient_updated"], 1)
            self.assertEqual(len(product_rows), 2)
            self.assertEqual(len(ingredient_rows), 2)
            self.assertNotIn("needs_review", product_rows[0])
            self.assertNotIn("review_status", ingredient_rows[-1])

    def test_mechanism_family_auto_draft_requires_exact_whitelist_alias(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            config = EngineConfig(
                category_to_setting_type={"mineral": "meal_preferred"},
                category_defaults={"mineral": {"setting_type": "meal_preferred", "special_time": None, "functionality": "essential nutrients"}},
                mechanism_aliases=[
                    {"alias": "magnesium", "mechanism_id": "MID-MG", "mechanism_name": "Magnesium"}
                ],
                compile_checks={"daily": {"enabled": True}},
                suppai_matching_policy={"semantic_similarity": "disabled"},
            )
            fixture = EngineFixture(Path(td), config=config)
            update_path = Path(td) / "update.json"
            write_json(
                update_path,
                {
                    "products": [
                        {
                            "product_brand": "A",
                            "product_concept": "Known Family",
                            "category": "mineral",
                            "recommender": "Tim",
                            "ingredients": [{"name": "New Exact Ingredient", "category": "mineral", "mechanism_family": "magnesium"}],
                        },
                        {
                            "product_brand": "B",
                            "product_concept": "Fuzzy Family",
                            "category": "mineral",
                            "recommender": "Tim",
                            "ingredients": [{"name": "Another Ingredient", "category": "mineral", "mechanism_family": "magnesium-like"}],
                        },
                    ]
                },
            )

            run_dir = fixture.engine().plan_update(update_path, run_id="run3")
            bottom = json.loads((run_dir / "bottom_layer_dry_run.json").read_text(encoding="utf-8"))
            candidates = json.loads((run_dir / "review_candidates.json").read_text(encoding="utf-8"))

            self.assertEqual(len(bottom["mechanism_ingredient_map"]), 1)
            self.assertEqual(bottom["mechanism_ingredient_map"][0]["mechanism_id"], "MID-MG")
            self.assertEqual(len(candidates["mechanism_family_assignments"]), 1)
            self.assertEqual(candidates["mechanism_family_assignments"][0]["review_status"], "needs_review")

    def test_existing_brand_and_concept_skips_product_regardless_of_ingredients(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fixture = EngineFixture(Path(td))
            update_path = Path(td) / "update.json"
            write_json(
                update_path,
                {
                    "products": [
                        {
                            "product_brand": "Existing Brand",
                            "product_concept": "Existing Product",
                            "category": "mineral",
                            "recommender": "Someone Else",
                            "ingredients": [{"name": "New Exact Ingredient", "category": "mineral"}],
                        }
                    ]
                },
            )

            run_dir = fixture.engine().plan_update(update_path, run_id="run4")
            bottom = json.loads((run_dir / "bottom_layer_dry_run.json").read_text(encoding="utf-8"))
            self.assertEqual(bottom["product_ingredient_mapping"], [])
            self.assertEqual(bottom["simple_ingredient_updated"], [])

    def test_existing_curated_product_covers_synthetic_product_before_drafting(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fixture = EngineFixture(Path(td))
            update_path = Path(td) / "update.json"
            write_json(
                update_path,
                {
                    "products": [
                        {
                            "product_brand": "Synthetic Magnesium Product",
                            "product_concept": "Synthetic Magnesium Product",
                            "category": "mineral",
                            "recommender": "synthetic",
                            "ingredients": [{"name": "Magnesium"}],
                        }
                    ]
                },
            )

            run_dir = fixture.engine().plan_update(update_path, run_id="run5")
            bottom = json.loads((run_dir / "bottom_layer_dry_run.json").read_text(encoding="utf-8"))
            search = json.loads((run_dir / "source_search_report.json").read_text(encoding="utf-8"))

            self.assertEqual(bottom["product_ingredient_mapping"], [])
            self.assertEqual(bottom["simple_ingredient_updated"], [])
            self.assertEqual(search["items"][0]["selected_source"], "biohacker_curated_product")
            self.assertEqual(search["items"][0]["recommendation"], "use_existing_biohacker_product")


if __name__ == "__main__":
    unittest.main()
