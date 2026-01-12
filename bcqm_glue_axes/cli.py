from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from . import simulate
from . import metrics as metrics_mod


def _analyse_lockstep(output_root: Path) -> None:
    output_root = output_root.expanduser().resolve()
    if not output_root.is_dir():
        raise SystemExit(f"Output directory not found: {output_root}")
    for pair_dir in sorted(output_root.iterdir()):
        if not pair_dir.is_dir():
            continue
        ts_path = pair_dir / "timeseries.npz"
        if not ts_path.exists():
            continue
        data = np.load(ts_path)
        m_all = data["m_all"]
        dX_all = data["dX_all"]
        metrics = metrics_mod.compute_lockstep_metrics(m_all, dX_all)
        pair_summary_path = pair_dir / "summary_lockstep.json"
        if pair_summary_path.exists():
            with pair_summary_path.open("r", encoding="utf-8") as fh:
                pair_summary = json.load(fh)
        else:
            pair_summary = {}
        pair_summary.update(metrics)
        with pair_summary_path.open("w", encoding="utf-8") as fh:
            json.dump(pair_summary, fh, indent=2)
        print(f"Updated lockstep metrics in {pair_summary_path}")


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="bcqm_glue_axes CLI (BCQM V glue-axes laboratory)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    p_run = subparsers.add_parser("run", help="run a glue-axes simulation")
    p_run.add_argument("config", type=str, help="YAML configuration file")
    p_an = subparsers.add_parser(
        "analyse-lockstep",
        help="recompute lockstep metrics from stored timeseries",
    )
    p_an.add_argument("output_dir", type=str, help="output directory for a run")
    args = parser.parse_args(argv)
    if args.command == "run":
        simulate.run_all(args.config)
    elif args.command == "analyse-lockstep":
        _analyse_lockstep(Path(args.output_dir))
    else:
        parser.error(f"Unknown command: {args.command!r}")


if __name__ == "__main__":
    main()
