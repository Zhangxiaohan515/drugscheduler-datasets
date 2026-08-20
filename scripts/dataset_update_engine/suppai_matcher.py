from __future__ import annotations

from pathlib import Path
from typing import Any

from .json_io import load_json
from .normalization import normalize_name


def _token_set(value: str) -> set[str]:
    return {token for token in normalize_name(value).split() if len(token) > 2}


class SuppAiMatcher:
    def __init__(self, cui_metadata_path: Path):
        self.records: dict[str, dict[str, Any]] = {}
        self.preferred_index: dict[str, list[str]] = {}
        self.alias_index: dict[str, list[str]] = {}
        if cui_metadata_path.exists():
            raw = load_json(cui_metadata_path)
            if isinstance(raw, dict):
                self.records = {str(k): v for k, v in raw.items() if isinstance(v, dict)}
        for cui, rec in self.records.items():
            preferred = normalize_name(rec.get("preferred_name"))
            if preferred:
                self.preferred_index.setdefault(preferred, []).append(cui)
            for key in ("synonyms", "tradenames"):
                values = rec.get(key) or []
                if isinstance(values, list):
                    for value in values:
                        alias = normalize_name(value)
                        if alias:
                            self.alias_index.setdefault(alias, []).append(cui)

    def match(self, ingredient_name: str, definition_hint: str | None = None) -> dict[str, Any]:
        norm = normalize_name(ingredient_name)
        preferred_hits = self.preferred_index.get(norm, [])
        if len(preferred_hits) == 1:
            cui = preferred_hits[0]
            if definition_hint:
                hint_tokens = _token_set(definition_hint)
                definition_tokens = _token_set(str(self.records[cui].get("definition") or ""))
                if hint_tokens and definition_tokens and not (hint_tokens & definition_tokens):
                    return {
                        "status": "needs_review_definition_mismatch",
                        "candidates": [cui],
                    }
            return {
                "status": "exact_preferred_match",
                "cui": cui,
                "record": self.records[cui],
            }
        if len(preferred_hits) > 1:
            return {"status": "ambiguous_preferred_match", "candidates": preferred_hits}

        alias_hits = self.alias_index.get(norm, [])
        if alias_hits:
            return {"status": "needs_review_alias_match", "candidates": sorted(set(alias_hits))}

        return {"status": "no_match"}
