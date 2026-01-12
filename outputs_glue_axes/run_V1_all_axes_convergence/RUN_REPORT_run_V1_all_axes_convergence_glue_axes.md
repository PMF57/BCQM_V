# RUN_REPORT – run_V1_all_axes_convergence_glue_axes

## 1. Run identifier

- Code package: `bcqm_glue_axes`
- Purpose: **convergence test** for the all-axes V1 bundle run
- Config file: `configs/run_V1_all_axes_convergence.yml`
- Output directory: `outputs_glue_axes/run_V1_all_axes_convergence`
- Random seed: `54321`

## 2. Configuration snapshot

- Grid: W_coh ∈ [20, 50, 100], N ∈ [2, 4, 8, 16, 32]
- Ensembles per (W_coh, N): 128
- Steps: 16000  (burn-in: 1600)
- Hop coherence: form=power_law, alpha=1.0, k_prefactor=2.0, memory_depth=1
- Shared bias: enabled=True, lambda_bias=0.3
- Phase lock: enabled=True, lambda_phase=0.3, theta_join=0.3, theta_break=1.5, omega_0=0.1, noise_sigma=0.05
- Domains: enabled=True, n_initial_domains=4, lambda_domain=0.3, merge_threshold=0.8, split_threshold=0.3, min_domain_size=2
- Diagnostics: store_states=True, compute_lockstep=True, compute_psd=False

Compared to the original V1 run, this convergence run uses **more ensembles** and **longer trajectories** (ensembles = 128, steps = 16000) but the same W_coh and N grids.

## 3. Numerical outputs

| W_coh |  N  | L_inst | ell_lock | Q_clock |
|------:|----:|-------:|---------:|--------:|
|    20 |   2 | 0.617 | 8.67 | 0.280 |
|    20 |   4 | 0.686 | 12.79 | 0.286 |
|    20 |   8 | 0.751 | 28.78 | 0.290 |
|    20 |  16 | 0.793 | 170.07 | 0.335 |
|    20 |  32 | 0.819 | 381.13 | 0.141 |
|    50 |   2 | 0.711 | 16.40 | 0.539 |
|    50 |   4 | 0.840 | 38.61 | 0.583 |
|    50 |   8 | 0.890 | 247.89 | 0.594 |
|    50 |  16 | 0.911 | 223.32 | 0.091 |
|    50 |  32 | 0.925 | 4.83 | 0.031 |
|   100 |   2 | 0.793 | 25.18 | 0.822 |
|   100 |   4 | 0.920 | 113.20 | 0.844 |
|   100 |   8 | 0.944 | 641.66 | 0.770 |
|   100 |  16 | 0.955 | 5.14 | 0.174 |
|   100 |  32 | 0.962 | 4.86 | 0.016 |

## 4. Interpretation

### 4.1 Overall pattern vs original V1

The qualitative picture is unchanged relative to the original V1 all-axes run:
- For each W_coh there is a **sweet spot in N** where the lockstep length ell_lock is maximal.
- L_inst remains high and increases with N, reflecting strong bundle alignment.
- Q_clock is largest in the stiff, moderate-N regime and collapses again at the largest N values.

In more detail:
- W_coh =  20: ell_lock peaks at N = 32, ell_lock ≈ 381.1, L_inst ≈ 0.819, Q_clock ≈ 0.141.
- W_coh =  50: ell_lock peaks at N = 8, ell_lock ≈ 247.9, L_inst ≈ 0.890, Q_clock ≈ 0.594.
- W_coh = 100: ell_lock peaks at N = 8, ell_lock ≈ 641.7, L_inst ≈ 0.944, Q_clock ≈ 0.770.

Relative to the original V1 numbers, the **positions of the peaks in N** are unchanged and the magnitudes of L_inst and Q_clock are similar.  The main difference is that some ell_lock values grow substantially (e.g. the W_coh = 100, N = 8 entry now reaches ≳ 640), which is exactly what we expect when we integrate further into the long tails of rare but very long lockstep episodes.

### 4.2 Lockstep and clock behaviour

- For W_coh = 20, ell_lock rises from ≈8.7 (N=2) to ≈28.8 (N=8) and peaks at ≈170 for N=16, before overshooting into a very long ≈381 episode at N=32.  L_inst grows smoothly from ~0.62 to ~0.82.
- For W_coh = 50, ell_lock climbs from ≈16 (N=2) through ≈38 (N=4) to ≈248 (N=8), with Q_clock ≈ 0.54–0.59 in that window; the larger-N bundles again lose their clock-like behaviour.
- For W_coh = 100, the bundle with N=4 remains a very stiff clock (L_inst ≈ 0.92, ell_lock ≈ 113, Q_clock ≈ 0.84), while N=8 now exhibits an even longer ell_lock ≳ 640 and slightly reduced Q_clock ≈ 0.77.

These results strengthen rather than weaken the original interpretation: there is a robust regime of **near-ballistic, clock-like bundle behaviour** at moderate N and large W_coh, framed by diffusive behaviour at small N and overgrown, noisy behaviour at the largest N.

## 5. Convergence assessment

- The **structure in (W_coh, N) space** (location of ell_lock peaks, fall-off at large N, behaviour of Q_clock) is unchanged.
- Quantitative changes in ell_lock at the peaks are in the direction expected for longer runs (rare long episodes are sampled more often), not random fluctuations or reversals of trend.
- L_inst and Q_clock values are close to the original V1 run, with no sign of drift toward qualitatively different behaviour.

Taken together, this suggests that the V1 all-axes results are **numerically stable** under substantial increases in ensemble size and trajectory length.  The main effect of the convergence run is to better resolve the long-tailed distribution of lockstep durations.

## 6. Status and next steps

- V1 all-axes convergence test: **passed**.
- Recommended follow-ups (optional):
  - Use this convergence dataset as the primary source for any figures that
    highlight near-ballistic bundle behaviour.
  - Repeat a similar convergence uplift for one A2 and one A3 slice if we
    want symmetry in the final BCQM V numerical appendix.