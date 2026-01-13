# BCQM V glue-axes code (`bcqm_glue_axes`)

This repository contains the production code used in **BCQM V** to study
how different “glue axes” between primitive threads give rise to
bundle–level phases: diffusive, stiff, clock–like, and mixed regimes.

The code simulates a **single bundle** of many primitive threads evolving
on a 1D event chain with:

- hop–coherence / slip law (BCQM–style W_coh dependence),
- shared bias (directional drift glue),
- phase–lock (phase–synchronisation glue),
- domains (shared label / region glue),
- cadence (per–thread hop cadence, with optional cadence–glue).

The main observables are:

- instantaneous alignment `L_inst`,
- typical lockstep length `ell_lock`,
- and clock quality `Q_clock`.

These are the quantities used throughout the BCQM V text and lab notes.

---

## 1. Repository layout

At the top level you should see something like:

- `bcqm_glue_axes/`
  - `__init__.py`
  - `cli.py` – command–line entry point (`python -m bcqm_glue_axes.cli …`)
  - `config_schemas.py` – config loading and validation
  - `simulate.py` – core simulation loop and observables
  - `analysis.py` – helper routines for post–processing (where needed)
- `configs/`
  - YAML configuration files for all A/B/C/V/S runs
- `outputs_glue_axes/`
  - One subdirectory per run (created automatically)
- `README.md` – this file
- `PROGRAMS.md` – short guide to the standard runs
- `CITATION.cff` – citation metadata (once you’ve added it)
- Any plotting scripts you have copied in (e.g. `plot_lockstep_B_series.py`).

The code does **not** depend on heavy external libraries: standard Python
3, `numpy` and `pyyaml` are sufficient.

---

## 2. Installation

The simplest workflow is to clone the repo and run it in–place:

```bash
git clone https://github.com/PMF57/BCQM_V_glue_axes.git
cd BCQM_V_glue_axes

# (optional) create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt  # if present
# otherwise: pip install numpy pyyaml
```

You do **not** need to install the package system–wide; running it with
`python -m bcqm_glue_axes.cli` from the repo root is enough.

---

## 3. Basic usage

All simulations are driven by YAML config files in `configs/`.

The general pattern is:

```bash
python3 -m bcqm_glue_axes.cli run configs/<config_name>.yml
```

This will:

1. Load and validate the YAML config;
2. Run the specified grid of (`W_coh`, `N`) values for the requested
   number of steps and ensembles;
3. Write results into a fresh subdirectory of `outputs_glue_axes/` that
   matches the `run_id` in the config.

Each output folder contains at least:

- `metadata.json` – full record of the configuration actually used;
- `summary.json` – per–(W_coh, N) summary of `L_inst`, `ell_lock`,
  `Q_clock`, etc.

We then generate human–readable summaries by hand using small helper
scripts or notebooks, and store them as:

- `RUN_REPORT_<run_id>.md` – natural–language summary of each run.

---

## 4. Configuration structure (high level)

A typical config looks like:

```yaml
run_id: run_A3_phase_lock
output_root: outputs_glue_axes

grid:
  W_coh_values: [20, 50, 100]
  N_values: [1, 2, 4, 8]
  ensembles: 32
  steps: 5000
  burn_in: 500

hop_coherence:
  form: power_law
  alpha: 1.0
  k_prefactor: 2.0
  memory_depth: 1

shared_bias:
  enabled: false
  lambda_bias: 0.0

phase_lock:
  enabled: true
  lambda_phase: 0.25
  theta_join: 0.3
  theta_break: 1.5
  omega_0: 0.1
  noise_sigma: 0.0

domains:
  enabled: false
  n_initial_domains: 1
  lambda_domain: 0.0
  merge_threshold: 0.8
  split_threshold: 0.3
  min_domain_size: 1

cadence:
  enabled: true
  distribution: lognormal
  mean_T: 1.0
  sigma_T: 0.2
  lambda_cadence: 0.15

diagnostics:
  store_states: true
  compute_lockstep: true
  compute_psd: false
```

The **A-series** configs switch on only one axis at a time; the **C-series**
configs combine cadence with various other axes; the **V1/S** configs turn on
all axes and/or probe symmetry and convergence. See `PROGRAMS.md` for the
canonical list.

---

## 5. Reproducing the main BCQM V runs

The key runs used in the BCQM V analysis are grouped as:

- **A-series (single–axis tests):**  
  Hop coherence only, bias only, phase only, domains only.

- **V1 + symmetry + convergence:**  
  Full glue axes switched on; symmetry sanity check; convergence tests.

- **C-series (cadence and co–operative effects):**  
  Cadence only, cadence+single axis, and all two–axis combinations with
  cadence, plus the three–axis case (bias + phase + cadence).

The exact mapping `run_id ↔ config file` is documented in `PROGRAMS.md`.
To regenerate all of them you can simply loop over the configs in that
table and call:

```bash
python3 -m bcqm_glue_axes.cli run configs/<that_run>.yml
```

---

## 6. Citing this code

If you use this repository directly in any publication, please cite both:

- the main **BCQM V paper**, and  
- the **Zenodo record for this code** (once minted).

A typical BibTeX entry for the code might look like:

```bibtex
@software{bcqm_glue_axes,
  author       = {Ferguson, Peter M.},
  title        = {BCQM V glue-axes bundle code (bcqm_glue_axes)},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.xxxxxxx},
  url          = {https://doi.org/10.5281/zenodo.xxxxxxx}
}
```

(Replace `xxxxxxx` with the actual DOI and keep the repo’s `CITATION.cff`
in sync.)

---

## 7. Provenance and reproducibility

This code is designed to act as a **reproducibility companion** to BCQM V:

- Every run is driven by a named YAML config,
- Every output folder carries a full `metadata.json` copy of that config,
- RUN\_REPORTs describe how each run was interpreted in the lab notes and paper.

If you need to extend the experiments (e.g. new glue regimes or different
grids), the recommended approach is to:

1. Clone an existing config as a starting point;
2. Change as little as possible (ideally only one or two parameters);
3. Give the new run a clear `run_id` and document it in a new RUN\_REPORT.
---

## 8. Related BCQM V paper

This repository provides the glue–axes simulations used in the fifth paper of the
Boundary–Condition Quantum Mechanics programme:

- P.~M.~Ferguson, *Boundary–Condition Quantum Mechanics V: Lockstep bundles and emergent time*,
  Zenodo record \href{https://doi.org/10.5281/zenodo.18233747}{doi:10.5281/zenodo.18233747}.

If you use this code in your own work, please cite both:

- the BCQM~V paper (Zenodo record \href{https://doi.org/10.5281/zenodo.18233747}{doi:10.5281/zenodo.18233747}), and
- this software record (Zenodo code DOI \href{https://doi.org/10.5281/zenodo.18234061}{doi:10.5281/zenodo.18234061}).

The repository also includes a `CITATION.cff` file with the same metadata.

