# RUN_REPORT: run_C6_domains_plus_cadence (v0.2 cadence-gated code)

## 1. Run identification

- **Run ID:** `run_C6_domains_plus_cadence`

- **Purpose:** Test for cooperative effects between **domain glue** and **cadence glue**, analogous to the bias+cadence (C4) and phase+cadence (C5) runs.

- **Code:** `bcqm_glue_axes` (cadence-enabled v0.2).

- **Random seed:** 67890


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

  - shared_bias: enabled = False, lambda_bias = 0.0 (off)

  - phase_lock: enabled = False, lambda_phase = 0.0 (off)

  - domains: enabled = True, lambda_domain = 0.25, n_initial_domains = 4, merge_threshold = 0.8, split_threshold = 0.3, min_domain_size = 1

- **Cadence axis:**

  - Enabled with the same settings as C3–C5:

    - distribution = `lognormal`

    - mean_T = 1.0, sigma_T ≈ 0.2

    - lambda_cadence = 0.15

  - `cadence_step` is called every step, gating which threads are active and nudging periods toward the mean.

- **Diagnostics:**

  - store_states = True, compute_lockstep = True, compute_psd = False


## 3. Key observables

Ensemble-averaged instantaneous alignment `L_inst`, lockstep length `ell_lock`, and clock quality `Q_clock` for each `(W_coh, N)` pair:

### 3.20  W_coh = 20

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 9.969 | 0.0035 |
| 2 | 0.494 | 10.336 | 0.0019 |
| 4 | 0.398 | 10.325 | 0.0037 |
| 8 | 0.319 | 11.297 | 0.0014 |

### 3.50  W_coh = 50

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 19.063 | 0.0072 |
| 2 | 0.499 | 18.953 | 0.0008 |
| 4 | 0.419 | 18.515 | 0.0051 |
| 8 | 0.344 | 22.409 | 0.0064 |

### 3.100  W_coh = 100

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 26.911 | 0.0377 |
| 2 | 0.503 | 32.665 | 0.0051 |
| 4 | 0.455 | 40.617 | 0.0106 |
| 8 | 0.378 | 41.862 | 0.0301 |

## 4. Interpretation

- **Alignment (`L_inst`):**

  - For `N = 1`, `L_inst` is 1.0 at all `W_coh`, as expected.

  - For `N = 2`, `L_inst` stays very close to the diffusive √N value (~0.5) across all `W_coh`.

  - For `N = 4` and `N = 8`, `L_inst` is modestly above the pure √N baseline but still relatively small:

    - At `W_coh = 20`, `L_inst` ≈ 0.40 (N=4) and 0.32 (N=8).

    - At `W_coh = 100`, `L_inst` ≈ 0.45 (N=4) and 0.38 (N=8).

  - In contrast to C4 (bias+cadence), there is **no large jump** toward ultra-stiff alignment; domains+cadence leave the bundle directions only mildly more coherent than diffusive.

- **Lockstep length (`ell_lock`):**

  - `ell_lock` grows with `W_coh` for `N = 1` (≈10.0, 19.1, 26.9 for W = 20, 50, 100), consistent with hop-only and cadence-only baselines.

  - For `N = 2`, lockstep stays close to the single-thread values at each `W_coh`.

  - For `N = 4` and `N = 8`, `ell_lock` increases somewhat with `N` and `W_coh`, but only by factors of order unity:

    - At `W_coh = 100`, `ell_lock` ≈ 40.6 (N=4) and ≈41.9 (N=8), compared to ≈26.9 for N=1.

  - This suggests that domains+cadence do produce slightly longer alignment stretches for larger bundles, but the effect is modest and far weaker than the bias+cadence case.

- **Clock quality (`Q_clock`):**

  - `Q_clock` is small at low `W_coh` and rises somewhat at `W_coh = 100`:

    - At `W_coh = 100`, `Q_clock` ≈ 0.0377 (N=1), ≈0.0051 (N=2), ≈0.0106 (N=4), ≈0.0301 (N=8).

  - These values are **much lower** than the high-Q regime seen in C5 (phase+cadence), and only slightly above cadence-only baselines.

  - There is no sign of a sharp, collective clock emerging from the interaction of domains with cadence.

## 5. Conclusion on cooperative effects

- The C6 run shows that adding domain glue to cadence yields only **mild** cooperative effects:

  - Directional alignment remains close to the diffusive √N pattern, with only modest enhancement at large `W_coh`.

  - Lockstep lengths grow slightly with `N` and `W_coh`, but do not exhibit the order-of-magnitude increases seen in the bias+cadence case.

  - Clock quality remains low; domains+cadence do not generate a high-Q internal clock.

- Intuitively, this fits the picture that domain glue primarily organises threads into spatial or label-based regions rather than directly enforcing a global direction or phase. Cadence, when combined with domains alone, does not find a strong handle to create either ultra-stiff motion or a clean clock.

- For BCQM V, C6 plays an important negative role: it shows that not all axis combinations lead to dramatic cooperative effects. Bias+cadence and phase+cadence stand out as special cases, whereas domains+cadence leave the system in a gently modified diffusive regime.
