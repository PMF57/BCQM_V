# RUN_REPORT: run_C8_bias_domains_cadence (v0.2 cadence-gated code)

## 1. Run identification

- **Run ID:** `run_C8_bias_domains_cadence`

- **Purpose:** Explore cooperative effects between **shared bias**, **domain glue**, and **cadence**, and compare with the bias+cadence (C4) and domains+cadence (C6) runs.

- **Code:** `bcqm_glue_axes` (cadence-enabled v0.2).

- **Random seed:** 89012


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

  - phase_lock: enabled = False (off)

  - domains: enabled = True, n_initial_domains = 4, lambda_domain = 0.25, merge_threshold = 0.8, split_threshold = 0.3, min_domain_size = 1

- **Cadence axis:**

  - Enabled with the standard settings:

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

| 1 | 1.000 | 10.844 | 0.0034 |
| 2 | 0.500 | 9.655 | 0.0126 |
| 4 | 0.568 | 12.937 | 0.0084 |
| 8 | 0.632 | 22.019 | 0.0105 |

### 3.50  W_coh = 50

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 18.380 | 0.0091 |
| 2 | 0.500 | 18.195 | 0.0187 |
| 4 | 0.710 | 37.194 | 0.0262 |
| 8 | 0.817 | 138.365 | 0.0025 |

### 3.100  W_coh = 100

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 30.206 | 0.0089 |
| 2 | 0.514 | 32.749 | 0.0003 |
| 4 | 0.797 | 82.450 | 0.0078 |
| 8 | 0.907 | 278.079 | 0.0067 |

## 4. Interpretation

- **Alignment (`L_inst`):**

  - `N = 1`: `L_inst = 1.0` at all `W_coh`, as expected for a single biased thread.

  - `N = 2`: `L_inst` stays ~0.50–0.51 for all `W_coh`, i.e. very close to the √N diffusive reference.

  - `N = 4, 8`: alignment is significantly enhanced at larger `W_coh`:

    - At `W_coh = 50`, `L_inst` ≈ 0.71 (N=4), 0.82 (N=8).

    - At `W_coh = 100`, `L_inst` ≈ 0.80 (N=4), 0.91 (N=8).

  - These values are very similar to the bias+cadence case (C4), showing that adding domains does *not* spoil the strong directional stiffness induced by bias+cadence.

- **Lockstep length (`ell_lock`):**

  - `N = 1`: `ell_lock` grows with `W_coh` (≈10.8, 18.4, 30.2), matching previous baselines.

  - `N = 2`: lockstep remains essentially at the single-thread level.

  - `N = 4, 8`: there is a substantial enhancement, especially for `N = 8` at large `W_coh`:

    - At `W_coh = 50`, `ell_lock` ≈ 37.2 (N=4) and ≈138.4 (N=8).

    - At `W_coh = 100`, `ell_lock` ≈ 82.5 (N=4) and ≈278.1 (N=8).

  - These numbers are extremely close to the bias+cadence (C4) run, indicating that domains do not strongly modify the lockstep statistics when bias is present; bias remains the dominant driver of long-lived directional alignment.

- **Clock quality (`Q_clock`):**

  - `Q_clock` is small throughout (≲0.03), with no clear monotone trend in `N` and only mild growth with `W_coh`.

  - This mirrors the bias+cadence case: even when bundles are very stiff, they do not automatically become good clocks.

  - Adding domains on top of bias+cadence does not create the high-Q regime seen in the phase+cadence (C5) and bias+phase+cadence (C7) runs.

## 5. Conclusion on cooperative effects

- In C8, combining **bias + domains + cadence** essentially reproduces the bias+cadence behaviour:

  - Large bundles (N = 4, 8) are strongly aligned at high `W_coh` and have very long lockstep lengths (`ell_lock` for N=8 at W=100 ≈ 278).

  - Domain glue does not significantly enhance or suppress this stiffness; it appears mostly neutral when bias is already present.

  - Clock quality remains low; domains do not cooperate with cadence to generate a good clock in the presence of bias.

- Qualitatively, domains here act more like a *spectator* glue axis when strong bias is present: they structure labels/regions but do not change the leading alignment or clock physics.

- For BCQM V, C8 reinforces the hierarchy we saw earlier:

  - Bias is the primary route to directional stiffness (especially when combined with cadence).

  - Phase-lock is the main route to high-Q clocks (especially with cadence).

  - Domains mostly modulate structure without dramatically altering either stiffness or clock behaviour, at least in this parameter regime.
