# RUN_REPORT: run_C9_phase_domains_cadence (v0.2 cadence-gated code)

## 1. Run identification

- **Run ID:** `run_C9_phase_domains_cadence`

- **Purpose:** Explore cooperative effects between **phase-lock glue**, **domain glue**, and **cadence**, and compare with phase+cadence (C5) and domains+cadence (C6).

- **Code:** `bcqm_glue_axes` (cadence-enabled v0.2).

- **Random seed:** 90123


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

  - shared_bias: enabled = False (off)

  - phase_lock: enabled = True, lambda_phase = 0.25, omega_0 = 0.1, theta_join = 0.3, theta_break = 1.5, noise_sigma = 0.0

  - domains: enabled = True, n_initial_domains = 4, lambda_domain = 0.25, merge_threshold = 0.8, split_threshold = 0.3, min_domain_size = 1

- **Cadence axis:**

  - Enabled (as in previous C-runs):

    - distribution = `lognormal`

    - mean_T = 1.0, sigma_T ≈ 0.2

    - lambda_cadence = 0.15

- **Diagnostics:**

  - store_states = True, compute_lockstep = True, compute_psd = False


## 3. Key observables

Ensemble-averaged instantaneous alignment `L_inst`, lockstep length `ell_lock`, and clock quality `Q_clock` for each `(W_coh, N)` pair:

### 3.20  W_coh = 20

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 10.268 | 0.005 |
| 2 | 0.625 | 10.062 | 0.284 |
| 4 | 0.537 | 11.464 | 0.301 |
| 8 | 0.487 | 12.997 | 0.287 |

### 3.50  W_coh = 50

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 18.725 | 0.011 |
| 2 | 0.717 | 17.197 | 0.588 |
| 4 | 0.664 | 24.213 | 0.597 |
| 8 | 0.654 | 42.875 | 0.570 |

### 3.100  W_coh = 100

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 34.066 | 0.023 |
| 2 | 0.795 | 23.230 | 0.901 |
| 4 | 0.773 | 46.086 | 0.786 |
| 8 | 0.795 | 136.297 | 0.831 |

## 4. Interpretation

- **Alignment (`L_inst`):**

  - `N = 1`: `L_inst = 1.0` at all `W_coh`, as expected.

  - `N = 2`: alignment rises with `W_coh`:

    - ≈0.625 at `W_coh = 20`, ≈0.717 at 50, ≈0.795 at 100.

  - `N = 4` and `N = 8`: alignment becomes quite strong at large `W_coh`:

    - `W_coh = 50`: `L_inst` ≈0.664 (N=4) and ≈0.654 (N=8).

    - `W_coh = 100`: `L_inst` ≈0.773 (N=4) and ≈0.795 (N=8).

  - These values are lower than in the bias-containing runs (C4, C7, C8), but clearly above pure diffusive √N scaling, indicating that phase+domains+cadence do cooperatively enhance directional coherence.

- **Lockstep length (`ell_lock`):**

  - `N = 1`: `ell_lock` grows with `W_coh` (≈10.3, 18.7, 34.1), consistent with other runs.

  - `N = 2`: lockstep stays near the single-thread value at each `W_coh`.

  - `N = 4` and `N = 8`: `ell_lock` shows a clear enhancement, especially for large `W_coh`:

    - `W_coh = 50`: ≈24.2 (N=4) and ≈42.9 (N=8).

    - `W_coh = 100`: ≈46.1 (N=4) and ≈136.3 (N=8).

  - This is qualitatively similar to the phase+cadence and domains+cadence runs: bundles persist longer than a single thread, but not to the extreme degree seen in bias-dominated cases.

- **Clock quality (`Q_clock`):**

  - `Q_clock` is small for `N = 1` at all `W_coh` (≲0.02).

  - For `N ≥ 2`, `Q_clock` rises sharply with `W_coh`:

    - `W_coh = 20`: ~0.28–0.30 for N=2,4,8.

    - `W_coh = 50`: ~0.59–0.60 for N=2,4,8.

    - `W_coh = 100`: ≈0.90 (N=2), ≈0.79 (N=4), ≈0.83 (N=8).

  - These values are comparable to, though slightly below, the pure phase+cadence (C5) high-Q regime, and notably **higher** than domains+cadence (C6).

## 5. Conclusion on cooperative effects

- C9 shows that combining **phase-lock + domains + cadence** yields a regime that is closer to the phase+cadence case than to pure domains+cadence:

  - Directional alignment and lockstep are moderately enhanced, but do not reach the stiffness of bias-containing runs.

  - Clock quality `Q_clock` is high (≈0.8–0.9) for multi-thread bundles at large `W_coh`, confirming that phase-lock remains the main driver of good clocks even when domains are present.

- Domains again appear largely *neutral* with respect to the clock physics: they decorate the structure but do not significantly change the high-Q behaviour produced by phase+cadence.

- Taken together with C5 and C6, C9 reinforces the pattern:

  - Phase-lock + cadence ⇒ good clocks; adding domains preserves this property.

  - Domains + cadence without phase (C6) ⇒ only mild effects on both stiffness and clocks.

- For BCQM V, C9 helps complete the glue-axis phase diagram: it shows that the “clock-like bundle” phase is robust under the addition of domains, whereas the “stiff bundle” phase requires bias.
