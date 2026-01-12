from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .config_schemas import load_config
from .state import ThreadState, BundleState
from . import kernels
from . import metrics as metrics_mod


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def run_ensemble_for_pair(rng: np.random.Generator,
                          cfg,
                          W_coh: float,
                          N: int):
    """
    Run all ensembles for a single (W_coh, N) pair and compute lockstep metrics.
    """
    steps = int(cfg.grid.steps)
    burn_in = int(cfg.grid.burn_in)
    n_ensembles = int(cfg.grid.ensembles)
    T_eff = steps - burn_in
    if T_eff <= 0:
        raise ValueError("burn_in must be < steps")

    m_all = np.zeros((n_ensembles, T_eff), dtype=float)
    dX_all = np.zeros((n_ensembles, T_eff), dtype=float)

    # Hop-coherence base slip probability for this W_coh
    alpha = float(cfg.hop_coherence.alpha)
    k_pref = float(cfg.hop_coherence.k_prefactor)
    form = cfg.hop_coherence.form
    if form == "power_law":
        q_base = min(0.5, k_pref / (float(W_coh) ** alpha))
    elif form == "exp":
        q_base = min(0.5, k_pref * np.exp(-float(W_coh)))
    else:
        q_base = min(0.5, k_pref / max(float(W_coh), 1.0))
    cfg.hop_coherence.q_base = q_base

    # Domains
    n_domains = int(getattr(cfg.domains, "n_initial_domains", 1))
    if n_domains < 1:
        n_domains = 1

    for e in range(n_ensembles):
        v0 = rng.choice([-1.0, 1.0], size=N)
        theta0 = rng.uniform(0.0, 2.0 * np.pi, size=N)
        domain0 = rng.integers(0, n_domains, size=N, endpoint=False)

        threads = ThreadState(v=v0, theta=theta0, domain=domain0, history_v=None)
        kernels.initialise_cadence(rng, threads, cfg.cadence)

        X = 0.0
        m = float(np.mean(threads.v))
        theta_mean = float(np.angle(np.mean(np.exp(1j * threads.theta))))
        bundle = BundleState(X=X, m=m, theta_mean=theta_mean)

        t_eff = 0
        for t in range(steps):
            # Cadence update and active mask
            kernels.cadence_step(rng, threads, cfg.cadence)
            # Hop coherence
            kernels.hop_coherence_step(rng, threads, cfg.hop_coherence)

            # Update bundle before further glue
            bundle.m = float(np.mean(threads.v))
            bundle.theta_mean = float(np.angle(np.mean(np.exp(1j * threads.theta))))

            # Shared bias
            kernels.shared_bias_step(rng, threads, bundle, cfg.shared_bias)

            # Phase locking
            kernels.phase_lock_step(rng, threads, bundle, cfg.phase_lock)

            # Domains
            kernels.domain_glue_step(rng, threads, cfg.domains)

            # Update aggregates and COM increment
            bundle.m = float(np.mean(threads.v))
            bundle.theta_mean = float(np.angle(np.mean(np.exp(1j * threads.theta))))
            dX = float(np.mean(threads.v))
            bundle.X += dX

            if t >= burn_in:
                m_all[e, t_eff] = bundle.m
                dX_all[e, t_eff] = dX
                t_eff += 1

        assert t_eff == T_eff

    metrics = metrics_mod.compute_lockstep_metrics(m_all, dX_all)
    return metrics, m_all, dX_all


def run_all(config_path: str | Path) -> None:
    """
    Top-level driver for a full run over the (W_coh, N) grid.
    """
    cfg = load_config(config_path)
    output_root = Path(cfg.output_dir)
    _ensure_dir(output_root)

    # JSON-serialisable metadata snapshot
    metadata = {
        "random_seed": cfg.random_seed,
        "grid": vars(cfg.grid),
        "hop_coherence": vars(cfg.hop_coherence),
        "shared_bias": vars(cfg.shared_bias),
        "phase_lock": vars(cfg.phase_lock),
        "domains": vars(cfg.domains),
        "diagnostics": vars(cfg.diagnostics),
    }
    with (output_root / "metadata.json").open("w", encoding="utf-8") as fh:
        json.dump(metadata, fh, indent=2)

    rng = np.random.default_rng(cfg.random_seed)

    summary_rows = []

    for W_coh in cfg.grid.W_coh_values:
        for N in cfg.grid.N_values:
            pair_dir = output_root / f"W{W_coh}_N{N}"
            _ensure_dir(pair_dir)

            metrics, m_all, dX_all = run_ensemble_for_pair(rng, cfg, W_coh=W_coh, N=N)

            pair_summary = {
                "W_coh": W_coh,
                "N": N,
                **metrics,
            }
            with (pair_dir / "summary_lockstep.json").open("w", encoding="utf-8") as fh:
                json.dump(pair_summary, fh, indent=2)

            if cfg.diagnostics.store_states:
                np.savez_compressed(
                    pair_dir / "timeseries.npz",
                    m_all=m_all,
                    dX_all=dX_all,
                )

            summary_rows.append(pair_summary)

    with (output_root / "summary.json").open("w", encoding="utf-8") as fh:
        json.dump(summary_rows, fh, indent=2)