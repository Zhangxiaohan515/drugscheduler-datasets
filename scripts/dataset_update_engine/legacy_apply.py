from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any

from .json_io import dump_json, load_json, read_rows
from .normalization import clean_text, is_yes
from .project_paths import DatasetPaths, default_paths
from .review_exporter import read_review_table
from .update_validator import validate_ingredient_row, validate_product_row


TARGETS = {
    "product_ingredient_mapping.json": "product_ingredient_mapping",
    "simple_ingredient_updated.json": "simple_ingredient_updated",
    "mechanism_ingredient_map.json": "mechanism_ingredient_map",
}


class ApprovedApplier:
    def __init__(self, paths: DatasetPaths | None = None):
        self.paths = paths or default_paths()

    def apply_run(self, run_dir: Path) -> Path:
        draft = load_json(run_dir / "draft_auto_additions.json")
        review_rows = read_review_table(run_dir / "review_table.csv")
        existing_ingredient_ids = {
            clean_text(row.get("ingredient_id"))
            for row in read_rows(self.paths.simple_ingredients)
            if clean_text(row.get("ingredient_id"))
        }
        draft_ingredient_ids = {
            clean_text(row.get("ingredient_id"))
            for row in draft.get("simple_ingredient_updated", [])
            if clean_text(row.get("ingredient_id"))
        }
        known_ingredient_ids = existing_ingredient_ids | draft_ingredient_ids

        applied: list[dict[str, Any]] = []
        skipped: list[dict[str, Any]] = []
        to_append: dict[str, list[dict[str, Any]]] = {key: [] for key in TARGETS}

        for review in review_rows:
            if not is_yes(review.get("approval_status")):
                skipped.append({**review, "skip_reason": "not approved"})
                continue
            target_file = clean_text(review.get("target_file"))
            draft_key = TARGETS.get(target_file)
            if not draft_key:
                skipped.append({**review, "skip_reason": "target is not apply-supported"})
                continue
            try:
                row_index = int(clean_text(review.get("row_index")))
                row = draft[draft_key][row_index]
            except Exception:
                skipped.append({**review, "skip_reason": "cannot locate draft row"})
                continue

            errors = self._validate_row(target_file, row, known_ingredient_ids)
            if errors:
                skipped.append({**review, "skip_reason": "; ".join(errors)})
                continue
            to_append[target_file].append(row)
            applied.append({**review, "applied_row": row})

        self._append_rows(self.paths.product_ingredient_mapping, to_append["product_ingredient_mapping.json"], "canonical_product_id")
        self._append_rows(self.paths.simple_ingredients, to_append["simple_ingredient_updated.json"], "ingredient_id")
        self._append_rows(self.paths.mechanism_ingredient_map, to_append["mechanism_ingredient_map.json"], "ingredient_id", secondary_key="mechanism_id")

        report = {
            "applied_at": dt.datetime.now().isoformat(timespec="seconds"),
            "run_dir": str(run_dir),
            "applied_count": len(applied),
            "skipped_count": len(skipped),
            "applied": applied,
            "skipped": skipped,
        }
        out_path = run_dir / "apply_report.json"
        dump_json(report, out_path)
        return out_path

    def _validate_row(self, target_file: str, row: dict[str, Any], known_ingredient_ids: set[str]) -> list[str]:
        if target_file == "product_ingredient_mapping.json":
            return validate_product_row(row, known_ingredient_ids)
        if target_file == "simple_ingredient_updated.json":
            return validate_ingredient_row(row)
        if target_file == "mechanism_ingredient_map.json":
            required = ["mechanism_id", "mechanism_name", "ingredient_id", "ingredient_name"]
            return [f"missing {field}" for field in required if not clean_text(row.get(field))]
        return [f"unsupported target {target_file}"]

    def _append_rows(self, path: Path, rows: list[dict[str, Any]], primary_key: str, secondary_key: str | None = None) -> None:
        if not rows:
            return
        existing = read_rows(path)
        seen = set()
        for row in existing:
            key = clean_text(row.get(primary_key))
            if secondary_key:
                key = f"{key}::{clean_text(row.get(secondary_key))}"
            seen.add(key)

        appended = False
        for row in rows:
            key = clean_text(row.get(primary_key))
            if secondary_key:
                key = f"{key}::{clean_text(row.get(secondary_key))}"
            if key in seen:
                continue
            existing.append(row)
            seen.add(key)
            appended = True
        if appended:
            dump_json(existing, path)
