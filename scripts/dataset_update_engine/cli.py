from __future__ import annotations

import argparse
from pathlib import Path

from .curated_sync import ExperimentSyncer
from .github_flow import git_status_summary, publish_update_run
from .legacy_apply import ApprovedApplier
from .project_paths import default_paths
from .update_pipeline import UpdateEngine


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dataset-update-engine")
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan-update", help="Dry-run update: inspect bottom-layer rows and review outputs without editing curated JSON")
    plan.add_argument("--input", required=True, type=Path)
    plan.add_argument("--out", type=Path, default=None)
    plan.add_argument("--run-id", default=None)

    auto = sub.add_parser("auto-update", help="Apply deterministic bottom-layer mappings locally and export high-level review outputs")
    auto.add_argument("--input", required=True, type=Path)
    auto.add_argument("--out", type=Path, default=None)
    auto.add_argument("--run-id", default=None)

    apply = sub.add_parser("apply-approved", help="Apply approved rows from a review run")
    apply.add_argument("--run-dir", required=True, type=Path)

    status = sub.add_parser("git-status", help="Check whether Git publishing is currently available")
    status.add_argument("--cwd", type=Path, default=None)

    publish = sub.add_parser("publish-update", help="Create branch, commit, push, and open a PR in Github/drugscheduler-datasets")
    publish.add_argument("--run-dir", required=True, type=Path)
    publish.add_argument("--branch", default=None)
    publish.add_argument("--title", default=None)
    publish.add_argument("--draft", action="store_true")

    sync = sub.add_parser("sync-approved-to-experiment", help="Append approved GitHub update-run bottom-layer rows to Biohacker_dataset")
    sync.add_argument("--run-dir", required=True, type=Path)

    args = parser.parse_args(argv)

    if args.command == "plan-update":
        out_dir = UpdateEngine().plan_update(args.input, out_dir=args.out, run_id=args.run_id)
        print(f"[ok] dry-run review bundle written to {out_dir}")
        return 0

    if args.command == "auto-update":
        out_dir = UpdateEngine().auto_update(args.input, out_dir=args.out, run_id=args.run_id)
        print(f"[ok] bottom-layer update applied; review bundle written to {out_dir}")
        return 0

    if args.command == "apply-approved":
        report = ApprovedApplier().apply_run(args.run_dir)
        print(f"[ok] apply report written to {report}")
        return 0

    if args.command == "git-status":
        cwd = args.cwd or default_paths().dataset_repo_root
        result = git_status_summary(cwd)
        print(result)
        return 0 if result["status"] == "ok" else 1

    if args.command == "publish-update":
        paths = default_paths()
        result = publish_update_run(
            repo_root=paths.dataset_repo_root,
            run_dir=args.run_dir,
            branch=args.branch,
            title=args.title,
            draft=args.draft,
        )
        print(result)
        return 0 if result["status"] == "ok" else 1

    if args.command == "sync-approved-to-experiment":
        report = ExperimentSyncer().sync_run_to_experiment(args.run_dir)
        print(f"[ok] synced approved run to experiment dataset: {report}")
        return 0

    parser.error(f"Unknown command {args.command}")
    return 2
