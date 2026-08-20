from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .normalization import clean_text, normalize_name
from .project_paths import DatasetPaths


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _contains_phrase(haystack: Any, needle: str) -> bool:
    hay = normalize_name(haystack)
    term = normalize_name(needle)
    if not hay or not term:
        return False
    return term == hay or term in hay


def _dedupe_terms(values: list[Any]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        term = clean_text(value)
        norm = normalize_name(term)
        if not norm or len(norm) < 3 or norm in seen:
            continue
        seen.add(norm)
        out.append(term)
    return out


def _load_json_if_exists(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def _candidate_db_files(root: Path, names: list[str]) -> list[Path]:
    return [root / name for name in names if (root / name).exists()]


class CandidateSourceSearcher:
    """Curated-first source recall for update packages.

    Search order is intentionally conservative:
    1. current Biohacker/curated product and ingredient rows;
    2. NDC candidate database for regulated/OTC drugs;
    3. DSLD candidate database for supplements.

    The search report is used to avoid creating new rows when an existing
    Biohacker product can already cover a synthetic experiment item.
    """

    def __init__(self, paths: DatasetPaths):
        self.paths = paths
        self.candidate_db_dir = paths.candidate_db_dir
        self._cui_metadata: dict[str, Any] | None = None
        self._ndc_map: dict[str, Any] | None = None

    def search_package(
        self,
        package: dict[str, Any],
        curated: dict[str, list[dict[str, Any]]],
    ) -> dict[str, Any]:
        items = []
        for index, product in enumerate(package.get("products", [])):
            item = self.search_product(product, curated, input_index=index)
            items.append(item)
        return {
            "search_order": [
                "biohacker_curated_product_and_ingredient",
                "ndc_candidate_database_for_drugs",
                "dsld_candidate_database_for_supplements",
            ],
            "policy": {
                "biohacker_curated_product": "use existing product/brand and do not draft a new product row unless force_new_product is true",
                "biohacker_curated_ingredient_only": "reuse ingredient id, but draft a product row if no existing product covers it",
                "ndc_or_dsld_candidate": "recall candidate only; curator reviews before promotion",
            },
            "items": items,
        }

    def search_product(
        self,
        product: dict[str, Any],
        curated: dict[str, list[dict[str, Any]]],
        *,
        input_index: int,
    ) -> dict[str, Any]:
        terms = self._terms_for_product(product)
        category = normalize_name(product.get("category") or product.get("product_type") or product.get("type"))
        force_new = self._truthy(product.get("force_new_product"))

        curated_matches = self._search_curated(terms, curated)
        selected_source = "none"
        recommendation = "draft_new_product_or_review"
        if curated_matches["product_matches"] and not force_new:
            selected_source = "biohacker_curated_product"
            recommendation = "use_existing_biohacker_product"
        elif curated_matches["ingredient_matches"]:
            selected_source = "biohacker_curated_ingredient_only"
            recommendation = "reuse_existing_ingredient_id"

        ndc_summary: dict[str, Any] | None = None
        dsld_summary: dict[str, Any] | None = None
        if selected_source == "none":
            if self._looks_like_drug(category, product):
                ndc_summary = self._search_ndc(terms)
                if ndc_summary["match_count"]:
                    selected_source = "ndc_candidate_database"
                    recommendation = "review_ndc_candidate"
            if selected_source == "none" and self._looks_like_supplement(category, product):
                dsld_summary = self._search_dsld(terms)
                if dsld_summary["match_count"]:
                    selected_source = "dsld_candidate_database"
                    recommendation = "review_dsld_candidate"

        return {
            "input_index": input_index,
            "product_brand": clean_text(product.get("product_brand")),
            "product_concept": clean_text(product.get("product_concept")),
            "category": clean_text(product.get("category") or product.get("product_type") or product.get("type")),
            "search_terms": terms,
            "force_new_product": force_new,
            "selected_source": selected_source,
            "recommendation": recommendation,
            "covered_by_existing_product": selected_source == "biohacker_curated_product",
            "curated": curated_matches,
            "ndc": ndc_summary,
            "dsld": dsld_summary,
        }

    def _terms_for_product(self, product: dict[str, Any]) -> list[str]:
        values: list[Any] = [
            product.get("product_concept"),
            product.get("product_brand"),
            product.get("main_ingredient"),
            product.get("main ingredient"),
            product.get("main_ingredients"),
            product.get("main ingredients"),
        ]
        for ingredient in product.get("ingredients") or []:
            if not isinstance(ingredient, dict):
                values.append(ingredient)
                continue
            values.extend(
                [
                    ingredient.get("name"),
                    ingredient.get("ingredient_name"),
                    ingredient.get("main_ingredient"),
                    ingredient.get("preferred_name"),
                    ingredient.get("definition"),
                ]
            )
        expanded: list[Any] = []
        for value in values:
            expanded.extend(_as_list(value))
        return _dedupe_terms(expanded)

    @staticmethod
    def _truthy(value: Any) -> bool:
        return clean_text(value).lower() in {"1", "true", "yes", "y", "force", "forced"}

    @staticmethod
    def _looks_like_drug(category: str, product: dict[str, Any]) -> bool:
        text = " ".join(
            [
                category,
                normalize_name(product.get("Notes")),
                normalize_name(product.get("notes")),
                normalize_name(product.get("Functionality")),
                normalize_name(product.get("functionality")),
            ]
        )
        return any(token in text for token in ("drug", "regulated", "prescription", "otc", "nsaid"))

    @staticmethod
    def _looks_like_supplement(category: str, product: dict[str, Any]) -> bool:
        if CandidateSourceSearcher._looks_like_drug(category, product):
            return False
        text = " ".join(
            [
                category,
                normalize_name(product.get("Notes")),
                normalize_name(product.get("notes")),
                normalize_name(product.get("Functionality")),
                normalize_name(product.get("functionality")),
            ]
        )
        if not text:
            return True
        return any(token in text for token in ("supplement", "botanical", "mineral", "vitamin", "sleep", "mood", "nootropic"))

    def _search_curated(
        self,
        terms: list[str],
        curated: dict[str, list[dict[str, Any]]],
    ) -> dict[str, Any]:
        ingredient_matches = []
        for row in curated["simple_ingredients"]:
            score = self._score_curated_ingredient(row, terms)
            if score:
                ingredient_matches.append(
                    {
                        "score": score,
                        **{
                            key: row.get(key)
                            for key in ("ingredient_id", "ingredient_name", "category/common_names", "supp.ai source id")
                        },
                    }
                )

        product_matches = []
        for row in curated["product_mapping"]:
            score = self._score_curated_product(row, terms)
            if score:
                product_matches.append(
                    {
                        "score": score,
                        **{
                            key: row.get(key)
                            for key in (
                                "canonical_product_id",
                                "product_brand",
                                "product_concept",
                                "recommender",
                                "expanded_ingredient_name_ofdraft",
                                "simple_ingredient_id",
                                "simple_ingredient_name",
                                "setting_type",
                                "Functionality",
                            )
                        },
                    }
                )

        ingredient_matches.sort(key=lambda row: (-row["score"], clean_text(row.get("ingredient_id"))))
        product_matches.sort(key=lambda row: (-row["score"], clean_text(row.get("canonical_product_id"))))
        return {
            "ingredient_match_count": len(ingredient_matches),
            "product_match_count": len(product_matches),
            "ingredient_matches": ingredient_matches[:10],
            "product_matches": self._dedupe_product_matches(product_matches)[:10],
        }

    @staticmethod
    def _score_curated_ingredient(row: dict[str, Any], terms: list[str]) -> int:
        name = row.get("ingredient_name")
        category = row.get("category/common_names")
        score = 0
        for term in terms:
            if normalize_name(name) == normalize_name(term):
                score = max(score, 100)
            elif _contains_phrase(name, term):
                score = max(score, 85)
            elif _contains_phrase(category, term):
                score = max(score, 45)
        return score

    @staticmethod
    def _score_curated_product(row: dict[str, Any], terms: list[str]) -> int:
        fields = {
            "simple_ingredient_name": 95,
            "expanded_ingredient_name_ofdraft": 90,
            "product_concept": 75,
            "product_brand": 55,
            "Functionality": 35,
        }
        score = 0
        for field, weight in fields.items():
            value = row.get(field)
            for term in terms:
                if normalize_name(value) == normalize_name(term):
                    score = max(score, weight + 5)
                elif _contains_phrase(value, term):
                    score = max(score, weight)
        return score

    @staticmethod
    def _dedupe_product_matches(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: set[tuple[str, str]] = set()
        out = []
        for row in rows:
            key = (clean_text(row.get("canonical_product_id")), clean_text(row.get("simple_ingredient_id")))
            if key in seen:
                continue
            seen.add(key)
            out.append(row)
        return out

    def _load_cui_metadata(self) -> dict[str, Any]:
        if self._cui_metadata is None:
            raw = _load_json_if_exists(self.paths.cui_metadata)
            self._cui_metadata = raw if isinstance(raw, dict) else {}
        return self._cui_metadata

    def _load_ndc_map(self) -> dict[str, Any]:
        if self._ndc_map is None:
            out: dict[str, Any] = {}
            for path in _candidate_db_files(self.candidate_db_dir, ["ndc-drug-map-1.json", "ndc-drug-map-2.json"]):
                raw = _load_json_if_exists(path)
                if isinstance(raw, dict):
                    out.update(raw)
            self._ndc_map = out
        return self._ndc_map

    def _search_ndc(self, terms: list[str]) -> dict[str, Any]:
        files = _candidate_db_files(
            self.candidate_db_dir,
            ["drug-ndc-slim-1.json", "drug-ndc-slim-2.json", "drug-ndc-slim-3.json"],
        )
        if not files:
            return {"match_count": 0, "reason": "ndc_files_not_found"}

        matches = []
        for path in files:
            raw = _load_json_if_exists(path)
            if not isinstance(raw, list):
                continue
            for row in raw:
                if not isinstance(row, dict):
                    continue
                score = self._score_ndc_row(row, terms)
                if score:
                    matches.append((score, row))

        matches.sort(key=lambda item: -item[0])
        ndc_map = self._load_ndc_map()
        valid_cuis = set(self._load_cui_metadata().keys())
        product_types: Counter[str] = Counter()
        pharm_classes: Counter[str] = Counter()
        active_ingredients: Counter[str] = Counter()
        candidate_cuis: Counter[tuple[str, str]] = Counter()
        validated_cuis: Counter[tuple[str, str]] = Counter()

        samples = []
        for score, row in matches:
            product_types[clean_text(row.get("product_type"))] += 1
            for value in row.get("pharm_class") or []:
                pharm_classes[clean_text(value)] += 1
            for ingredient in row.get("active_ingredients") or []:
                active_ingredients[clean_text(ingredient.get("name"))] += 1
            mapped = ndc_map.get(row.get("product_ndc")) or {}
            for item in mapped.get("cuis") or []:
                cui = clean_text(item.get("cui"))
                preferred = clean_text(item.get("preferred_name"))
                key = (cui, preferred)
                candidate_cuis[key] += 1
                if cui in valid_cuis:
                    validated_cuis[key] += 1
            if len(samples) < 8:
                samples.append(
                    {
                        "score": score,
                        **{
                            key: row.get(key)
                            for key in (
                                "product_ndc",
                                "generic_name",
                                "brand_name",
                                "product_type",
                                "pharm_class",
                                "active_ingredients",
                                "rxcui",
                                "unii",
                            )
                        },
                    }
                )

        return {
            "match_count": len(matches),
            "product_types": dict(product_types.most_common(8)),
            "top_active_ingredients": active_ingredients.most_common(8),
            "top_pharm_classes": pharm_classes.most_common(8),
            "top_candidate_cuis": [
                {"cui": cui, "preferred_name": preferred, "count": count}
                for (cui, preferred), count in candidate_cuis.most_common(8)
            ],
            "top_validated_cuis": [
                {"cui": cui, "preferred_name": preferred, "count": count}
                for (cui, preferred), count in validated_cuis.most_common(8)
            ],
            "samples": samples,
        }

    @staticmethod
    def _score_ndc_row(row: dict[str, Any], terms: list[str]) -> int:
        fields = [
            row.get("generic_name"),
            row.get("brand_name"),
            *[item.get("name") for item in row.get("active_ingredients") or []],
        ]
        score = 0
        for field in fields:
            for term in terms:
                if normalize_name(field) == normalize_name(term):
                    score = max(score, 100)
                elif _contains_phrase(field, term):
                    score = max(score, 70)
        return score

    def _search_dsld(self, terms: list[str]) -> dict[str, Any]:
        files = _candidate_db_files(self.candidate_db_dir, ["dsld-1.jsonl", "dsld-2.jsonl"])
        if not files:
            return {"match_count": 0, "reason": "dsld_files_not_found"}

        count = 0
        brands: Counter[str] = Counter()
        ingredients: Counter[str] = Counter()
        samples = []
        for path in files:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    row = json.loads(line)
                    score = self._score_dsld_row(row, terms)
                    if not score:
                        continue
                    count += 1
                    brands[clean_text(row.get("brand_name"))] += 1
                    for ingredient in row.get("ingredients") or []:
                        ingredients[clean_text(ingredient.get("preferred_name"))] += 1
                    if len(samples) < 8:
                        samples.append(
                            {
                                "score": score,
                                "dsld_label_id": row.get("dsld_label_id"),
                                "supplement_name": row.get("supplement_name"),
                                "brand_name": row.get("brand_name"),
                                "ingredients": (row.get("ingredients") or [])[:8],
                            }
                        )

        return {
            "match_count": count,
            "top_brands": brands.most_common(8),
            "top_ingredients": ingredients.most_common(8),
            "samples": samples,
        }

    @staticmethod
    def _score_dsld_row(row: dict[str, Any], terms: list[str]) -> int:
        fields = [
            row.get("supplement_name"),
            row.get("brand_name"),
            *[item.get("preferred_name") for item in row.get("ingredients") or []],
        ]
        score = 0
        for field in fields:
            for term in terms:
                if normalize_name(field) == normalize_name(term):
                    score = max(score, 100)
                elif _contains_phrase(field, term):
                    score = max(score, 65)
        return score


def covered_input_indexes(search_report: dict[str, Any]) -> set[int]:
    out: set[int] = set()
    for item in search_report.get("items", []):
        if item.get("covered_by_existing_product"):
            out.add(int(item["input_index"]))
    return out
