from __future__ import annotations

import json
from pathlib import Path


ROOT = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "drug_lists"
    / "Real world experiment"
    / "scenario_files"
    / "Biohacker_dataset"
)

TIME_INTERVAL_FIELD = "time interval"

MECHANISM_TIME_INTERVAL_EXCEPTIONS = {
    "MEC-008": 3,
    "MEC-150": 2,
    "MEC-212": 2,
    "MEC-123": "delta H",
    "MEC-126": "delta H",
    "MEC-131": "delta H",
    "MEC-132": "delta H",
}


def load_json(name: str) -> list[dict]:
    with (ROOT / name).open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def dump_json(name: str, rows: list[dict]) -> None:
    with (ROOT / name).open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        f.write("\n")


def apply_mechanism_intervals(rows: list[dict]) -> dict[str, int]:
    stats = {"default": 0, "specific_hour": 0, "delta_h": 0, "changed": 0}
    seen_exceptions: set[str] = set()

    for row in rows:
        rule_id = row.get("rule_id")
        interval = MECHANISM_TIME_INTERVAL_EXCEPTIONS.get(rule_id, "default")

        if row.get(TIME_INTERVAL_FIELD) != interval:
            row[TIME_INTERVAL_FIELD] = interval
            stats["changed"] += 1

        if interval == "default":
            stats["default"] += 1
        elif interval == "delta H":
            stats["delta_h"] += 1
            seen_exceptions.add(rule_id)
        else:
            stats["specific_hour"] += 1
            seen_exceptions.add(rule_id)

    missing = sorted(set(MECHANISM_TIME_INTERVAL_EXCEPTIONS) - seen_exceptions)
    if missing:
        raise SystemExit(f"Missing mechanism rule IDs for time interval exceptions: {missing}")

    return stats


def apply_extra_effect_intervals(rows: list[dict]) -> dict[str, int]:
    stats = {"default": 0, "changed": 0}
    for row in rows:
        if row.get(TIME_INTERVAL_FIELD) != "default":
            row[TIME_INTERVAL_FIELD] = "default"
            stats["changed"] += 1
        stats["default"] += 1
    return stats


def main() -> None:
    mechanism_rules = load_json("mechanism_rules.json")
    extra_effect_rules = load_json("extra_effect_rules.json")

    mechanism_stats = apply_mechanism_intervals(mechanism_rules)
    extra_effect_stats = apply_extra_effect_intervals(extra_effect_rules)

    dump_json("mechanism_rules.json", mechanism_rules)
    dump_json("extra_effect_rules.json", extra_effect_rules)

    print(
        json.dumps(
            {
                "updated": {
                    "mechanism_rules": mechanism_stats["changed"],
                    "extra_effect_rules": extra_effect_stats["changed"],
                },
                "mechanism_time_interval_distribution": {
                    "default": mechanism_stats["default"],
                    "specific_hour": mechanism_stats["specific_hour"],
                    "delta H": mechanism_stats["delta_h"],
                },
                "extra_effect_time_interval_distribution": {
                    "default": extra_effect_stats["default"],
                },
                "mechanism_exceptions": MECHANISM_TIME_INTERVAL_EXCEPTIONS,
                "totals": {
                    "mechanism_rules": len(mechanism_rules),
                    "extra_effect_rules": len(extra_effect_rules),
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
