# PROGRAMS.md – BCQM V glue-axes standard runs

This file lists the **canonical runs** used in the BCQM V glue-axes
analysis. Each run is defined by a YAML file in `configs/` and writes its
results into a matching subdirectory under `outputs_glue_axes/`.

The exact filenames may differ slightly depending on how you name your
configs (e.g. with or without `_glue_axes`), but the `run_id` field in the
YAML and the output folder name should match the identifiers listed here.

---

## A-series: single-axis tests

These runs establish the behaviour of each glue axis in isolation.

| Run ID               | Purpose                                | Notes                       |
|----------------------|----------------------------------------|-----------------------------|
| `run_A1_hop_only`    | Hop coherence only                     | Baseline W_coh–dependent slip law; other glue disabled. |
| `run_A2_shared_bias` | Shared bias only                       | Tests pure directional drift glue. |
| `run_A3_phase_lock`  | Phase lock only                        | Tests pure phase-synchronisation glue; main source of clock-like behaviour. |
| `run_A4_domains`     | Domains only                           | Tests domain glue as a spectator axis. |

Each uses a small grid: W_coh = {20, 50, 100}, N = {1, 2, 4, 8},
32 ensembles, 5000 steps, 500 burn-in.

---

## V1, symmetry, and convergence runs

These runs exercise the full system and check that observables are stable.

| Run ID                     | Purpose                                      |
|----------------------------|----------------------------------------------|
| `run_V1_all_axes`          | All glue axes enabled (hop, bias, phase, domains, cadence) – baseline “everything on” regime. |
| `run_S_symmetry`           | Symmetry sanity check (e.g. sign flips, label permutations) to confirm no hidden bias. |
| `run_V1_all_axes_conv`     | Long convergence run for `run_V1_all_axes`. |
| `run_A2_shared_bias_conv`  | Convergence run for the bias-only case.     |
| `run_A3_phase_lock_conv`   | Convergence run for the phase-only case.    |

You can map these run IDs to the corresponding YAML filenames in
`configs/` (e.g. `configs/run_V1_all_axes.yml`, etc.) according to your
naming convention.

---

## C-series: cadence and co-operative effects

The C-series explores how the **cadence axis** interacts with the other
glue axes. All runs use the same grid (W_coh, N) as the A-series.

| Run ID                         | Glue axes enabled                        | Comment                                  |
|--------------------------------|------------------------------------------|------------------------------------------|
| `run_C1_cadence_only`          | Cadence only                             | Checks that cadence alone does not create stiffness or clocks. |
| `run_C2_cadence_glue`          | Cadence (stronger) only                  | Sanity check for stronger cadence glue.  |
| `run_C3_cadence_glue_strong`   | Cadence (very strong) only               | Confirms no hidden co-operative effect appears. |
| `run_C4_bias_plus_cadence`     | Bias + cadence                           | Stiff bundles; pointer-like behaviour.   |
| `run_C5_phase_plus_cadence`    | Phase lock + cadence                     | Good clocks; moderate stiffness.         |
| `run_C6_domains_plus_cadence`  | Domains + cadence                        | Mild modifications; domains as spectator axis. |
| `run_C7_bias_phase_cadence`    | Bias + phase lock + cadence              | Co-operative regime: stiff and clock-like for moderate N. |
| `run_C8_bias_domains_cadence`  | Bias + domains + cadence                 | Similar to bias+cadence; domains largely spectator. |
| `run_C9_phase_domains_cadence` | Phase lock + domains + cadence           | Clock-like bundles; domains do not spoil high-Q behaviour. |

For each run, the corresponding output directory
`outputs_glue_axes/<run_id>/` contains:

- `metadata.json` – full configuration for that run,
- `summary.json` – per-(W_coh, N) summary of observables.

The lab notes:

- `BCQM_V_glue_axes_A_series_lab_note_YYYY-MM-DD.tex`
- `BCQM_V_glue_axes_C_series_lab_note_YYYY-MM-DD.tex`

and the various `RUN_REPORT_<run_id>.md` files give the detailed
interpretation of each run and are the canonical reference for how these
results feed into the BCQM V paper.

---

## Extending the run set

If you add new runs (e.g. different glue strengths or grids), please:

1. Clone the closest existing config in `configs/`,
2. Change as few parameters as possible,
3. Give the new run a clear `run_id`,
4. Add a row to this table documenting its purpose,
5. Generate a new `RUN_REPORT_<run_id>.md` that explains what you learned.

This keeps the code+data package self-documenting and makes it easier
to track which runs are actually used in published BCQM work.
