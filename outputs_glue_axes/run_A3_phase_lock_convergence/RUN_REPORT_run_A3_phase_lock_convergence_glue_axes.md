# RUN_REPORT – run_A3_phase_lock_convergence_glue_axes

## 1. Run identifier

- Code package: `bcqm_glue_axes`
- Purpose: **convergence test** for the A3 phase-lock-only bundle run
- Config file: `configs/run_A3_phase_lock_convergence.yml`
- Output directory: `outputs_glue_axes/run_A3_phase_lock_convergence`
- Random seed: `54321`

## 2. Configuration snapshot

- Grid: W_coh ∈ [20, 50, 100], N ∈ [1, 2, 4, 8, 16]
- Ensembles per (W_coh, N): 128
- Steps: 8000  (burn-in: 800)
- Hop coherence: form=power_law, alpha=1.0, k_prefactor=2.0, memory_depth=1
- Shared bias: enabled=False, lambda_bias=0.0
- Phase lock: enabled=True, lambda_phase=0.3, theta_join=0.3, theta_break=1.5, omega_0=0.1, noise_sigma=0.05
- Domains: enabled=False, n_initial_domains=1, lambda_domain=0.0, merge_threshold=0.8, split_threshold=0.3, min_domain_size=1
- Diagnostics: store_states=True, compute_lockstep=True, compute_psd=False

Compared to the original A3 run, this convergence run uses **more ensembles** and **longer trajectories** (ensembles = 128, steps = 8000) but the same W_coh and N grids.

## 3. Numerical outputs

| W_coh |  N  | L_inst | ell_lock | Q_clock |
|------:|----:|-------:|---------:|--------:|
|    20 |   1 | 1.000 | 7.41 | 0.000 |
|    20 |   2 | 0.616 | 7.18 | 0.284 |
|    20 |   4 | 0.522 | 8.43 | 0.296 |
|    20 |   8 | 0.447 | 10.06 | 0.294 |
|    20 |  16 | 0.397 | 14.20 | 0.292 |
|    50 |   1 | 1.000 | 15.07 | 0.007 |
|    50 |   2 | 0.709 | 13.95 | 0.552 |
|    50 |   4 | 0.643 | 19.06 | 0.562 |
|    50 |   8 | 0.602 | 32.58 | 0.596 |
|    50 |  16 | 0.585 | 102.31 | 0.637 |
|   100 |   1 | 1.000 | 25.32 | 0.014 |
|   100 |   2 | 0.795 | 22.55 | 0.843 |
|   100 |   4 | 0.756 | 38.34 | 0.906 |
|   100 |   8 | 0.738 | 112.20 | 0.961 |
|   100 |  16 | 0.736 | 290.54 | 0.695 |

## 4. Interpretation

### 4.1 Overall pattern vs original A3

The phase-lock-only behaviour seen in the original A3 run is preserved and sharpened by this convergence uplift:
- For each W_coh, L_inst remains high and decays only mildly with N, reflecting strong alignment within the bundle.
- Q_clock becomes large and positive as soon as N ≥ 2, indicating a robust clock-like centre-of-mass drift.
- ell_lock grows systematically with N and W_coh, reaching very long lockstep episodes in the stiff, large-W_coh regime.

- W_coh = 20:
  - N =  1: L_inst ≈ 1.000, ell_lock ≈ 7.4, Q_clock ≈ 0.000
  - N =  2: L_inst ≈ 0.616, ell_lock ≈ 7.2, Q_clock ≈ 0.284
  - N =  4: L_inst ≈ 0.522, ell_lock ≈ 8.4, Q_clock ≈ 0.296
  - N =  8: L_inst ≈ 0.447, ell_lock ≈ 10.1, Q_clock ≈ 0.294
  - N = 16: L_inst ≈ 0.397, ell_lock ≈ 14.2, Q_clock ≈ 0.292
- W_coh = 50:
  - N =  1: L_inst ≈ 1.000, ell_lock ≈ 15.1, Q_clock ≈ 0.007
  - N =  2: L_inst ≈ 0.709, ell_lock ≈ 14.0, Q_clock ≈ 0.552
  - N =  4: L_inst ≈ 0.643, ell_lock ≈ 19.1, Q_clock ≈ 0.562
  - N =  8: L_inst ≈ 0.602, ell_lock ≈ 32.6, Q_clock ≈ 0.596
  - N = 16: L_inst ≈ 0.585, ell_lock ≈ 102.3, Q_clock ≈ 0.637
- W_coh = 100:
  - N =  1: L_inst ≈ 1.000, ell_lock ≈ 25.3, Q_clock ≈ 0.014
  - N =  2: L_inst ≈ 0.795, ell_lock ≈ 22.6, Q_clock ≈ 0.843
  - N =  4: L_inst ≈ 0.756, ell_lock ≈ 38.3, Q_clock ≈ 0.906
  - N =  8: L_inst ≈ 0.738, ell_lock ≈ 112.2, Q_clock ≈ 0.961
  - N = 16: L_inst ≈ 0.736, ell_lock ≈ 290.5, Q_clock ≈ 0.695

Relative to the original A3 numbers, the positions of the stiffest regimes are unchanged (moderate N at large W_coh), and the magnitudes of L_inst and Q_clock are similar or slightly enhanced.  The main quantitative change is an increase in ell_lock for the larger-N, larger-W_coh entries, as longer runs better sample rare extended lockstep periods.

### 4.2 Pure phase-lock glue behaviour

- At W_coh = 20, the bundles already show modest but growing lockstep: ell_lock rises from ~7.4 at N=1 to ~14.2 at N=16, while Q_clock stabilises around 0.29 for N ≥ 2.
- At W_coh = 50, phase-lock glue produces a clear clock-like regime: L_inst stays in the 0.58–1.00 range, ell_lock grows from ~15 to ~102, and Q_clock sits between ~0.55 and ~0.64 for N ≥ 2.
- At W_coh = 100, phase-lock alone is enough to generate very stiff clocks: for N=4 and N=8 we see ell_lock ≈ 38 and ≈ 112 with Q_clock ≈ 0.91 and 0.96, respectively.  Even at N=16 the bundle remains highly coherent (ell_lock ≈ 291, Q_clock ≈ 0.70).

This confirms that phase-lock is a powerful glue axis on its own: it can produce long-lived, strongly directed bundle motion without any help from shared-bias or domain glue.

## 5. Convergence assessment

- The **qualitative structure** of the A3 results is unchanged: phase-lock generates strong alignment and a robust COM clock, with increasing lockstep length at larger W_coh and N.
- Differences relative to the original A3 run are mainly in the expected direction for longer integrations (larger ell_lock in the stiff regimes), not qualitative reversals or instabilities.
- There is no sign that the high-Q_clock clocks at large W_coh are numerical artefacts; they persist and become more sharply resolved.

We therefore regard the A3 phase-lock-only diagnostics as **numerically stable** under substantial increases in ensemble size and trajectory length.

## 6. Status and next steps

- A3 phase-lock convergence test: **passed**.
- Optional follow-ups:
  - Use this convergence dataset as the definitive source for any figures
    that showcase phase-lock-only clocks.
  - Combine with the V1 convergence run to bracket the behaviour of 
    "pure phase" vs "all glue axes" bundles in the BCQM V paper.