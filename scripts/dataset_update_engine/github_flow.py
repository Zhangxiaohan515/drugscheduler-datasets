from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any


def _run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def git_status_summary(cwd: Path) -> dict[str, str]:
    result = _run(["git", "status", "--short"], cwd)
    if "dubious ownership" in result.stderr.lower():
        return {
            "status": "blocked",
            "reason": "git safe.directory ownership check failed; approve git config setup before publishing",
            "stderr": result.stderr,
        }
    return {
        "status": "ok" if result.returncode == 0 else "error",
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def _ensure_ok(result: subprocess.CompletedProcess[str], step: str) -> None:
    if result.returncode != 0:
        raise RuntimeError(f"{step} failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")


def branch_name_from_run(run_dir: Path) -> str:
    raw = re.sub(r"[^A-Za-z0-9._-]+", "-", run_dir.name).strip("-")
    return f"codex/dataset-update-{raw or 'run'}"


def find_gh_executable() -> str:
    found = shutil.which("gh")
    if found:
        return found
    common = Path(r"C:\Program Files\GitHub CLI\gh.exe")
    if common.exists():
        return str(common)
    return "gh"


def publish_update_run(
    *,
    repo_root: Path,
    run_dir: Path,
    branch: str | None = None,
    title: str | None = None,
    draft: bool = False,
) -> dict[str, Any]:
    """Create a branch, commit approved update artifacts, push, and open a PR.

    This function intentionally uses direct subprocess argv calls rather than
    shell composition. It should be run only after `apply-approved`.
    """
    status = git_status_summary(repo_root)
    if status["status"] == "blocked":
        return status

    branch = branch or branch_name_from_run(run_dir)
    title = title or f"Dataset update {run_dir.name}"
    body_file = run_dir / "audit_report.md"
    if not body_file.exists():
        body_file = run_dir / "apply_report.json"

    steps: list[dict[str, str]] = []

    commands = [
        ("create_branch", ["git", "checkout", "-b", branch]),
        ("stage_curated", ["git", "add", "curated"]),
        ("stage_candidate_database", ["git", "add", "candidate database"]),
        ("stage_specs", ["git", "add", "specs"]),
        ("stage_update_runs", ["git", "add", "update_runs"]),
        ("commit", ["git", "commit", "-m", title]),
        ("push", ["git", "push", "-u", "origin", branch]),
    ]
    for step, command in commands:
        result = _run(command, repo_root)
        steps.append({"step": step, "stdout": result.stdout, "stderr": result.stderr})
        _ensure_ok(result, step)

    pr_command = [find_gh_executable(), "pr", "create", "--title", title, "--body-file", str(body_file)]
    if draft:
        pr_command.append("--draft")
    pr = _run(pr_command, repo_root)
    steps.append({"step": "create_pr", "stdout": pr.stdout, "stderr": pr.stderr})
    _ensure_ok(pr, "create_pr")

    summary = {
        "status": "ok",
        "branch": branch,
        "pr_url": pr.stdout.strip(),
        "steps": steps,
    }
    (run_dir / "publish_report.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary
