from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import Any

from .candidate_search import CandidateSourceSearcher, covered_input_indexes
from .config import EngineConfig
from .id_generator import reserve_next
from .json_io import dump_json, read_rows
from .normalization import clean_text, normalize_name
from .project_paths import DatasetPaths, default_paths
from .review_exporter import write_review_table, write_review_workbook
from .suppai_matcher import SuppAiMatcher
from .update_input_loader import parse_update_file
from .update_validator import run_daily_compile_check, validate_ingredient_row, validate_product_row


def _now_run_id() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def _index_by_normalized_name(rows: list[dict[str, Any]], name_key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = normalize_name(row.get(name_key))
        if key and key not in out:
            out[key] = row
    return out


def _existing_ids(rows: list[dict[str, Any]], key: str) -> set[str]:
    return {clean_text(row.get(key)) for row in rows if clean_text(row.get(key))}


def _mechanism_id_from_name(name: str, existing_ids: set[str]) -> str:
    slug = re.sub(r"[^A-Z0-9]+", "-", normalize_name(name).upper()).strip("-")
    slug = slug[:30] or "NEW"
    candidate = f"MID-{slug}"
    if candidate not in existing_ids:
        return candidate
    i = 2
    while f"{candidate}-{i}" in existing_ids:
        i += 1
    return f"{candidate}-{i}"


class UpdateEngine:
    def __init__(self, paths: DatasetPaths | None = None, config: EngineConfig | None = None):
        self.paths = paths or default_paths()
        self.config = config or EngineConfig.load()

    def plan_update(self, input_path: Path, out_dir: Path | None = None, run_id: str | None = None) -> Path:
        """Dry-run entry: creates the same review bundle without editing curated JSON."""
        return self._run_update(input_path, out_dir=out_dir, run_id=run_id, apply_bottom_layer=False)

    def auto_update(self, input_path: Path, out_dir: Path | None = None, run_id: str | None = None) -> Path:
        """Main entry: directly writes deterministic bottom-layer rows to curated JSON."""
        return self._run_update(input_path, out_dir=out_dir, run_id=run_id, apply_bottom_layer=True)

    def _run_update(
        self,
        input_path: Path,
        *,
        out_dir: Path | None,
        run_id: str | None,
        apply_bottom_layer: bool,
    ) -> Path:
        package = parse_update_file(input_path)
        run_id = run_id or _now_run_id()
        out_dir = out_dir or (self.paths.review_runs_dir / run_id)
        out_dir.mkdir(parents=True, exist_ok=True)

        curated = self._load_curated()
        search_report = CandidateSourceSearcher(self.paths).search_package(package, curated)
        bottom, review_candidates, review_rows, coverage = self._build_bottom_layer_update(
            package,
            curated,
            covered_products=covered_input_indexes(search_report),
        )
        daily_check = run_daily_compile_check(
            bottom["product_ingredient_mapping"],
            bottom["simple_ingredient_updated"],
            _existing_ids(curated["simple_ingredients"], "ingredient_id"),
        )

        apply_report = {
            "mode": "dry_run",
            "applied_counts": {},
            "skipped_bottom_rows": [],
        }
        if apply_bottom_layer:
            apply_report = self._apply_bottom_layer(bottom, curated)
            curated_after = self._load_curated()
            daily_check = run_daily_compile_check([], [], _existing_ids(curated_after["simple_ingredients"], "ingredient_id"))

        dump_json(package, out_dir / "canonical_input.json")
        dump_json(search_report, out_dir / "source_search_report.json")
        bottom_filename = "bottom_layer_auto_applied.json" if apply_bottom_layer else "bottom_layer_dry_run.json"
        dump_json(bottom, out_dir / bottom_filename)
        dump_json(review_candidates, out_dir / "review_candidates.json")
        dump_json(coverage, out_dir / "coverage_audit.json")
        dump_json(daily_check, out_dir / "daily_compile_check.json")
        dump_json(apply_report, out_dir / "bottom_layer_apply_report.json")
        write_review_table(review_rows, out_dir / "review_table.csv")
        write_review_workbook(review_rows, out_dir / "review_table.xlsx")
        (out_dir / "audit_report.md").write_text(
            self._render_audit_report(run_id, bottom, review_candidates, coverage, daily_check, apply_report),
            encoding="utf-8",
        )
        return out_dir

    def _load_curated(self) -> dict[str, list[dict[str, Any]]]:
        return {
            "simple_ingredients": read_rows(self.paths.simple_ingredients),
            "product_mapping": read_rows(self.paths.product_ingredient_mapping),
            "mechanism_ingredient_map": read_rows(self.paths.mechanism_ingredient_map),
            "mechanism_rules": read_rows(self.paths.mechanism_rules),
            "extra_effect_rules": read_rows(self.paths.extra_effect_rules),
            "food_component_dataset": read_rows(self.paths.food_component_dataset),
            "food_component_ingredient_rules": read_rows(self.paths.food_component_ingredient_rules),
            "food_routine": read_rows(self.paths.food_routine),
        }

    def _build_bottom_layer_update(
        self,
        package: dict[str, Any],
        curated: dict[str, list[dict[str, Any]]],
        *,
        covered_products: set[int] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
        covered_products = covered_products or set()
        existing_ingredients = _index_by_normalized_name(curated["simple_ingredients"], "ingredient_name")
        existing_foods = _index_by_normalized_name(curated["food_component_dataset"], "food_name")
        existing_products = {
            (
                normalize_name(row.get("product_brand")),
                normalize_name(row.get("product_concept")),
            )
            for row in curated["product_mapping"]
        }
        existing_ingredient_ids = _existing_ids(curated["simple_ingredients"], "ingredient_id")
        existing_product_ids = _existing_ids(curated["product_mapping"], "canonical_product_id")
        existing_mechanism_ids = _existing_ids(curated["mechanism_ingredient_map"], "mechanism_id")
        concept_defaults = self._product_concept_defaults(curated["product_mapping"])

        ingredient_ids = set(existing_ingredient_ids)
        product_ids = set(existing_product_ids)
        bottom_ingredient_by_name: dict[str, dict[str, Any]] = {}
        blocked_ingredient_names: set[str] = set()
        bottom_product_rows: list[dict[str, Any]] = []
        bottom_mechanism_rows: list[dict[str, Any]] = []
        blocked_bottom_rows: list[dict[str, Any]] = []

        review_candidates: dict[str, list[dict[str, Any]]] = {
            "suppai_matches": [],
            "mechanism_family_assignments": [],
            "new_mechanism_families": [],
            "new_rules": [],
            "food_items": [],
            "components": [],
        }
        review_rows: list[dict[str, Any]] = []

        suppai = SuppAiMatcher(self.paths.cui_metadata)
        mechanism_aliases = self._mechanism_alias_lookup()
        exact_mechanism_pairs: set[tuple[str, str]] = {
            (clean_text(row.get("ingredient_id")), clean_text(row.get("mechanism_id")))
            for row in curated["mechanism_ingredient_map"]
        }

        for product_index, product in enumerate(package["products"]):
            if product_index in covered_products:
                continue

            brand = clean_text(product.get("product_brand"))
            concept = clean_text(product.get("product_concept"))
            recommender = clean_text(product.get("recommender"))
            product_key = (normalize_name(brand), normalize_name(concept))
            if product_key in existing_products:
                continue
            existing_products.add(product_key)

            product_id = reserve_next(product_ids, "PROD")
            category = clean_text(product.get("category")).lower()
            defaults = {
                **self.config.category_defaults.get(category, {}),
                **concept_defaults.get(normalize_name(concept), {}),
            }
            setting_type = clean_text(product.get("setting_type") or defaults.get("setting_type"))
            special_time = clean_text(product.get("special_time") or defaults.get("special_time"))
            functionality = clean_text(
                product.get("functionality")
                or product.get("Functionality")
                or defaults.get("functionality")
                or category
            )

            ingredients = product.get("ingredients") or []
            for ingredient in ingredients:
                ing_name = clean_text(ingredient.get("name") or ingredient.get("ingredient_name"))
                if not ing_name:
                    continue

                existing_ing = existing_ingredients.get(normalize_name(ing_name))
                if existing_ing:
                    ing_id = clean_text(existing_ing.get("ingredient_id"))
                    simple_name = clean_text(existing_ing.get("ingredient_name"))
                else:
                    ing_norm = normalize_name(ing_name)
                    draft_ing = bottom_ingredient_by_name.get(ing_norm)
                    if not draft_ing:
                        ing_id = reserve_next(ingredient_ids, "ING")
                        category_names = clean_text(
                            ingredient.get("category")
                            or ingredient.get("functional_category")
                            or product.get("category")
                            or functionality
                        )
                        draft_ing = {
                            "ingredient_id": ing_id,
                            "ingredient_name": ing_name,
                            "category/common_names": category_names,
                        }
                        suppai_match = suppai.match(ing_name, clean_text(ingredient.get("definition")))
                        if suppai_match["status"] == "exact_preferred_match":
                            draft_ing["supp.ai source id"] = suppai_match["cui"]
                        elif suppai_match["status"] != "no_match":
                            review_candidates["suppai_matches"].append(
                                {
                                    "ingredient_id": ing_id,
                                    "ingredient_name": ing_name,
                                    "review_status": "needs_review",
                                    "match_status": suppai_match["status"],
                                    "candidates": suppai_match.get("candidates", []),
                                }
                            )
                        errors = validate_ingredient_row(draft_ing)
                        if errors:
                            blocked_ingredient_names.add(ing_norm)
                            blocked_bottom_rows.append(
                                {
                                    "target_file": "simple_ingredient_updated.json",
                                    "row": draft_ing,
                                    "errors": errors,
                                }
                            )
                        else:
                            bottom_ingredient_by_name[ing_norm] = draft_ing
                    if ing_norm in blocked_ingredient_names:
                        blocked_bottom_rows.append(
                            {
                                "target_file": "product_ingredient_mapping.json",
                                "row": {
                                    "product_concept": concept,
                                    "product_brand": brand,
                                    "expanded_ingredient_name_ofdraft": ing_name,
                                },
                                "errors": ["referenced ingredient skeleton was blocked"],
                            }
                        )
                        continue
                    ing_id = clean_text(draft_ing["ingredient_id"])
                    simple_name = clean_text(draft_ing["ingredient_name"])

                row = {
                    "canonical_product_id": product_id,
                    "conceptual_supplement_group": clean_text(product.get("conceptual_supplement_group") or concept),
                    "product_concept": concept,
                    "product_brand": brand,
                    "setting_type": setting_type,
                    "recommender": recommender,
                    "expanded_ingredient_name_ofdraft": ing_name,
                    "simple_ingredient_id": ing_id,
                    "simple_ingredient_name": simple_name,
                    "reference_url": clean_text(product.get("reference_url")),
                    "Notes": clean_text(product.get("notes") or product.get("Notes")),
                    "Functionality": functionality,
                }
                if special_time:
                    row["special_time"] = special_time

                validation_errors = validate_product_row(row, existing_ingredient_ids | ingredient_ids)
                if validation_errors:
                    blocked_bottom_rows.append(
                        {
                            "target_file": "product_ingredient_mapping.json",
                            "row": row,
                            "errors": validation_errors,
                        }
                    )
                else:
                    bottom_product_rows.append(row)

                mechanism_hint = clean_text(ingredient.get("mechanism_family") or ingredient.get("mechanism_id"))
                if mechanism_hint:
                    mechanism = mechanism_aliases.get(normalize_name(mechanism_hint))
                    if mechanism:
                        pair = (ing_id, mechanism["mechanism_id"])
                        if pair not in exact_mechanism_pairs:
                            bottom_mechanism_rows.append(
                                {
                                    "mechanism_id": mechanism["mechanism_id"],
                                    "mechanism_name": mechanism["mechanism_name"],
                                    "ingredient_id": ing_id,
                                    "ingredient_name": simple_name,
                                }
                            )
                            exact_mechanism_pairs.add(pair)
                    else:
                        self._add_review_row(
                            review_rows,
                            item_type="mechanism_family_assignment",
                            display_name=f"{simple_name} -> {mechanism_hint}",
                            reason="not an exact approved mechanism family alias",
                        )
                        review_candidates["mechanism_family_assignments"].append(
                            {
                                "ingredient_id": ing_id,
                                "ingredient_name": simple_name,
                                "proposed_family": mechanism_hint,
                                "review_status": "needs_review",
                                "reason": "mechanism family hint is not an exact approved whitelist alias",
                            }
                        )
                else:
                    proposed_mid = _mechanism_id_from_name(simple_name, existing_mechanism_ids)
                    existing_mechanism_ids.add(proposed_mid)
                    self._add_review_row(
                        review_rows,
                        item_type="new_mechanism_family",
                        display_name=f"{simple_name} -> {proposed_mid}",
                        reason="new ingredient has no approved mechanism family",
                    )
                    review_candidates["new_mechanism_families"].append(
                        {
                            "ingredient_id": ing_id,
                            "ingredient_name": simple_name,
                            "proposed_mechanism_id": proposed_mid,
                            "proposed_mechanism_name": simple_name,
                            "review_status": "needs_review",
                            "reason": "new ingredient has no mechanism family assignment",
                        }
                    )

        self._collect_food_reviews(package, existing_foods, review_candidates, review_rows)
        self._collect_rule_reviews(package, review_candidates, review_rows)

        bottom = {
            "product_ingredient_mapping": bottom_product_rows,
            "simple_ingredient_updated": list(bottom_ingredient_by_name.values()),
            "mechanism_ingredient_map": bottom_mechanism_rows,
            "blocked_bottom_rows": blocked_bottom_rows,
        }
        coverage = self._coverage_audit(package, curated, bottom, review_candidates)
        return bottom, review_candidates, review_rows, coverage

    @staticmethod
    def _product_concept_defaults(mapping_rows: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
        defaults: dict[str, dict[str, str]] = {}
        for row in mapping_rows:
            concept_key = normalize_name(row.get("product_concept"))
            if not concept_key or concept_key in defaults:
                continue
            values = {
                "setting_type": clean_text(row.get("setting_type")),
                "special_time": clean_text(row.get("special_time")),
                "functionality": clean_text(row.get("Functionality")),
            }
            defaults[concept_key] = {k: v for k, v in values.items() if v}
        return defaults

    def _apply_bottom_layer(self, bottom: dict[str, Any], curated: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
        applied_counts = {
            "product_ingredient_mapping": self._append_rows(
                self.paths.product_ingredient_mapping,
                bottom["product_ingredient_mapping"],
                primary_keys=["canonical_product_id", "simple_ingredient_id"],
            ),
            "simple_ingredient_updated": self._append_rows(
                self.paths.simple_ingredients,
                bottom["simple_ingredient_updated"],
                primary_keys=["ingredient_id"],
            ),
            "mechanism_ingredient_map": self._append_rows(
                self.paths.mechanism_ingredient_map,
                bottom["mechanism_ingredient_map"],
                primary_keys=["ingredient_id", "mechanism_id"],
            ),
        }
        return {
            "mode": "bottom_layer_auto_applied",
            "applied_counts": applied_counts,
            "skipped_bottom_rows": bottom.get("blocked_bottom_rows", []),
        }

    def _append_rows(self, path: Path, rows: list[dict[str, Any]], primary_keys: list[str]) -> int:
        if not rows:
            return 0
        existing = read_rows(path)
        seen = {self._row_key(row, primary_keys) for row in existing}
        added = 0
        for row in rows:
            key = self._row_key(row, primary_keys)
            if key in seen:
                continue
            existing.append(row)
            seen.add(key)
            added += 1
        if added:
            dump_json(existing, path)
        return added

    @staticmethod
    def _row_key(row: dict[str, Any], keys: list[str]) -> tuple[str, ...]:
        return tuple(clean_text(row.get(key)) for key in keys)

    def _mechanism_alias_lookup(self) -> dict[str, dict[str, str]]:
        out: dict[str, dict[str, str]] = {}
        for item in self.config.mechanism_aliases:
            alias = normalize_name(item.get("alias"))
            mechanism_id = clean_text(item.get("mechanism_id"))
            mechanism_name = clean_text(item.get("mechanism_name"))
            if alias and mechanism_id and mechanism_name:
                out[alias] = {"mechanism_id": mechanism_id, "mechanism_name": mechanism_name}
        return out

    def _collect_food_reviews(
        self,
        package: dict[str, Any],
        existing_foods: dict[str, dict[str, Any]],
        review_candidates: dict[str, list[dict[str, Any]]],
        review_rows: list[dict[str, Any]],
    ) -> None:
        for item in package.get("food_items", []):
            name = clean_text(item.get("food_name") or item.get("name"))
            if name and normalize_name(name) not in existing_foods:
                self._add_review_row(review_rows, item_type="food_item", display_name=name, reason="new food item")
                review_candidates["food_items"].append(
                    {"food_name": name, "review_status": "needs_review", "reason": "new food item"}
                )
        for routine in package.get("food_routines", []):
            names = routine.get("map to food list") or routine.get("food_items") or []
            if isinstance(names, str):
                names = [part.strip() for part in names.split(",") if part.strip()]
            for name in names:
                if normalize_name(name) not in existing_foods:
                    self._add_review_row(
                        review_rows,
                        item_type="food_item",
                        display_name=str(name),
                        reason="food routine references unknown food",
                    )
                    review_candidates["food_items"].append(
                        {
                            "food_name": name,
                            "review_status": "needs_review",
                            "reason": "food routine references unknown food",
                        }
                    )
        for component in package.get("components", []):
            name = clean_text(component.get("component_name") or component.get("name"))
            self._add_review_row(review_rows, item_type="food_component", display_name=name, reason="new components are review-gated")
            review_candidates["components"].append(
                {
                    "component_name": name,
                    "review_status": "needs_review",
                    "reason": "new food components are review-gated; inherit existing components only",
                }
            )

    def _collect_rule_reviews(
        self,
        package: dict[str, Any],
        review_candidates: dict[str, list[dict[str, Any]]],
        review_rows: list[dict[str, Any]],
    ) -> None:
        for key in ("mechanism_rules", "extra_effect_rules", "food_component_ingredient_rules"):
            for row in package.get(key, []) or []:
                self._add_review_row(review_rows, item_type=key, display_name=clean_text(row.get("rule_id") or key), reason="all new rules are review-gated")
                review_candidates["new_rules"].append(
                    {
                        "rule_type": key,
                        "review_status": "needs_review",
                        "reason": "all new rules are review-gated",
                        "confidence": row.get("confidence") or row.get("Confidence") or row.get("evidence_confidence"),
                        "candidate": row,
                    }
                )

    @staticmethod
    def _add_review_row(review_rows: list[dict[str, Any]], *, item_type: str, display_name: str, reason: str) -> None:
        review_rows.append(
            {
                "item_type": item_type,
                "target_file": "review_only",
                "row_index": len(review_rows),
                "review_status": "needs_review",
                "reason": reason,
                "approval_status": "pending",
                "action": "manual review; do not auto-promote",
                "display_name": display_name,
            }
        )

    def _coverage_audit(
        self,
        package: dict[str, Any],
        curated: dict[str, list[dict[str, Any]]],
        bottom: dict[str, Any],
        review_candidates: dict[str, list[dict[str, Any]]],
    ) -> dict[str, Any]:
        existing_mech_ing = _existing_ids(curated["mechanism_ingredient_map"], "ingredient_id")
        bottom_mech_ing = _existing_ids(bottom["mechanism_ingredient_map"], "ingredient_id")
        bottom_ing_ids = _existing_ids(bottom["simple_ingredient_updated"], "ingredient_id")
        product_ing_ids = _existing_ids(bottom["product_ingredient_mapping"], "simple_ingredient_id")
        missing_mechanism = sorted((bottom_ing_ids | product_ing_ids) - existing_mech_ing - bottom_mech_ing)

        effect_covered = set()
        for row in curated["extra_effect_rules"]:
            a = clean_text(row.get("ingredient_A_id"))
            b = clean_text(row.get("ingredient_B_id"))
            if a:
                effect_covered.add(a)
            if b:
                effect_covered.add(b)

        return {
            "input_counts": {key: len(package.get(key, [])) for key in package.keys()},
            "bottom_layer_counts": {
                "product_ingredient_mapping": len(bottom["product_ingredient_mapping"]),
                "simple_ingredient_updated": len(bottom["simple_ingredient_updated"]),
                "mechanism_ingredient_map": len(bottom["mechanism_ingredient_map"]),
                "blocked_bottom_rows": len(bottom["blocked_bottom_rows"]),
            },
            "review_candidate_counts": {key: len(value) for key, value in review_candidates.items()},
            "ingredients_missing_mechanism_family": missing_mechanism,
            "ingredients_without_extra_effect_rule_coverage": sorted((bottom_ing_ids | product_ing_ids) - effect_covered),
        }

    def _render_audit_report(
        self,
        run_id: str,
        bottom: dict[str, Any],
        review_candidates: dict[str, list[dict[str, Any]]],
        coverage: dict[str, Any],
        daily_check: dict[str, Any],
        apply_report: dict[str, Any],
    ) -> str:
        lines = [
            "# Dataset Update Audit Report",
            "",
            f"- run_id: `{run_id}`",
            "- mode: bottom-layer auto-write; high-level rule review only",
            f"- bottom apply mode: `{apply_report['mode']}`",
            f"- daily compile check passed: **{daily_check['passed']}**",
            "",
            "## Bottom-Layer Rows",
        ]
        for key in ("product_ingredient_mapping", "simple_ingredient_updated", "mechanism_ingredient_map"):
            lines.append(f"- `{key}`: {len(bottom[key])} rows")
        lines.append(f"- blocked bottom rows: {len(bottom['blocked_bottom_rows'])}")
        lines += ["", "## Review Candidates"]
        for key, value in review_candidates.items():
            lines.append(f"- `{key}`: {len(value)}")
        lines += [
            "",
            "## Coverage",
            f"- ingredients missing mechanism family: {len(coverage['ingredients_missing_mechanism_family'])}",
            f"- ingredients without extra-effect coverage: {len(coverage['ingredients_without_extra_effect_rule_coverage'])}",
            "",
            "High-level rules are review-only and were not promoted into curated JSON.",
        ]
        return "\n".join(lines) + "\n"
