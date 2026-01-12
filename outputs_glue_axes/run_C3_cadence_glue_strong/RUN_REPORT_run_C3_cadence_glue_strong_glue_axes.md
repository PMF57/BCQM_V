# RUN_REPORT: run_C3_cadence_glue_strong (v0.2 cadence-gated code)

## 1. Run identification

- **Run ID:** `run_C3_cadence_glue_strong`

- **Purpose:** Probe stronger cadence glue (λ_cadence = 0.15) and a longer time series to test whether cadence can measurably enhance lockstep and clock quality.

- **Code:** `bcqm_glue_axes` (cadence-enabled v0.2).

- **Random seed:** 34567


## 2. Configuration

- **Grid:**

  - `W_coh_values`: [20, 50, 100]

  - `N_values`: [1, 2, 4, 8]

  - `ensembles`: 32

  - `steps`: 5000

  - `burn_in`: 500

- **Hop coherence:**

  - form = `power_law`, alpha = 1.0, k_prefactor = 2.0, memory_depth = 1

- **Glue axes (non-cadence):**

  - shared_bias: enabled = False, lambda_bias = 0.0

  - phase_lock: enabled = False, lambda_phase = 0.0

  - domains: enabled = False, lambda_domain = 0.0

- **Cadence axis:**

  - Enabled with:

    - distribution = `lognormal`

    - mean_T = 1.0, sigma_T = 0.2

    - lambda_cadence = 0.15 (stronger than C2’s 0.05)

  - `cadence_step` is called every step, setting `threads.active` via tick events and nudging periods toward the mean with strength λ_cadence.

- **Diagnostics:**

  - store_states = True, compute_lockstep = True, compute_psd = False


## 3. Key observables

Ensemble-averaged instantaneous alignment `L_inst`, lockstep length `ell_lock`, and clock quality `Q_clock` for each `(W_coh, N)` pair:

### 3.20  W_coh = 20

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 10.105 | 0.0199 |
| 2 | 0.500 | 9.915 | 0.0047 |
| 4 | 0.375 | 10.324 | 0.0120 |
| 8 | 0.273 | 9.600 | 0.0132 |

### 3.50  W_coh = 50

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 18.003 | 0.0031 |
| 2 | 0.507 | 17.834 | 0.0035 |
| 4 | 0.378 | 17.971 | 0.0151 |
| 8 | 0.273 | 17.414 | 0.0203 |

### 3.100  W_coh = 100

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 30.979 | 0.0261 |
| 2 | 0.501 | 30.932 | 0.0095 |
| 4 | 0.371 | 30.736 | 0.0476 |
| 8 | 0.276 | 30.296 | 0.0084 |

## 4. Interpretation

- **Alignment (`L_inst`):**

  - As in C1/C2 and the hop-only baselines, `L_inst` ≈ 1.0 for `N = 1` and follows the expected √N pattern for larger bundles:

    - ≈0.50 for `N = 2`, ≈0.37–0.38 for `N = 4`, and ≈0.27–0.28 for `N = 8` across all `W_coh`.

  - Stronger cadence glue does **not** drive any visible drift toward more rigid alignment in this observable; directions still look like averaged telegraph processes.

- **Lockstep length (`ell_lock`):**

  - `ell_lock` continues to scale up with `W_coh` in a smooth way:

    - For `N = 1`: ≈10.1 (W=20), ≈18.0 (W=50), ≈31.0 (W=100).

    - For `N = 2, 4, 8` the lockstep lengths are very close to these single-thread values at each `W_coh`.

  - Compared to C2, there is a modest overall increase in `ell_lock` (especially at large `W_coh`), but the pattern is still essentially “single-thread-like”: the bundle COM is not dramatically stiffer than its constituents.

- **Clock quality (`Q_clock`):**

  - `Q_clock` sits in the ~0.003–0.048 range, with no clean monotone trend in `N`.

  - The largest values appear at `(W_coh=100, N=4)` but are still small; we do not yet see a sharp emergence of a high-quality global clock from cadence alone.

## 5. Conclusion and next steps

- `run_C3_cadence_glue_strong` shows that even with stronger cadence glue (λ_cadence = 0.15) and longer time series (5000 steps), cadence on its own does **not** produce a dramatic enhancement of COM lockstep or clock quality compared to the hop-only baseline.

- Cadence clearly does not *break* the dynamics, and there is a hint of slightly longer lockstep at high `W_coh`, but the effect is modest and does not move the system into a qualitatively new regime.

- This supports the emerging picture that cadence is best viewed as a **supporting glue axis**: by itself it does not create ultra-rigid bundles, but it may become important when combined with shared bias, phase-lock, or domain structure.

- For BCQM V, this run provides a useful data point: we can say explicitly that “even with cadences synchronised at λ_cadence ≈ 0.15, the COM remains in the same diffusive universality class; cadence is not a magic shortcut to ballistic behaviour.”
