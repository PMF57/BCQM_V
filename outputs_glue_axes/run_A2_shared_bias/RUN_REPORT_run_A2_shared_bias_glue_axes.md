# RUN_REPORT – run_A2_shared_bias_glue_axes

## 1. Run identifier

- Code package: `bcqm_glue_axes`
- Glue axes: **shared-bias only** (no phase-lock, no domains)
- Config file (intended): `configs/run_A2_shared_bias.yml`
- Output directory (convention): `outputs_glue_axes/run_A2_shared_bias`
- Random seed: `12345`

## 2. Configuration snapshot

- Grid: W_coh ∈ [20, 50, 100], N ∈ [1, 2, 4, 8, 16]
- Ensembles per (W_coh, N): 32
- Steps: 2000  (burn-in: 200)
- Hop coherence (soft-rudder style): form=power_law, alpha=1.0, k_prefactor=2.0
- Shared-bias glue: **enabled = True**, lambda_bias = 0.3
- Phase-lock axis: enabled=False, lambda_phase=0.0
- Domains axis: enabled=False, n_initial_domains=1, lambda_domain=0.0
- Diagnostics: store_states=True, compute_lockstep=True

## 3. Numerical outputs (lockstep metrics)

Summary table from `summary.json` (per (W_coh, N)):

| W_coh | N  | L_inst | ell_lock | Q_clock |
|------:|---:|-------:|---------:|--------:|
|    20 |  1 | 1.000 | 7.60 | 0.000 |
|    20 |  2 | 0.503 | 7.21 | 0.012 |
|    20 |  4 | 0.581 | 9.35 | 0.002 |
|    20 |  8 | 0.647 | 16.39 | 0.011 |
|    20 | 16 | 0.675 | 56.51 | 0.010 |
|    50 |  1 | 1.000 | 16.21 | 0.008 |
|    50 |  2 | 0.496 | 13.03 | 0.024 |
|    50 |  4 | 0.706 | 27.96 | 0.018 |
|    50 |  8 | 0.829 | 102.18 | 0.075 |
|    50 | 16 | 0.841 | 15.24 | 0.019 |
|   100 |  1 | 1.000 | 23.48 | 0.028 |
|   100 |  2 | 0.514 | 23.74 | 0.051 |
|   100 |  4 | 0.826 | 66.93 | 0.166 |
|   100 |  8 | 0.910 | 53.03 | 0.081 |
|   100 | 16 | 0.913 | 5.19 | 0.326 |

## 4. Interpretation

### 4.1 Baseline checks (N = 1)

- W_coh =  20: N = 1 gives L_inst = 1.000 (as expected, fully aligned), ell_lock ≈ 7.60, Q_clock ≈ 0.000.
- W_coh =  50: N = 1 gives L_inst = 1.000 (as expected, fully aligned), ell_lock ≈ 16.21, Q_clock ≈ 0.008.
- W_coh = 100: N = 1 gives L_inst = 1.000 (as expected, fully aligned), ell_lock ≈ 23.48, Q_clock ≈ 0.028.

This is the single-thread telegraph baseline: lockstep persistence grows with W_coh (≈7.6 → 16.2 → 23.5), but there is no notion of multi-thread bundle coherence.

### 4.2 Effect of shared-bias glue for N > 1

- For **all W_coh**, increasing N above 1 produces partial but clear bundle coherence:
  - L_inst rises from ≈0.5 at N = 2 up to ≈0.8–0.9 for intermediate N,
  - ell_lock develops a pronounced peak at some N, often much larger than the N = 1 baseline.

- W_coh =  20: peak ell_lock ≈ 56.5 at N = 16 with L_inst ≈ 0.675, Q_clock ≈ 0.010.
- W_coh =  50: peak ell_lock ≈ 102.2 at N = 8 with L_inst ≈ 0.829, Q_clock ≈ 0.075.
- W_coh = 100: peak ell_lock ≈ 66.9 at N = 4 with L_inst ≈ 0.826, Q_clock ≈ 0.166.

This is exactly the qualitative behaviour we wanted from a **modest mean-field glue axis**:
- single-thread behaviour sets the diffusive baseline,
- multi-thread bundles can lock together for much longer stretches without becoming perfectly rigid.

### 4.3 Non-monotonic behaviour at large N

At the largest N values the persistence sometimes **drops** again, despite high L_inst, e.g.:
- W_coh = 50: ell_lock peaks ≈102 at N = 8 but falls back to ≈15 at N = 16;
- W_coh = 100: ell_lock peaks ≈67 at N = 4, ≈53 at N = 8, then collapses to ≈5 at N = 16
  while L_inst remains ≳0.9 and Q_clock rises to ≈0.33.

This suggests that, for fixed lambda_bias = 0.3, very large bundles can become **over-constrained**: they maintain high instantaneous alignment but decorrelate more rapidly in time, and the COM acquires a stronger net drift (larger Q_clock). In other words, this simple shared-bias rule has a natural "sweet spot" in N where lockstep is longest, beyond which the behaviour is less coherent.

## 5. Provisional conclusions

- The shared-bias axis by itself is enough to move us **beyond the single-thread diffusive baseline**:
  we see extended lockstep (ell_lock) and elevated bundle alignment (L_inst) for moderate N.

- The run **does not** reproduce the extreme rigidity of the 2×2 hierarchical toy from IV_d lab runs: alignment is strong but not perfect, lockstep has a finite peak, and COM motion remains noisy.
- There is a clear **tension between bundle size and glue strength**: with fixed lambda_bias, large N does not simply mean "better"—instead we get a peak in ell_lock and then a fall-off. This will be a useful constraint when we tune the full four-axis glue model in BCQM V.

## 6. To-do / follow-ups

- [ ] Run the hop-only baseline (A1) with the same W_coh and N grid to get a clean diffusive reference.
- [ ] Plot L_inst and ell_lock vs N at fixed W_coh (and vice versa) to visualise the sweet-spot behaviour.
- [ ] Check robustness vs ensembles and steps (e.g. double ensembles or T to see if peaks persist).
- [ ] Decide whether any of these slices should appear in the main BCQM V figures or remain in lab notes.
