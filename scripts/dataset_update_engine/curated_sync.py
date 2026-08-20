from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any

from .json_io import dump_json, load_json, read_rows
from .normalization import clean_text
from .project_paths import DatasetPaths, default_paths


SYNC_TARGETS = {
    "product_ingredient_mapping": ("product_ingredient_mapping.json", ["canonical_product_id", "simple_ingredient_id"]),
    "simple_ingredient_updated": ("simple_ingredient_updated.json", ["ingredient_id"]),
    "mechanism_ingredient_map": ("mechanism_ingredient_map.json", ["ingredient_id", "mechanism_id"]),
}


class ExperimentSyncer:
    def __init__(self, paths: DatasetPaths | None = None):
        self.paths = paths or default_paths()

    def sync_run_to_experiment(self, run_dir: Path) -> Path:
        if self.paths.experiment_curated_dir is None:
            raise RuntimeError("No experiment_curated_dir configured")

        bottom_path = run_dir / "bottom_layer_auto_applied.json"
        if not bottom_path.exists():
            raise FileNotFoundError(f"Expected auto-update output at {bottom_path}")
        bottom = load_json(bottom_path)

        copied: dict[str, int] = {}
        for key, (filename, id_fields) in SYNC_TARGETS.items():
            source_rows = bottom.get(key, [])
            target_path = self.paths.experiment_curated_dir / filename
            copied[key] = self._append_rows(target_path, source_rows, id_fields)

        report = {
            "synced_at": dt.datetime.now().isoformat(timespec="seconds"),
            "source_run_dir": str(run_dir),
            "experiment_curated_dir": str(self.paths.experiment_curated_dir),
            "synced_counts": copied,
        }
        out_path = run_dir / "sync_to_experiment_report.json"
        dump_json(report, out_path)
        return out_path

    @staticmethod
    def _append_rows(path: Path, rows: list[dict[str, Any]], id_fields: list[str]) -> int:
        if not rows:
            return 0
        existing = read_rows(path)
        seen = {tuple(clean_text(row.get(field)) for field in id_fields) for row in existing}
        added = 0
        for row in rows:
            key = tuple(clean_text(row.get(field)) for field in id_fields)
            if key in seen:
                continue
            existing.append(row)
            seen.add(key)
            added += 1
        if added:
            dump_json(existing, path)
        return added
