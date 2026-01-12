# RUN_REPORT: run_C4_bias_plus_cadence (v0.2 cadence-gated code)

## 1. Run identification

- **Run ID:** `run_C4_bias_plus_cadence`

- **Purpose:** Test for a *cooperative* effect between shared bias and cadence glue, using parameters where each axis on its own gives a modest effect.

- **Code:** `bcqm_glue_axes` (cadence-enabled v0.2).

- **Random seed:** 45678


## 2. Configuration

- **Grid:**

  - `W_coh_values`: [20, 50, 100]

  - `N_values`: [1, 2, 4, 8]

  - `ensembles`: 32

  - `steps`: 5000

  - `burn_in`: 500

- **Hop coherence:**

  - form = `power_law`, alpha = 1.0, k_prefactor = 2.0, memory_depth = 1

- **Glue axes:**

  - shared_bias: enabled = True, lambda_bias = 0.25

  - phase_lock: enabled = False, lambda_phase = 0.0 (off)

  - domains: enabled = False, lambda_domain = 0.0 (off)

- **Cadence axis:**

  - For this run we reused the C3 cadence settings:

    - distribution = `lognormal`

    - mean_T = 1.0, sigma_T = 0.2

    - lambda_cadence = 0.15

  - `cadence_step` is called every step, setting `threads.active` via tick events and nudging periods toward the mean with strength λ_cadence.

- **Diagnostics:**

  - store_states = True, compute_lockstep = True, compute_psd = False


## 3. Key observables

Ensemble-averaged instantaneous alignment `L_inst`, lockstep length `ell_lock`, and clock quality `Q_clock` for each `(W_coh, N)` pair:

### 3.20  W_coh = 20

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 10.509 | 0.0105 |
| 2 | 0.500 | 10.363 | 0.0083 |
| 4 | 0.558 | 12.696 | 0.0188 |
| 8 | 0.601 | 19.845 | 0.0127 |

### 3.50  W_coh = 50

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 18.926 | 0.0059 |
| 2 | 0.501 | 18.711 | 0.0137 |
| 4 | 0.687 | 32.903 | 0.0003 |
| 8 | 0.793 | 113.668 | 0.0261 |

### 3.100  W_coh = 100

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 31.050 | 0.0091 |
| 2 | 0.498 | 31.051 | 0.0253 |
| 4 | 0.791 | 91.250 | 0.0165 |
| 8 | 0.890 | 289.393 | 0.0209 |

## 4. Interpretation

- **Alignment (`L_inst`):**

  - For `N = 1`, `L_inst` is exactly 1.0 at all `W_coh`, as expected for a single biased telegraph thread.

  - For `N = 2`, the alignment remains near 0.5, similar to the hop-only and cadence-only baselines.

  - For `N = 4` and `N = 8`, however, `L_inst` is noticeably higher than the pure-diffusive √N pattern:

    - At `W_coh = 20`, `L_inst` ≈ 0.56 (N=4) and 0.60 (N=8).

    - At `W_coh = 50`, `L_inst` ≈ 0.69 (N=4) and 0.79 (N=8).

    - At `W_coh = 100`, `L_inst` ≈ 0.79 (N=4) and 0.89 (N=8).

  - This indicates that bias + cadence together do generate substantially more directional coherence than cadence alone: large bundles are spending most of the time with the majority of threads aligned.

- **Lockstep length (`ell_lock`):**

  - `ell_lock` continues to grow with `W_coh` for `N = 1` (≈10.5, 18.9, 31.1 for W = 20, 50, 100).

  - For `N = 2`, the lockstep length remains very close to the single-thread values at each `W_coh`.

  - For `N = 4` and `N = 8`, there is a clear enhancement compared to C2/C3 and the hop-only baselines:

    - At `W_coh = 20`, `ell_lock` ≈ 12.7 (N=4) and 19.8 (N=8).

    - At `W_coh = 50`, `ell_lock` ≈ 32.9 (N=4) and 113.7 (N=8).

    - At `W_coh = 100`, `ell_lock` ≈ 91.3 (N=4) and 289.4 (N=8).

  - Particularly for `N = 8`, the lockstep length at large `W_coh` is an order of magnitude larger than the single-thread value, showing that the bundle COM can stay “stuck” in a preferred direction over very long stretches.

- **Clock quality (`Q_clock`):**

  - `Q_clock` values lie in the ~0.005–0.026 range and do not show a simple monotone scaling in `N`.

  - The largest values occur at `(W_coh=100, N=2)` and `(W_coh=50, N=8)`, but overall the clock metric remains modest: even when the bundle is stiff, the zero-crossings are not yet forming a sharply periodic clock.

## 5. Conclusion on cooperative effects

- Compared to the cadence-only run (C3), adding shared bias clearly amplifies directional coherence for larger bundles: `L_inst` for `N = 4, 8` climbs well above the pure √N diffusive pattern.

- The corresponding lockstep lengths show that the COM can remain aligned for durations that are **much longer** than a single-thread persistence time, especially for `N = 8` at high `W_coh`.

- This is evidence for a genuine *cooperative* regime between bias and cadence: cadence does not create stiffness on its own, but in the presence of bias it helps bundles settle into and maintain a strongly preferred direction.

- However, even in this regime the behaviour remains stochastic rather than fully ballistic: the COM can still wander and `Q_clock` remains modest, so this is more like a “strongly biased diffusive” phase than a clean inertial/ballistic phase.

- For BCQM V, the C4 run supports the narrative that:

  - cadence is a **supporting glue axis** that becomes important when combined with other axes (here: shared bias),

  - there is a spectrum from diffusive → strongly biased diffusive → ultra-rigid (as in 2×2 hierarchical experiments), and

  - the physically interesting bundles (candidate mass/spacetime carriers) likely live in an intermediate regime where multiple glue axes cooperate without freezing the dynamics completely.
