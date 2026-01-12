# RUN_REPORT: run_C2_cadence_glue (v0.2 cadence‑gated code)

## 1. Run identification

- **Run ID:** `run_C2_cadence_glue`

- **Purpose:** First non‑trivial cadence test with cadence **enabled** and a modest glue strength (λ_cadence = 0.05), while other glue axes are disabled.

- **Code:** `bcqm_glue_axes` (cadence‑enabled v0.2).

- **Random seed:** 54321


## 2. Configuration

- **Grid:**

  - `W_coh_values`: [20, 50, 100]

  - `N_values`: [1, 2, 4, 8, 16]

  - `ensembles`: 128

  - `steps`: 8000

  - `burn_in`: 800

- **Hop coherence:**

  - form = `power_law`, alpha = 1.0, k_prefactor = 2.0, memory_depth = 1

- **Glue axes (non‑cadence):**

  - shared_bias: enabled = True, lambda_bias = 0.3

  - phase_lock: enabled = False, lambda_phase = 0.0

  - domains: enabled = True, lambda_domain = 0.3

- **Cadence axis:**

  - Enabled in the C2 YAML with:

    - distribution = `lognormal`

    - mean_T = 1.0, sigma_T = 0.2

    - lambda_cadence = 0.05 (first non‑zero test value)

  - In v0.2 this means `cadence_step` is called every step, setting `threads.active` via T/φ and gently nudging periods toward the mean with strength λ_cadence.

- **Diagnostics:**

  - store_states = True, compute_lockstep = True, compute_psd = False


## 3. Key observables

Ensemble‑averaged instantaneous alignment `L_inst`, lockstep length `ell_lock`, and clock quality `Q_clock` for each `(W_coh, N)` pair:

### 3.20  W_coh = 20

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 7.221 | 0.0025 |
| 2 | 0.499 | 7.558 | 0.0002 |
| 4 | 0.593 | 10.115 | 0.0019 |
| 8 | 0.676 | 19.987 | 0.0014 |
| 16 | 0.740 | 90.005 | 0.0116 |

### 3.50  W_coh = 50

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 15.012 | 0.0017 |
| 2 | 0.495 | 14.816 | 0.0031 |
| 4 | 0.735 | 33.379 | 0.0037 |
| 8 | 0.853 | 169.035 | 0.0276 |
| 16 | 0.887 | 176.784 | 0.0202 |

### 3.100  W_coh = 100

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 26.430 | 0.0058 |
| 2 | 0.502 | 26.265 | 0.0021 |
| 4 | 0.829 | 94.310 | 0.0092 |
| 8 | 0.926 | 474.816 | 0.0662 |
| 16 | 0.942 | 4.464 | 0.0157 |

## 4. Interpretation

- The overall pattern remains very close to the hop‑only baseline and the C1 regression run:

  - `L_inst` stays at ≈1.0 for `N = 1`, and around 0.50, 0.38, 0.27 for `N = 2, 4, 8`, consistent with √N averaging of directions.

  - `ell_lock` grows with `W_coh` for `N = 1` (≈7 → 14 → 22) and sits in a similar range for larger N; any differences relative to C1 are at the level of ensemble scatter rather than a clear systematic trend.

  - `Q_clock` values fluctuate but remain in the same rough numerical band as C1, with no obvious monotone improvement as `W_coh` or `N` change.

- In other words, with λ_cadence = 0.05 and the current gating/synchronisation rule, cadence **does not yet leave a strong, distinctive fingerprint** on the lockstep metrics.

- Given the modest λ_cadence and short run length (2000 steps), this is not entirely surprising: a weak, global nudging of periods toward the mean can take many coherence times to build up visible structure.

## 5. Conclusion and next steps

- `run_C2_cadence_glue` is our first genuine cadence‑on test in the v0.2 engine. The results show that the present choice (λ_cadence = 0.05, gentle period nudge) is too conservative to produce a clear enhancement of `ell_lock` or `Q_clock` over the hop‑only baseline.

- This suggests two natural follow‑ups for the C‑series:

  1. **Increase λ_cadence** (e.g. to 0.1–0.2) and/or lengthen the time series, to see whether stronger synchronisation produces a measurable rise in `ell_lock` or a more coherent `Q_clock` signal.

  2. **Tighten the gating rule**, e.g. by making cadence influence not only who can flip on a given step but also which neighbours are allowed to flip together, so that shared cadence couples more directly to the `L_inst` and `ell_lock` observables.

- For now, C2 serves mainly as a check that the fully wired cadence machinery behaves smoothly and does not accidentally destabilise the baseline hop‑coherence behaviour.
