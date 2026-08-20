from __future__ import annotations

import re


def next_prefixed_id(existing_ids: set[str], prefix: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}-(\d+)$", re.IGNORECASE)
    max_seen = 0
    width = 3
    for value in existing_ids:
        m = pattern.match(str(value).strip())
        if not m:
            continue
        raw = m.group(1)
        max_seen = max(max_seen, int(raw))
        width = max(width, len(raw))
    return f"{prefix}-{max_seen + 1:0{width}d}"


def reserve_next(existing_ids: set[str], prefix: str) -> str:
    new_id = next_prefixed_id(existing_ids, prefix)
    existing_ids.add(new_id)
    return new_id
