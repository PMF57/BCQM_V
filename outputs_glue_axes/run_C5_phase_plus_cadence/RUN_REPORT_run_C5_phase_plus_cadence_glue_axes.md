# RUN_REPORT: run_C5_phase_plus_cadence (v0.2 cadence-gated code)

## 1. Run identification

- **Run ID:** `run_C5_phase_plus_cadence`

- **Purpose:** Test for cooperative effects between **phase-lock glue** and **cadence glue**, using parameters where each axis on its own produces only modest structure.

- **Code:** `bcqm_glue_axes` (cadence-enabled v0.2).

- **Random seed:** 56789


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

  - shared_bias: enabled = False, lambda_bias = 0.0 (off in this run)

  - phase_lock: enabled = True, lambda_phase = 0.25, omega_0 = 0.1, theta_join = 0.3, theta_break = 1.5, noise_sigma = 0.0

  - domains: enabled = False, lambda_domain = 0.0 (off in this run)

- **Cadence axis:**

  - Enabled in the C5 YAML (same settings as C3/C4):

    - distribution = `lognormal`

    - mean_T = 1.0, sigma_T ≈ 0.2

    - lambda_cadence = 0.15

  - Operationally: `cadence_step` is called each step, gating which threads are active and gently nudging periods toward the mean.

- **Diagnostics:**

  - store_states = True, compute_lockstep = True, compute_psd = False


## 3. Key observables

Ensemble-averaged instantaneous alignment `L_inst`, lockstep length `ell_lock`, and clock quality `Q_clock` for each `(W_coh, N)` pair:

### 3.20  W_coh = 20

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 9.852 | 0.004 |
| 2 | 0.624 | 9.633 | 0.303 |
| 4 | 0.525 | 11.008 | 0.291 |
| 8 | 0.450 | 13.655 | 0.288 |

### 3.50  W_coh = 50

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 17.883 | 0.013 |
| 2 | 0.718 | 16.382 | 0.589 |
| 4 | 0.656 | 23.695 | 0.604 |
| 8 | 0.613 | 40.934 | 0.620 |

### 3.100  W_coh = 100

| N | L_inst | ell_lock | Q_clock |

|---|--------|----------|---------|

| 1 | 1.000 | 33.854 | 0.024 |
| 2 | 0.797 | 26.198 | 0.815 |
| 4 | 0.763 | 43.985 | 0.930 |
| 8 | 0.748 | 109.051 | 0.912 |

## 4. Interpretation

- **Alignment (`L_inst`):**

  - For `N = 1`, `L_inst` is exactly 1.0 at all `W_coh`, as expected.

  - For `N = 2`, `L_inst` sits in the 0.62–0.80 range as `W_coh` increases, modestly above the pure √N diffusive value (~0.71) at high `W_coh`.

  - For `N = 4` and `N = 8`, `L_inst` rises with `W_coh` but stays lower than in the bias+cadence case (C4):

    - At `W_coh = 100`, `L_inst` ≈ 0.76 (N=4) and ≈ 0.75 (N=8), compared to ≈0.79 and ≈0.89 in C4.

  - So phase+cadence do increase directional coherence relative to a purely diffusive or cadence-only baseline, but they do not make large bundles as stiff as bias+cadence did.

- **Lockstep length (`ell_lock`):**

  - `ell_lock` grows with `W_coh` for `N = 1` (≈9.85, 17.88, 33.85 for W = 20, 50, 100), matching earlier trends.

  - For `N = 2`, lockstep stays close to the single-thread value for each `W_coh`.

  - For `N = 4` and `N = 8`, `ell_lock` is clearly enhanced compared to hop-only and cadence-only baselines, but less dramatically than in the bias+cadence case:

    - At `W_coh = 100`, `ell_lock` ≈ 43.99 (N=4) and ≈109.05 (N=8), versus ≈91 and ≈289 in C4.

  - This suggests that phase-lock + cadence cooperatively extend the typical lockstep duration, but bias remains the dominant driver of very long-lived directional alignment.

- **Clock quality (`Q_clock`):**

  - `Q_clock` shows a striking feature: for `W_coh >= 50`, bundles with `N >= 2` achieve relatively high values (≈0.59–0.93), substantially higher than in bias+cadence.

  - In particular, at `W_coh = 100`:

    - `Q_clock` ≈ 0.81 (N=2), ≈0.93 (N=4), ≈0.91 (N=8).

  - This indicates that phase-lock + cadence are very efficient at producing a **high-quality internal clock**, even when directional stiffness is only moderate.

## 5. Conclusion on cooperative effects

- Compared to cadence alone (C3), adding phase-lock glue produces a **strong cooperative effect on clock quality**: `Q_clock` becomes large (≳0.8) for multi-thread bundles at high `W_coh`, signalling a robust collective tick.

- Directional alignment (`L_inst`) and lockstep length (`ell_lock`) are enhanced relative to purely diffusive baselines, but not as dramatically as in the bias+cadence run (C4). This matches the intuition that phase-lock prefers to organise oscillatory phases rather than pick a single spatial direction.

- Taken together, C4 and C5 suggest a division of labour:

  - **Bias + cadence**: best for long-lived directional stiffness (large `ell_lock`, high `L_inst`), with only modest clock improvements.

  - **Phase + cadence**: best for high-quality clocks (`Q_clock` ≈ 1) while keeping only moderate directional stiffness.

- For BCQM V, this run supports the idea that different pairs of glue axes carve out different regimes:

  - Some bundles behave more like stiff “pointer” structures (bias-dominated),

  - others behave more like good internal clocks (phase-dominated),

  - and cadence acts as a supporting axis that amplifies whichever tendency is already present.
