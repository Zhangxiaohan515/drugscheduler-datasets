from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


FIELDS = [
    "item_type",
    "target_file",
    "row_index",
    "review_status",
    "reason",
    "approval_status",
    "action",
    "display_name",
]


def write_review_table(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def write_review_workbook(rows: list[dict[str, Any]], path: Path) -> bool:
    """Write an Excel review table when openpyxl is available."""
    try:
        import openpyxl  # type: ignore
    except ImportError:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "review_table"
    sheet.append(FIELDS)
    for row in rows:
        sheet.append([row.get(field, "") for field in FIELDS])
    for col in sheet.columns:
        width = max(len(str(cell.value or "")) for cell in col)
        sheet.column_dimensions[col[0].column_letter].width = min(max(width + 2, 12), 60)
    workbook.save(path)
    return True


def read_review_table(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]
