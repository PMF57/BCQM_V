# RUN_REPORT: run_C1_cadence_only (v0.2 cadence-gated code)

## 1. Run identification

- **Run ID:** `run_C1_cadence_only`

- **Purpose:** Regression check for the cadence-gated engine with cadence *disabled* in the config.

- **Code:** `bcqm_glue_axes` (cadence-enabled v0.2).

- **Random seed:** 12345


## 2. Configuration

- **Grid:**

  - `W_coh_values`: [20, 50, 100]

  - `N_values`: [1, 2, 4, 8]

  - `ensembles`: 32

  - `steps`: 2000

  - `burn_in`: 200

- **Hop coherence:**

  - form = `power_law`, alpha = 1.0, k_prefactor = 2.0, memory_depth = 1

- **Glue axes (non-cadence):**

  - shared_bias: enabled = False, lambda_bias = 0.0

  - phase_lock: enabled = False, lambda_phase = 0.0

  - domains: enabled = False, lambda_domain = 0.0

- **Cadence axis in this config:**

  - No explicit `cadence:` block in the YAML; the `CadenceConfig` therefore defaults to `enabled = False`.

  - In the v0.2 engine this means `cadence_step` is called but simply marks all threads as active each step (no cadence gating).

- **Diagnostics:**

  - store_states = True, compute_lockstep = True, compute_psd = False


## 3. Key observables

Ensemble-averaged instantaneous alignment `L_inst`, lockstep length `ell_lock`, and clock quality `Q_clock` for each `(W_coh, N)` pair:

### 3.20  W_coh = 20

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 7.448 | 0.0000 |
| 2 | 0.495 | 7.538 | 0.0021 |
| 4 | 0.377 | 7.276 | 0.0158 |
| 8 | 0.271 | 7.646 | 0.0106 |

### 3.50  W_coh = 50

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 14.310 | 0.0383 |
| 2 | 0.503 | 13.556 | 0.0070 |
| 4 | 0.375 | 14.055 | 0.0134 |
| 8 | 0.276 | 15.486 | 0.0051 |

### 3.100  W_coh = 100

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 25.883 | 0.0369 |
| 2 | 0.498 | 23.867 | 0.0407 |
| 4 | 0.379 | 24.593 | 0.0565 |
| 8 | 0.272 | 24.349 | 0.0375 |

## 4. Interpretation

- The pattern of observables is essentially identical to the earlier hop-only A1 runs:

  - `L_inst` ≈ 1 for `N = 1`, and drops toward ≈0.5, 0.38, 0.27 for `N = 2, 4, 8`, matching the expected √N averaging behaviour.

  - `ell_lock` increases with `W_coh` for `N = 1` (≈7.4 → 14.3 → 25.9) and stays in a similar range for larger N, indicating that the basic persistence vs. coherence-horizon relation is unchanged.

  - `Q_clock` values are small but non-zero and live in the same numerical ballpark as in the pre-cadence engine.

- This confirms that the introduction of the cadence machinery (T, φ, active mask) does **not** alter the dynamics when cadence is disabled in the configuration.

## 5. Conclusion

- `run_C1_cadence_only` (with cadence disabled) is a clean regression test for the v0.2 engine: results are consistent with the original hop-only behaviour.

- This baseline is what we compare against when we turn cadence **on** (λ_cadence > 0) in the C2 and subsequent runs.
