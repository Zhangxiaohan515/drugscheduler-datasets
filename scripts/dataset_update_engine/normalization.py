from __future__ import annotations

import re
import unicodedata
from typing import Any


_SPACE_RE = re.compile(r"\s+")
_NON_WORD_RE = re.compile(r"[^a-z0-9]+")


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_name(value: Any) -> str:
    text = unicodedata.normalize("NFKD", clean_text(value))
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = _NON_WORD_RE.sub(" ", text)
    return _SPACE_RE.sub(" ", text).strip()


def is_yes(value: Any) -> bool:
    return clean_text(value).lower() in {"1", "true", "yes", "y", "approved", "approve"}


def unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out
