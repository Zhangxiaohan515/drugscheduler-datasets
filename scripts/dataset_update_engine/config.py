from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CONFIG_DIR = Path(__file__).resolve().parent / "config"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


@dataclass(frozen=True)
class EngineConfig:
    category_to_setting_type: dict[str, str]
    category_defaults: dict[str, dict[str, Any]]
    mechanism_aliases: list[dict[str, str]]
    compile_checks: dict[str, dict[str, Any]]
    suppai_matching_policy: dict[str, str]

    @classmethod
    def load(cls, config_dir: Path = CONFIG_DIR) -> "EngineConfig":
        mech = load_json(config_dir / "mechanism_auto_map_allowlist.json")
        return cls(
            category_to_setting_type={
                str(k).strip().lower(): str(v).strip()
                for k, v in load_json(config_dir / "product_category_setting_map.json").items()
            },
            category_defaults={
                str(k).strip().lower(): v
                for k, v in load_json(config_dir / "product_category_timing_defaults.json").items()
                if isinstance(v, dict)
            },
            mechanism_aliases=list(mech.get("aliases", [])),
            compile_checks=load_json(config_dir / "enabled_compile_checks.json"),
            suppai_matching_policy=load_json(config_dir / "suppai_matching_policy.json"),
        )
