from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def find_project_root(start: Path | None = None) -> Path:
    """Find the nearest project root containing `.project_root`."""
    cur = (start or Path(__file__)).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".project_root").exists():
            return candidate
    raise FileNotFoundError(f"Could not locate .project_root above {cur}")


@dataclass(frozen=True)
class DatasetPaths:
    project_root: Path
    dataset_repo_root: Path
    curated_dir: Path
    candidate_db_dir: Path
    specs_dir: Path
    review_runs_dir: Path
    experiment_curated_dir: Path | None = None

    @property
    def simple_ingredients(self) -> Path:
        return self.curated_dir / "simple_ingredient_updated.json"

    @property
    def product_ingredient_mapping(self) -> Path:
        return self.curated_dir / "product_ingredient_mapping.json"

    @property
    def mechanism_ingredient_map(self) -> Path:
        return self.curated_dir / "mechanism_ingredient_map.json"

    @property
    def mechanism_rules(self) -> Path:
        return self.curated_dir / "mechanism_rules.json"

    @property
    def extra_effect_rules(self) -> Path:
        return self.curated_dir / "extra_effect_rules.json"

    @property
    def food_component_dataset(self) -> Path:
        return self.curated_dir / "food_component_dataset.json"

    @property
    def food_component_ingredient_rules(self) -> Path:
        return self.curated_dir / "food_component_ingredient_rules.json"

    @property
    def food_routine(self) -> Path:
        return self.curated_dir / "food_routine.json"

    @property
    def cui_metadata(self) -> Path:
        direct = self.candidate_db_dir / "cui_metadata.json"
        if direct.exists():
            return direct
        return self.candidate_db_dir / "original_data" / "cui_metadata.json"


def default_paths(project_root: Path | None = None) -> DatasetPaths:
    root = project_root or find_project_root()
    if not (root / "Github" / "drugscheduler-datasets").exists():
        for candidate in root.parents:
            if (candidate / "Github" / "drugscheduler-datasets").exists():
                root = candidate
                break
    scenario_files = root / "data" / "drug_lists" / "Real world experiment" / "scenario_files"
    dataset_repo = root / "Github" / "drugscheduler-datasets"
    if dataset_repo.exists():
        return DatasetPaths(
            project_root=root,
            dataset_repo_root=dataset_repo,
            curated_dir=dataset_repo / "curated",
            candidate_db_dir=dataset_repo / "candidate database",
            specs_dir=dataset_repo / "specs",
            review_runs_dir=dataset_repo / "update_runs",
            experiment_curated_dir=scenario_files / "Biohacker_dataset",
        )
    return DatasetPaths(
        project_root=root,
        dataset_repo_root=root,
        curated_dir=scenario_files / "Biohacker_dataset",
        candidate_db_dir=root / "data" / "json_db" / "interaction-data-sample",
        specs_dir=root / "specs",
        review_runs_dir=root / "dataset_update_runs",
        experiment_curated_dir=scenario_files / "Biohacker_dataset",
    )
