from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict

import yaml


@dataclass
class GridConfig:
    W_coh_values: list
    N_values: list
    ensembles: int
    steps: int
    burn_in: int


@dataclass
class HopCoherenceConfig:
    form: str = "power_law"
    alpha: float = 1.0
    k_prefactor: float = 2.0
    memory_depth: int = 1


@dataclass
class SharedBiasConfig:
    enabled: bool = False
    lambda_bias: float = 0.0


@dataclass
class PhaseLockConfig:
    enabled: bool = False
    lambda_phase: float = 0.0
    theta_join: float = 0.3
    theta_break: float = 1.5
    omega_0: float = 0.1
    noise_sigma: float = 0.0


@dataclass
class DomainsConfig:
    enabled: bool = False
    n_initial_domains: int = 1
    lambda_domain: float = 0.0
    merge_threshold: float = 0.8
    split_threshold: float = 0.3
    min_domain_size: int = 1


@dataclass
class CadenceConfig:
    enabled: bool = False
    distribution: str = "lognormal"
    mean_T: float = 1.0
    sigma_T: float = 0.0
    lambda_cadence: float = 0.0


@dataclass
class DiagnosticsConfig:
    store_states: bool = False
    compute_lockstep: bool = True
    compute_psd: bool = False


@dataclass
class TopConfig:
    output_dir: str
    random_seed: int
    grid: GridConfig
    hop_coherence: HopCoherenceConfig
    shared_bias: SharedBiasConfig
    phase_lock: PhaseLockConfig
    domains: DomainsConfig
    cadence: CadenceConfig
    diagnostics: DiagnosticsConfig


def _to_namespace(d: Dict[str, Any]) -> SimpleNamespace:
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out[k] = _to_namespace(v)
        else:
            out[k] = v
    return SimpleNamespace(**out)


def load_config(path: str | Path) -> SimpleNamespace:
    path = Path(path)
    with path.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)

    if not isinstance(raw, dict):
        raise ValueError("Top-level YAML must be a mapping")

    for key in ("output_dir", "random_seed", "grid", "hop_coherence"):
        if key not in raw:
            raise ValueError(f"Missing required top-level key: {key}")

    grid = raw.get("grid", {})
    W_vals = grid.get("W_coh_values", [])
    N_vals = grid.get("N_values", [])
    ensembles = int(grid.get("ensembles", 16))
    steps = int(grid.get("steps", 2000))
    burn_in = int(grid.get("burn_in", steps // 10))

    if not W_vals or not N_vals:
        raise ValueError("grid.W_coh_values and grid.N_values must be non-empty lists")

    if ensembles <= 0 or steps <= 0:
        raise ValueError("grid.ensembles and grid.steps must be positive")

    if burn_in < 0 or burn_in >= steps:
        raise ValueError("grid.burn_in must satisfy 0 <= burn_in < steps")

    grid_cfg = GridConfig(
        W_coh_values=list(W_vals),
        N_values=list(N_vals),
        ensembles=ensembles,
        steps=steps,
        burn_in=burn_in,
    )

    hc = raw.get("hop_coherence", {})
    hop_cfg = HopCoherenceConfig(
        form=str(hc.get("form", "power_law")),
        alpha=float(hc.get("alpha", 1.0)),
        k_prefactor=float(hc.get("k_prefactor", 2.0)),
        memory_depth=int(hc.get("memory_depth", 1)),
    )

    sb = raw.get("shared_bias", {})
    shared_cfg = SharedBiasConfig(
        enabled=bool(sb.get("enabled", False)),
        lambda_bias=float(sb.get("lambda_bias", 0.0)),
    )

    pl = raw.get("phase_lock", {})
    phase_cfg = PhaseLockConfig(
        enabled=bool(pl.get("enabled", False)),
        lambda_phase=float(pl.get("lambda_phase", 0.0)),
        theta_join=float(pl.get("theta_join", 0.3)),
        theta_break=float(pl.get("theta_break", 1.5)),
        omega_0=float(pl.get("omega_0", 0.1)),
        noise_sigma=float(pl.get("noise_sigma", 0.0)),
    )

    dom = raw.get("domains", {})
    domains_cfg = DomainsConfig(
        enabled=bool(dom.get("enabled", False)),
        n_initial_domains=int(dom.get("n_initial_domains", 1)),
        lambda_domain=float(dom.get("lambda_domain", 0.0)),
        merge_threshold=float(dom.get("merge_threshold", 0.8)),
        split_threshold=float(dom.get("split_threshold", 0.3)),
        min_domain_size=int(dom.get("min_domain_size", 1)),
    )
    cad = raw.get("cadence", {})
    cadence_cfg = CadenceConfig(
        enabled=bool(cad.get("enabled", False)),
        distribution=str(cad.get("distribution", "lognormal")),
        mean_T=float(cad.get("mean_T", 1.0)),
        sigma_T=float(cad.get("sigma_T", 0.0)),
        lambda_cadence=float(cad.get("lambda_cadence", 0.0)),
    )



    diag = raw.get("diagnostics", {})
    diagnostics_cfg = DiagnosticsConfig(
        store_states=bool(diag.get("store_states", False)),
        compute_lockstep=bool(diag.get("compute_lockstep", True)),
        compute_psd=bool(diag.get("compute_psd", False)),
    )

    top = TopConfig(
        output_dir=str(raw.get("output_dir")),
        random_seed=int(raw.get("random_seed", 0)),
        grid=grid_cfg,
        hop_coherence=hop_cfg,
        shared_bias=shared_cfg,
        phase_lock=phase_cfg,
        domains=domains_cfg,
        cadence=cadence_cfg,
        diagnostics=diagnostics_cfg,
    )

    as_dict = {
        "output_dir": top.output_dir,
        "random_seed": top.random_seed,
        "grid": vars(top.grid),
        "hop_coherence": vars(top.hop_coherence),
        "shared_bias": vars(top.shared_bias),
        "phase_lock": vars(top.phase_lock),
        "domains": vars(top.domains),
        "cadence": vars(top.cadence),
        "diagnostics": vars(top.diagnostics),
    }

    return _to_namespace(as_dict)